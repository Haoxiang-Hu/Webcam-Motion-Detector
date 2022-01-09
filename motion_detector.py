import cv2

video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #把frame转化为一个图片
    cv2.imshow("Capturing", gray) #打开一个窗口显示捕获的画面，每次使用imshow都需要记得下面需要一个destroyAllWindows()关闭窗口

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()