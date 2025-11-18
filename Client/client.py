import requests as rq
import cv2

# localization
from localization import localize_response

# fastapi URL config
base_url = "https://samka1u--ocr-fastapi-app.modal.run"
endpoints = ["/","/receive_img"]
URLparams =  [
    {"OCR_backend": "paddle"},
    {"OCR_backend": "easy"}
]

# load OCR frameworks
rq.get(base_url + endpoints[0])


def main():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        exit()
    while True:
        # preview with openCV
        ret, frame =  cap.read()
        if frame is None:
            print('[Cam] frame skipped')
            continue
        cv2.imshow("frame", frame)

        # capture and send image of letter if c key is pressed
        k = cv2.waitKey(1)
        if k  == ord('c'):
            # save letter image
            cv2.imwrite("letter_image.png", frame)

            # send letter image to LetterSorter app
            try:
                files = {'file': open('letter_image.png', 'rb')}
            except Exception as e:
                print(f"letter image file could not be opened: {e}")  # exit program if letter image not saved
                break

            location = rq.post(base_url + endpoints[1], files=files, params=URLparams[0])
            status = location.status_code
            if status != 200:
                print(f"[response error] status code: {status},response: {location.content}")
                continue
            else:
                b_resp = location.content
                localize_response(b_resp)
        # exit program on 'esc' key pressed
        elif k == 27:
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    # location = b"lubbock texas 79401"
    # encoded_region = localize_response(location)

