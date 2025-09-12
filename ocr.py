from paddleocr import PaddleOCR

def Optical_Char_Rec(image):
    """
    Takes an image and returns character recognition result.
    :param image: image of letter to be read
    :return result: letter text recognition result
    """
    result = ocr.predict(
        input = image
    )
    return result


if "__name__" == "__main__":
    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False
    )