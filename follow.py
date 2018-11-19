from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, GPIO.HIGH)

camera = PiCamera()
camera.resolution = (320, 240)
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=(320, 240))
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image=frame.array

    roi=image[220:120,0:319]
    
    blackline=cv2.inRange(roi, (0,0,0), (100,100,100))
    kernel=np.ones((3,3), np.uint8)
    blackline=cv2.erode(blackline,kernel,iterations=5)
    blackline=cv2.dilate(blackline,kernel,iterations=6)
    contours,hierarchy = cv2.findContours(blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image,contours,-1,(0,255,0),2)
    if len(contours)>0:
        x,y,w,h = cv2.boundingRect(contours[0])
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.line(image,(x+(w/2),120), (x+(w/2),220),(255,0,0),2)
    cv2.imshow("Black in range", blackline)
    cv2.imshow("Original with contours",image)
    rawCapture.truncate(0)
    key=cv2.waitKey(1) & 0xFF
    if key==ord("q"):
        break

    GPIO.output(40, GPIO.LOW)
    
