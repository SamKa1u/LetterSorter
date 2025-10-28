import regex
import numpy as np
import json

# paddle
from paddleocr import PaddleOCR

# easy
import easyocr

def loadOCR():
    ocr = PaddleOCR(
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
            )
    reader = easyocr.Reader(['en'])  # this needs to run only once to load the model into memory
    return ocr, reader

def Optical_Char_Rec(OCR_backend: str, image, ocr, reader):
    """
    Takes an image and returns letter character recognition result based on selected OCR backend (paddleOCR | easyOCR).
    :param reader: easyocr class
    :param ocr: paddleocr class
    :param image: image containing characters to be recognized
    :param OCR_backend: the OCR framework the backend should use
    :returns result: letter text recognition result
    """
    np_image = np.array(image)
    # paddleOCR
    if OCR_backend == 'paddle':
        result = ocr.predict(
            input=np_image
        )
        print("type:", type(result), "\nresult:", result)
        return result
    # easyOCR
    elif OCR_backend == 'easy':
        result = reader.readtext(np_image, detail=0)
        json_str = json.dumps(result)      # dump list into string
        print("type:",type(json_str),"\nresult:",json_str)
        return json_str
    else:
        return 'Backend does not contain a matching OCR framework'

def get_pattern_match(pattern, txt):
        matches = regex.findall(pattern, txt)
        if matches:
            return matches[0]
        else:
            return None

if __name__ == "__main__":
    text = "Lubbock Texas 79401"
    match = get_pattern_match("[A-z]* [A-z]* [0-9][0-9][0-9][0-9][0-9]", text)   # update to take care of commas inbetween city and state
    print(match)