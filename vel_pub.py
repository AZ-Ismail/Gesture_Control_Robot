# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 15:33:05 2022

@author: User
"""
from cProfile import label
import rospy
import cv2
import numpy as np
import HandTrackingModule as htm
import time
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16

rospy.init_node("vel_pub")
pub=rospy.Publisher("/cmd_vel",Twist,queue_size=10)
rate=rospy.Rate(1000000)
cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.7)
pTime = 0
while not rospy.is_shutdown():
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) > 0:
        
        lmlist[0][1]
        middle=300
        if lmlist[0][1] > middle:
            x1, y1 = lmlist[4][1], lmlist[4][2]
            x2, y2 = lmlist[8][1], lmlist[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(img, (x1, y1), 5, (0, 215, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 5, (0, 215, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), 5, (0, 215, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 215, 255), 3)
            length = math.hypot(x2 - x1, y2 - y2)
            speedx=np.interp(length,[35,200],[0,1])
            twist=Twist()
            twist.linear.x=speedx
            pub.publish(twist)
            if length < 35:
                cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
            if length > 200:
                cv2.circle(img, (cx, cy), 15, (255, 127, 80), cv2.FILLED)
            rate.sleep()
        if lmlist[0][1] < middle:
            x3, y3 = lmlist[4][1], lmlist[4][2]
            x4, y4 = lmlist[8][1], lmlist[8][2]
            cx, cy = (x3 + x4) // 2, (y3 + y4) // 2
            cv2.circle(img, (x3, y3), 5, (255, 215, 0), cv2.FILLED)
            cv2.circle(img, (x4, y4), 5, (255, 215, 0), cv2.FILLED)
            cv2.circle(img, (cx, cy), 5, (255, 215, 0), cv2.FILLED)
            cv2.line(img, (x3, y3), (x4, y4), (255, 215, 0), 3)
            
            length = math.hypot(x4 - x3, y4 - y3)
            
            speedz=np.interp(length,[35,200],[0,1])
            twist=Twist()
            twist.angular.z=speedz
            pub.publish(twist)
            if length < 35:
                cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
            if length > 200:
                cv2.circle(img, (cx, cy), 15, (255, 127, 80), cv2.FILLED)
            rate.sleep()
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
    cv2.imshow("Img", img)
    cv2.waitKey(1)