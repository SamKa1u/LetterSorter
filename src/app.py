# modal deployment
import modal
image = modal.Image.debian_slim().apt_install("libgl1-mesa-glx", "libglib2.0-dev").pip_install(
    "fastapi[standard]",   #---------------utils
    "pillow",
    "numpy",
    "opencv-python-headless",
    "regex",
    "paddlepaddle",                  #---------------Paddle
    "paddleocr",
)
app = modal.App(image=image)

@app.function(image=image)  #gpu="H100"
@modal.concurrent(max_inputs=10)
@modal.asgi_app()
def fastapi_app():
    """
    FastAPI app cloud deployment for OCR backend
    :return: callable for modal labs container
    """
    from fastapi import FastAPI, File, UploadFile, HTTPException
    from src.ocr import loadOCR
    web_app = FastAPI()
    global ocr
    ocr = loadOCR()

    @web_app.get("/")
    def read_root():
        """
        Checks health of FastAPI app deployment to ensure models were properly downloaded into Modal container
        return: message indicating API status
        """
        import os
        os.mkdir("/output")                 # create ocr results output folder

        # check API health
        if ocr:
            return {"message": "Welcome to the Modal LetterSorter API, OCR frameworks successfully loaded"}
        else:
            return {"message": "Error loading OCR frameworks"}

    @web_app.post("/receive_img")
    async def receive_img(OCR_backend: str, file: UploadFile = File(...) ):
        """
        FastAPI app async endpoint for receiving images and calling optical character recognition
        :param OCR_backend: the OCR framework the backend should use
        :param file: the uploaded image file of text to run through OCR
        :return: response containing recognized text from image or error message
        """
        from src.ocr import Optical_Char_Rec, get_pattern_match
        from PIL import Image
        from io import BytesIO
        import glob
        import json
        try:
            # read contents
            contents = await file.read()

            # buffer
            image_stream = BytesIO(contents)

            # read image_stream into pil image
            img = Image.open(image_stream)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{e}")

        # process image with ocr model
        try:
            letter_chars = Optical_Char_Rec(OCR_backend, img, ocr)
            print(letter_chars)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"OCR failed, letter characters not found: {e}")

        # save recognition result to json file
        try:
            if OCR_backend == "paddle":
                for res in letter_chars:
                    res.save_to_json("output")          #attribute of paddleocr
            else:
                with open("output/ocrResult.json", "w") as f:
                    json.dump(letter_chars, f)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not save to json: {e}")

        # read recognition result json
        file_pattern = 'output/*.json'
        matching_files = glob.glob(file_pattern)
        try:
            with open(matching_files[-1], 'r') as file:
                data = json.load(file)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"letter text json not found:{e}")

        # parse recognized texts for city state zip
        if OCR_backend == "paddle":
            rec_texts = data["rec_texts"]
        else:
            rec_texts = data

        # concatenate list of recognized text strings into one string
        seperator = " "
        rec_text_string = seperator.join(rec_texts)
        print(rec_text_string)

        # get matches for city state zip or state zip
        just_state = False
        response = None
        res_index = None
        matches = get_pattern_match("(New [A-z]* [0-9][0-9][0-9][0-9][0-9]|South [A-z]* [0-9][0-9][0-9][0-9][0-9]|West [A-z]* [0-9][0-9][0-9][0-9][0-9]|North [A-z]* [0-9][0-9][0-9][0-9][0-9]|Rhode [A-z]* [0-9][0-9][0-9][0-9][0-9])|([A-z]*, [A-z]* [0-9][0-9][0-9][0-9][0-9]|[A-z]* [A-z]* [0-9][0-9][0-9][0-9][0-9])", rec_text_string)

        if matches:
            i = 0
            for match in matches:  # First Non-Empty String in list
                if match:
                    response = match
                res_index = i
                i += 1
            response = response[res_index]
            print("response:", response)
            print("res_index:", res_index)

            if res_index == 0:                  # set just_state flag if only state name is contained in message
                just_state = True
            print("Just State:", just_state)
        else:
            raise HTTPException(status_code=404, detail=f"list of matches is empty")

        return {
            "message": response,
            "Just State Flag": just_state,
        }
    return web_app

# modal deploy -m src.app --name=ocr