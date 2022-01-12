import cv2, time, pandas
from datetime import datetime

first_frame = None #First frame, like a reference.
status_list = [None,None] #Add status list, two "None" to make sure the following if loop will not out of index
times = [] #Time list
video = cv2.VideoCapture(0)
df = pandas.DataFrame(columns=["Start","End"]) #The csv file frame structure

#Turn on the camera for few seconds. Warm up the camera. Macbook system has is issue. 
i=100
while i>0:
    i = i-1
    check, frame_1 = video.read()

while True: #While loop makes every frames coherent
    check, frame = video.read()
    status = 0
    gray =cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Transfer frame to a gray color base picture
    gray =cv2.GaussianBlur(gray,(21,21),0)

    if first_frame is None:
        first_frame = gray
        continue

    #Add delta_frame and thresh_frame
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
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    #Crate a camera window.
    #Remanber! every time after use imshow(), we need a destroyAllWindows() to close all windows.
    #Whatever how many imshow() used, just need one destroyAllWindows() to close all windows
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1) 

    if key == ord('q'):
        if status == 1: #if quit when the object is detected, it still has a quit time.
            times.append(datetime.now())
        break

print(status_list)
print(times)

for i in range(0, len(times), 2):  #Range is from 0 to the length of the times[], step is 2.
    df = df.append({"Start" : times[i], "End" : times[i+1]}, ignore_index = True) #Put i value in start column, put i+1 value in end column

df.to_csv("Times.csv") #Export the data frame to a csv file

video.release()  

cv2.destroyAllWindows()