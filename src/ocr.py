import regex
import numpy as np

# paddle
from paddleocr import PaddleOCR

def loadOCR():
    ocr = PaddleOCR(
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
            )
    return ocr

def Optical_Char_Rec(OCR_backend: str, image, ocr):
    """
    Takes an image and returns letter character recognition result based on selected OCR backend (paddleOCR | easyOCR).
    :param ocr: instantiation of paddleocr class
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