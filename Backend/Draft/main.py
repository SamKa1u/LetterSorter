import uvicorn
from PIL import Image
from ocr import Optical_Char_Rec, get_pattern_match, loadOCR
from fastapi import FastAPI, File, UploadFile, HTTPException
from io import BytesIO
import glob
import json

app = FastAPI()

@app.get("/")
def read_root():
    global ocr, reader
    ocr, reader = loadOCR()
    return {"message": "Welcome from the LetterSorter API"}

@app.post("/receive_img")
async def receive_img(OCR_backend: str, file: UploadFile = File(...) ):
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
    file_pattern = '../backend/output/*.json'
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
        city_state_zip = None
        for texts in rec_texts:
            _ = get_pattern_match("[A-z]* [A-z]* [0-9][0-9][0-9][0-9][0-9]",texts)
            if _ != city_state_zip:  # if pattern is matched assign match to city_state_zip
                city_state_zip = _
                break
        if city_state_zip is None:
            raise HTTPException(status_code=404, detail=f"city state zip pattern not found in rec_texts list") # if no break -> pattern was not in rec texts list
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"city state zip pattern not found: {e}")

    return {
        "message": city_state_zip,
    }



if __name__=="__main__":
    uvicorn.run("main:app", host="100.95.80.63", port=8080)