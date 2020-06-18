# -*- coding: UTF-8 -*-
import numpy as np
import cv2
from car import Car

vs = cv2.VideoCapture(0)
vs.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
vs.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

car = Car('/dev/ttyACM0', 9600)

FORWARD = 1
LEFT    = 2
RIGHT   = 3

now_state = FORWARD

# 迴圈取得影像幀
while (vs.isOpened()):
    ret, frame = vs.read()
    dst = cv2.pyrMeanShiftFiltering(frame, 10, 50)                 # 濾波
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)                   # 灰度
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY) # 二值化
    # print(ret)
    # cv2.imshow("ShiftFiltering", dst) # 顯示濾波
    # cv2.imshow("threshold", thresh)   # 顯示二值化
    # canny_output = cv2.Canny(gray, ret, ret * 2)
    # cv2.imshow("canny", canny_output)
    find_countour_input = thresh
    # 找輪廓
    cnts, hierarchy = cv2.findContours(find_countour_input, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # init state
    now_state = FORWARD

    print('-'*30)
    for i in cnts:
        peri = cv2.arcLength(i, True)                 # 輪廓近似，清除斜邊上小又多的輪廓
        approx = cv2.approxPolyDP(i, 0.05*peri, True) # 計算輪廓線條量
        # print(len(approx))
        x, y, w, h = cv2.boundingRect(approx)
        start_point = (x, y)
        end_point = (x+w, y+h)
        # six
        if len(approx) == 6:
            color = (255, 0, 0)
            # frame = cv2.rectangle(frame, start_point, end_point, color, 2)
            #
            now_state = LEFT
        # star
        elif len(approx) == 10:
            color = (0, 255, 0)
            # frame = cv2.rectangle(frame, start_point, end_point, color, 2)
            now_state = RIGHT

    if now_state == LEFT:
        print('six: left')
        car.go_left(90)
    elif now_state == RIGHT:
        print('star: right')
        car.go_right(90)
    else:
        print('none: forward')
        car.go_forward(70)

    # cv2.imshow("result", frame) # 顯示結果

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
