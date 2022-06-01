import cv2
import imutils
import time
from threading import *
import numpy as np
from numpy import linalg

from app.IA import liberacao

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

orangeLower = (180, 70, 255)
orangeUpper = (180, 0, 255)

blueLower = (101,50,38)
blueUpper = (255,255,110)

x1 = 0.0
y1 = 0.0

x2 = 0.0
y2 = 0.0

x3 = 0.0
y3 = 0.0

def reconhecedorLbph(lista):
    
    camera = cv2.VideoCapture(0)   

    while(True):

        _, frame = camera.read()

        if frame is None:
            break
      
        Thread_bola1 = Thread(target=bola1(frame))         
        Thread_bola1.start()
        
        Thread_bola2 = Thread(target=bola2(frame))         
        Thread_bola2.start()
        
        Thread_bola3 = Thread(target=bola3(frame))         
        Thread_bola3.start() 
        
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        
        if x1 != 0.0 and y1 != 0.0 and x2 != 0.0 and y2 != 0.0 and x3 != 0.0 and y3 != 0.0:
            Thread_comando = Thread(target=comando())
            Thread_comando.start()

        
    camera.release()
    cv2.destroyAllWindows()

def bola1(frame):

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    width, height = frame.shape[:2]
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # To see the centroid clearly
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 5)
            #cv2.imwrite("circled_frame.png", cv2.resize(frame, (int(height / 2), int(width / 2))))
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
        print("x1 = " , x , " | y1 = " , y)
        x1,y1 = x,y

       

def bola2(frame):
   
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    width, height = frame.shape[:2]
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, orangeLower, orangeUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # To see the centroid clearly
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 5)
            #cv2.imwrite("circled_frame.png", cv2.resize(frame, (int(height / 2), int(width / 2))))
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
        print("x2 = " , x , " | y2 = " , y)
        x2,y2 = x,y

def bola3(frame):
   
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    width, height = frame.shape[:2]
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, blueLower, blueUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # To see the centroid clearly
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 5)
            #cv2.imwrite("circled_frame.png", cv2.resize(frame, (int(height / 2), int(width / 2))))
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
        print("x3 = " , x , " | y3 = " , y)
        x3,y3 = x,y

        
def comando():
    print("Controlando carro!")

    matrix = np.array([[x1, y1, 1], [x2, y3, 1], [x3, y3, 1]]) 
    determinante = np.linalg.det(matrix)

    if(determinante == 0):
        print("Andar para frente ou para tras")


