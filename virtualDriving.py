import cv2
import numpy as np
import pyautogui as pag

cap=cv2.VideoCapture(0)
cap.set(3,1200)
cap.set(4,600)
cap.set(10,100)

left_line=320
right_line=640
color_matrix=[[0,20,127,255,139,255], #orange
              [27,179,0,255,0,97]]  #darkBlue
k = 0

while True:
    success,imgWebcam=cap.read()
    hT,wT,cT=imgWebcam.shape
    imgHSV=cv2.cvtColor(imgWebcam,cv2.COLOR_BGR2HSV)
    cv2.rectangle(imgWebcam,(0,0),(370,270),(0,0,255),2)
    cv2.putText(imgWebcam,"RIGHT",(220,30),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)
    cv2.rectangle(imgWebcam,(590,0),(wT,270),(0,0,255),2)
    cv2.putText(imgWebcam,"LEFT",(650,30),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)
    cv2.rectangle(imgWebcam,(0,270),(wT,370),(0,0,255),2)
    cv2.putText(imgWebcam,"UP",(0,300),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)
    cv2.rectangle(imgWebcam,(0,420),(wT,hT),(0,0,255),2)
    cv2.putText(imgWebcam,"DOWN",(0,470),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)
    lower = np.array([color_matrix[k][0], color_matrix[k][2], color_matrix[k][4]])
    upper = np.array([color_matrix[k][1], color_matrix[k][3], color_matrix[k][5]])
    mask = cv2.inRange(imgHSV, lower, upper)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    centers=[]
    for cnt in contours:
        if cv2.contourArea(cnt)>500:
            # cv2.drawContours(imgWebcam,cnt,-1,(255,0,255),3)
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
            x,y,w,h=cv2.boundingRect(approx)
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(imgWebcam, (cX, cY), 7, (0, 255, 0), -1)
            centers.append([cX,cY])
    if(len(centers)==2):
        up=[]
        down=[]
        if centers[0][1]<centers[1][1]:
            up.append(centers[0])
            down.append(centers[1])
        else:
            down.append(centers[0])
            up.append(centers[1])
        # print(up)
        # print(down)
        if up[0][1]<270 and up[0][0] > 590:
            print('LEFT')
            pag.keyDown('left')
        else:
            pag.keyUp('left')
        if up[0][1]<270 and up[0][0] < 370:
            print("Right")
            pag.keyDown('right')
        else:
            pag.keyUp('right')
        if 270<down[0][1]<370:
            print("up")
            pag.keyDown('up')
        else:
            pag.keyUp('up')
        if 420<down[0][1]<hT:
            print("down")
            pag.keyDown('down')
        else:
            pag.keyUp('down')

    cv2.imshow("Webcam",imgWebcam)
    # cv2.imshow("HSV",imgHSV)
    # cv2.imshow("Mask",mask)
    cv2.waitKey(1)
