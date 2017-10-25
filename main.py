#CREATED BY DALTON SMITH
import zbar
import cv2
import data
import time

from PIL import Image
from datetime import datetime
from imutils.video import WebcamVideoStream

def main():
    #note: multithreading is untested, if code no work, replace
    capture = WebcamVideoStream(src=0).start()
    prevID = 0
    oldtime = 0

    fixed_time = datetime.strptime("3:00:00.000000", "%H:%M:%S.%f")
    fixed_time2 = datetime.strptime("4:00:00.000000", "%H:%M:%S.%f")

    while True:

        current_time = datetime.strptime(str(datetime.today().time()), "%H:%M:%S.%f")

        #logout at 3am
        if (fixed_time < current_time and current_time > fixed_time2):
            #data.logout()
            pass

        else:
            pass

        # Breaks down the video into frames
        frame = capture.read()

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

            #if idnumber is not prevID, login
            if (idnumber != prevID):
                data.login(idnumber)
                oldtime = time.time()

            else:
                #if 5 minutes has passed, reset prevID
                if (time.time() - oldtime > 299):
                    #reset variables
                    prevID = 0
                    idnumber = 0

                else:
                    pass

            prevID = idnumber

        frame = cv2.flip(frame, 1)
        cv2.namedWindow('image',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image', 500, 390)
        cv2.rectangle(frame,(175,150),(450,350),(255,0,0),3)
        cv2.imshow('image', frame)
        if cv2.waitKey(1) == 27: 
            break # esc to quit

main()
