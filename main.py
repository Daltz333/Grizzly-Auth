import zbar

from PIL import Image
from datetime import datetime
import cv2
import data



def main():
    capture = cv2.VideoCapture(0)
    prevID = 0

    date1 = datetime.today().date()

    while True:
        # Breaks down the video into frames
        ret, frame = capture.read()

        # Converts image to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        image = Image.fromarray(gray)
        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())

        # Scans the zbar image.
        scanner = zbar.ImageScanner()
        scanner.scan(zbar_image)

        # Prints data from image.
        for decoded in zbar_image:
            idnumber = decoded.data

            if (date1 < datetime.today().date()):
                data.logout()

            if (idnumber != prevID):
                data.login(idnumber)

            else:
                pass

            prevID = idnumber

main()
