import regex
import numpy as np

# paddle
from paddleocr import PaddleOCR

def loadOCR():
    """
    Preloads paddle OCr backend
    :returns ocr: instantiation of paddle OCR class
    """
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
    # print("begin")
    np_image = np.array(image)
    # print("image")
    # paddleOCR
    if OCR_backend == 'paddle':
        # print("paddle")
        result = ocr.predict(
            input=np_image
        )
        try:
            print("type:", type(result), "\nresult:", result)
            return result
        except IndexError as e:
            return f"{e}: transcription failed"
    else:
        return 'Backend does not contain a matching OCR framework'

def get_pattern_match(pattern, txt):
    """
    Takes a pattern and text string and returns matches for the pattern.
    :param txt: (Str) a string of text pattern will be searched for in.
    :param pattern: (Any) the regex pattern to match.
    :returns matches: (list) pattern recognition result.
    """
    matches = regex.findall(pattern, txt)
    # print("matches:",matches)
    if matches:
        return matches
    else:
        return None

if __name__ == "__main__":
    text = "W A. Brahm Linkon 1863 Bloadway W, Blvd Boulder Colorado 64925 27 DBF-1P1 "
    match = get_pattern_match("(New [A-z]* [0-9][0-9][0-9][0-9][0-9]|South [A-z]* [0-9][0-9][0-9][0-9][0-9]|West [A-z]* [0-9][0-9][0-9][0-9][0-9]|North [A-z]* [0-9][0-9][0-9][0-9][0-9]|Rhode [A-z]* [0-9][0-9][0-9][0-9][0-9])|([A-z]*, [A-z]* [0-9][0-9][0-9][0-9][0-9]|[A-z]* [A-z]* [0-9][0-9][0-9][0-9][0-9])", text)   # update to take care of commas inbetween city and state   # brittle og : [A-z]* [A-z]* [0-9][0-9][0-9][0-9][0-9]
    print(match)                                                                                                            # commas : [A-z]* [A-z]* [0-9][0-9][0-9][0-9][0-9]|[A-z]*, [A-z]* [0-9][0-9][0-9][0-9][0-9]
                                                                                                                            # 2 word states & commas: ([A-z]* [A-z]* [0-9][0-9][0-9][0-9][0-9])|([A-z]*, [A-z]* [A-z]* [0-9][0-9][0-9][0-9][0-9])|([A-z]* [A-z]* [A-z]* [0-9][0-9][0-9][0-9][0-9])|([A-z]*, [A-z]* [0-9][0-9][0-9][0-9][0-9])