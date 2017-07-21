import zbar

from PIL import Image
import cv2
import numpy

id = "null"
capture = cv2.VideoCapture(0)

# Breaks down the video into frames
while(True):
    ret, frame = capture.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    scanner = zbar.Scanner()
    results = scanner.scan(frame)
    for result in results:
        print(result.data)