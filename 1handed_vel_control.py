# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 15:33:05 2022

@author: User
"""
import cv2
import numpy as np
import HandTrackingModule as htm
import time
import math

cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.7)
"""
cap.set(3, 1280)
cap.set(4, 720)
"""
pTime = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) > 0:
        # print(lmlist[4], lmlist[8])

        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        x3, y3 = lmlist[12][1], lmlist[12][2]
        x4, y4 = lmlist[9][1], lmlist[9][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (x1, y1), 5, (0, 215, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 5, (0, 215, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 5, (0, 215, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 5, (0, 215, 255), cv2.FILLED)
        cv2.circle(img, (x4, y4), 5, (0, 215, 255), cv2.FILLED)

        cv2.line(img, (x1, y1), (x2, y2), (0, 215, 255), 3)
        cv2.line(img, (x3, y3), (x4, y4), (0, 215, 255), 3)
        length1 = math.hypot(x2 - x1, y2 - y2)
        length2 = math.hypot(x4 - x3, y4 - y3)
        print(length2)
        if length2<100:
            if lmlist[0][1] > 300:
                #print(length1)
                if length1 < 35:
                    cv2.putText(img, "STOP ", (20, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
                    cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
                if length1 > 35:
                    cv2.putText(img, "FORWARD", (20, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
                    cv2.circle(img, (cx, cy), 15, (255, 127, 80), cv2.FILLED)
            if lmlist[0][1] < 300:
                #print(length1)
                if length1 <= 35:
                    cv2.putText(img, "STOP", (20, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
                    cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)
                if length1 > 35:
                    cv2.putText(img, "BACKWARDS ", (20, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
                    cv2.circle(img, (cx, cy), 15, (80, 127, 255), cv2.FILLED)
        if length2>130:
            if lmlist[0][2] > 300:
                #print(length1)
                if length1 < 35:
                    cv2.putText(img, "STOP ", (20, 140), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
                    cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
                if length1 > 35:
                    cv2.putText(img, "CLOCKWISE", (20, 140), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
                    cv2.circle(img, (cx, cy), 15, (255, 127, 80), cv2.FILLED)
            if lmlist[0][2] < 300:
                #print(length1)
                if length1 <= 35:
                    cv2.putText(img, "STOP", (20, 140), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
                    cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)
                if length1 > 35:
                    cv2.putText(img, "COUNTER-CLOCKWISE ", (20, 140), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
                    cv2.circle(img, (cx, cy), 15, (80, 127, 255), cv2.FILLED)

        # range 35-200
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.imshow("Img", img)

    cv2.waitKey(1)
