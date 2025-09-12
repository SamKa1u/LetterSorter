import uvicorn
from PIL import Image
from ocr import *
from fastapi import FastAPI, File, UploadFile, HTTPException
from io import BytesIO
import json
import glob

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome from the LetterSorter API"}

@app.post("/receive_img")
async def receive_img(file: UploadFile = File(...)):
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
        letter_chars = Optical_Char_Rec(img)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"OCR failed, letter characters not found: {e}")

    # save recognition result to json
    for res in letter_chars:
        res.save_to_json("output")

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
        rec_texts = data["rec_texts"]
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

    return {"message": city_state_zip,
        }



if __name__=="__main__":
    uvicorn.run("main:app", host="100.95.80.63", port=8080)