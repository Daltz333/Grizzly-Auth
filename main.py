#CREATED BY DALTON SMITH
import imutils
from pyzbar import pyzbar
import cv2
import data
import time

from PIL import Image
from datetime import datetime
from imutils.video import WebcamVideoStream
from imutils.video import VideoStream

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
        frame = imutils.resize(frame, width=400)

        barcodes = pyzbar.decode(frame)

        # Prints data from image.
        for decoded in barcodes:
            idnumber = decoded.data.decode("utf-8")
            print(idnumber)

            (x, y, w, h) = decoded.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

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
        cv2.imshow('image', frame)
        if cv2.waitKey(1) == 27: 
            break # esc to quit

main()
