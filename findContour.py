# -*- coding: UTF-8 -*-
import numpy as np
import cv2

vs = cv2.VideoCapture(0)
vs.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
vs.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)


# 迴圈取得影像幀
while (vs.isOpened()):
    ret, frame = vs.read()
    dst = cv2.pyrMeanShiftFiltering(frame, 10, 50)#濾波
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)#灰度
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)#二值化
    #cv2.imshow("ShiftFiltering", dst)#顯示濾波
    #cv2.imshow("threshold", thresh)#顯示二值化
    cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#找輪廓
    print(len(cnts))    
    for i in cnts:
        peri = cv2.arcLength(i, True)#輪廓近似，清除斜邊上小又多的輪廓
        approx = cv2.approxPolyDP(i, 0.01*peri, True)# 計算輪廓線條量
        # print(approx)
        if len(approx) == 7:
            start_point = (approx[0][0][0], approx[0][0][1])
            end_point = (approx[3][0][0], approx[3][0][1])
            color = (255, 0, 0)#框框顏色
            frame = cv2.rectangle(frame, start_point, end_point, color, 2)#畫正方形標出來    
    cv2.imshow("result", frame)#顯示結果
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break