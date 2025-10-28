import requests as rq
import cv2
from picamera2 import Picamera2
import time

# localization
from uszipcode import SearchEngine

# fastapi URL config
base_url = "http://100.95.80.63:8080"
endpoints = ["/","/receive_img"]
URLparams =  [
    {"OCR_backend": "paddle"},
    {"OCR_backend": "easy"}
]

# load OCR frameworks
rq.get(base_url + endpoints[0])

# initialize Picamera
cam = Picamera2()
config = cam.create_preview_configuration({'format': 'BGR888'})
cam.configure(config)
cam.start()
time.sleep(1)

def get_us_region(zipcode):
    """
    Takes a U.S. zip code and returns the Census region.
    """
    search = SearchEngine()
    zip_info = search.by_zipcode(zipcode)
    if zip_info:
        return {
            "region": zip_info.major_city_state.region,
        }
    return None

def main():
    while True:
        # preview with openCV
        frame =  cam.capture_array()
        if frame is None:
            print('[Picam] frame skipped')
            continue
        cv2.imshow("frame", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # capture and send image of letter if c key is pressed
        k = cv2.waitKey(1)
        if k  == ord('c'):
            # save letter image
            cam.capture_file("letter_image.png")

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
                print(location.content)
                zipcode = location.content[-1:-5]
                region = get_us_region(zipcode)
                print(region)

        # exit program on 'esc' key pressed
        elif k == 27:
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
