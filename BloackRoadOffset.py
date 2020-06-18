# -*- coding: UTF-8 -*-
import cv2
import numpy as np
from car import Car

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
center = 320

car = Car('/dev/ttyACM0', 9600)
print('start')

while(True):
  try:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU) # 大津演算法二值化 
    kernel = np.ones((5,5),np.uint8)                           # 宣告5*5的卷積核
    dst = cv2.erode(dst,kernel,iterations=1)                   # 腐蝕 清除白色雜訊
    dst = cv2.dilate(dst, kernel, iterations=1)                # 膨脹 加強白色區域
    color = dst[400]                                           # 以橫像素座標400為判定基準
    cv2.line(frame, (0, 400), (640, 400), (0, 0, 255), 5)      # 測試用，在像素400行畫一條，讓你們知道判定是落在哪落在哪
    black_count = np.sum(color == 0)   # 找到黑色的像素點個數
    black_index = np.where(color == 0) # 找到黑色的像素點索引
    if black_count == 0:
  	   black_index = np.array([[0], [0]])
  	   black_count = 1
    # 找到黑色像素的中心點位置 
    center = (black_index[0][black_count - 1] + black_index[0][0]) / 2
    # 計算出center与标准中心点的偏移量 
    direction = center - 320
    print('off={}'.format(direction), end=' ') # 列出偏移值
    # 顯示圖片
    cv2.imshow('g', dst)
  except:
    car.stop()
    break

  speed = 65
  # > right, < left 
  if direction > 10:
  	# car.go_right(100)
  	print("right")
  elif direction < -10:
  	# car.go_left(100)
  	print("left")
  else:
  	# car.go_forward(speed)
  	print("forward")

car.stop()
print('stop')
# 釋放攝影機
cap.release()

# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()