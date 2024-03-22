import cv2
import signal
import sys

import imagezmq


# 使用OpenCV捕捉视频流
# 对于树莓派摄像头，通常使用0（或-1），如果有多个摄像头，可能需要尝试1、2等。
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("打开摄像头失败！")
    exit()
else:
    print("摄像头成功打开")


while True:
    # 逐帧捕获
    ret, frame = cap.read()
    print("读取状态：", ret)
    # 如果正确读取帧，ret为True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # 将帧显示在窗口中
    # cv2.imshow('frame', frame)
    cv2.imwrite('./src/caption.jpg', frame)
 

# 释放摄像头
cap.release()
cv2.destroyAllWindows()


# sender = imagezmq.ImageSender(connect_to="tcp://172.20.10.5:5555")
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to capture image")
#         break
#     sender.send_image("Raspberry Pi Camera", frame)
