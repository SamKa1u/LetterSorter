# modal deployment
import modal
image = modal.Image.debian_slim().apt_install("libgl1-mesa-glx", "libglib2.0-dev").pip_install(
    "fastapi[standard]",
    "paddlepaddle",
    "paddleocr",
    "easyocr",
    "pillow",
    "numpy",
    "opencv-python-headless",
    "opencv-contrib-python-headless",
    "streamlit",
    "uszipcode",
    "regex"
)
app = modal.App(image=image)

@app.function(image=image)  #gpu="H100"
@modal.concurrent(max_inputs=10)
@modal.asgi_app()
def fastapi_app():
    from fastapi import FastAPI, File, UploadFile, HTTPException
    from src.ocr import loadOCR
    web_app = FastAPI()
    global ocr, reader
    ocr, reader = loadOCR()

    @web_app.get("/")
    def read_root():
        import os
        os.mkdir("/output")

        if ocr is None:
            return {"message": "Error loading paddleOCR framework"}
        if reader is None:
            return {"message": "Error loading paddleOCR framework"}
        elif ocr and reader:
            return {"message": "Welcome to the Modal LetterSorter API, OCR frameworks successfully loaded"}
        else:
            return {"message": "Error loading OCR frameworks"}


    @web_app.post("/receive_img")
    async def receive_img(OCR_backend: str, file: UploadFile = File(...) ):
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
            letter_chars = Optical_Char_Rec(OCR_backend, img, ocr, reader)
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
        try:
            if OCR_backend == "paddle":
                rec_texts = data["rec_texts"]
            else:
                rec_texts = data

            # concatenate list of recognized text strings into one string
            seperator = " "
            rec_text_string = seperator.join(rec_texts)
            print(rec_text_string)
            city_state_zip = None

            _ = get_pattern_match("[A-z]* [A-z]* [0-9][0-9][0-9][0-9][0-9]", rec_text_string)
            if _ != city_state_zip:  # if pattern is matched assign match to city_state_zip
                city_state_zip = _

            if city_state_zip is None:
                raise HTTPException(status_code=404, detail=f"city state zip pattern not found in rec_texts list") # if no break -> pattern was not in rec texts list
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"city state zip pattern not found: {e}")

        return {
            "message": city_state_zip,
        }
    return web_app

if __name__=="__main__":
    pass
# modal deploy -m src.app --name=ocr