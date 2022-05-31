import cv2
import imutils
import time
from app.IA import liberacao

def reconhecedorLbph(lista):
    
    camera = cv2.VideoCapture(0)

    greenLower = (29, 86, 6)
    greenUpper = (64, 255, 255)
    while (True):
        _, frame = camera.read()

        if frame is None:
            break

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
            print(x,y)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for cnt in cnts:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            #print(len(approx))
            
            if len(approx)==3:
                #print("Green = triangle")
                
                cv2.drawContours(frame,[cnt],0,(0,255,0),-1)
            elif len(approx)==4:
                #print("Red = square")
                
                cv2.drawContours(frame,[cnt],0,(0,0,255),-1)
            
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()