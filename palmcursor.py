import cv2
from cvzone.HandTrackingModule import HandDetector
import mouse
import numpy as np
import time

detector = HandDetector(detectionCon=0.9,maxHands=1)

cap = cv2.VideoCapture(0)
alien_w , alien_h = 640,480
cap.set(3, alien_w)
cap.set(4, alien_h)
frame= 100
l_delay = 1

def l_click_delay():
   global l_delay
   global l_click_thread
   time.sleep(1)
   l_delay=1
   l_click_thread= threading.Thread(target=l_click_delay)



while True:
    success, img = cap.read()
    img = cv2.flip(img,1)

    hands, img = detector.findHands(img, flipType=False)
    cv2.rectangle(img,(frame,frame),(alien_w-frame,alien_h-frame),(255,0,255),2)
    if hands:
        lmList = hands[0]['lmList']
        ind_x, ind_y = lmList[8][0], lmList[8][1]
        mid_x,mid_y= lmList[12][0],lmList[12][1]
        thb_x,thb_y= lmList[4][0],lmList[4][1]


        cv2.circle(img,(ind_x, ind_y),5,(0,255,255),2)
        fingers = detector.fingersUp(hands[0])
    
#mouse movement intergration into x and y corodinate, note that both ind_ 7 ind_y were intergrated into a turple which was later intergrated into 2 more turples ; alien_x & alien_y
        if fingers[1] == 1 and fingers[2]==0 and fingers[0]==1:
         alien_x = int(np.interp(ind_x,(frame,alien_w-frame),(0,1366)))
         alien_y = int(np.interp(ind_y,(frame,alien_h-frame),(0,768)))
         mouse.move(alien_x,alien_y)

#mouse left click button
        if fingers[1]==1 and fingers[2]==1:
           if abs(ind_x - mid_x) < 40:
              if l_delay ==1:
                 mouse.click(button='left')
                 l_delay = 0

        if fingers[1]==1 and fingers[0]==1:
         if abs(ind_x - thb_x) < 40:
            if l_delay ==1:
               mouse.click(button='right')
            l_delay = 0
                 
                 

    cv2.imshow('Camera Feed', img)
    cv2.waitKey(1)