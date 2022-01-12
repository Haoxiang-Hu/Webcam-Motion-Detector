import cv2
import time
from datetime import datetime

first_frame = None
status_list = []
times = []

video = cv2.VideoCapture(0)

#Turn on the camera for few seconds.
i=100
while i>0:
    i = i-1
    check, frame_1 = video.read()

while True:
    check, frame = video.read()
    status = 0
    gray =cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #把frame转化为一个图片
    gray =cv2.GaussianBlur(gray,(21,21),0)

    if first_frame is None:
        first_frame = gray
        continue

    #Add frames
    delta_frame = cv2.absdiff(first_frame,gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    #Contour Method
    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue

        status = 1

        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)

    status_list.append(status)

    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 1 and status_list[-2] == 1:
        times.append(datetime.now())

    cv2.imshow("First Frame", first_frame)
    cv2.imshow("Gray Frame", gray) #打开一个窗口显示捕获的画面，每次使用imshow都需要记得下面需要一个destroyAllWindows()关闭窗口
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

print(status_list)
print(times)

video.release()  

cv2.destroyAllWindows()