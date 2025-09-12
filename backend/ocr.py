from paddleocr import PaddleOCR
import regex
import numpy as np

def Optical_Char_Rec(image):
    """
    Takes an image and returns letter character recognition result.
    :param image: image of letter to be read
    :return result: letter text recognition result
    """
    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
    )
    result = ocr.predict(
        input = np.array(image)
    )
    return result

def get_pattern_match(pattern, txt):
        matches = regex.findall(pattern, txt)
        if matches:
            return matches[0]
        else:
            return None

if __name__ == "__main__":
    text = "Lubbock Texas 79401"
    match = get_pattern_match("[A-z]* [A-z]* [0-9][0-9][0-9][0-9][0-9]", text)
    print(match)