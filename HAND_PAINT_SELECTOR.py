import cv2
import os
import numpy as np
import HandTrackingModule as htm
#######################
brushThickness = 15
eraserThickness = 200
########################
########## THIS PROGRAM ONLU WORK WITH 720P CAMERA DUE TO RESOLUTION ISSUES
folderPath = 'K:/PROGRAMS/PYTHON/HAND_TRACKING/HEADER'
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0]

drawColor = (255, 0, 255)

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.65,maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    success, img = cap.read()
    # frame = cv2.resize(frame, (1280, 720))
    img = cv2.flip(img, 1)

    # Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # print(lmList)
        # tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)

        # If Selection Mode – Two finger are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print('Selection Mode')
            # Checking for the click
            if y1 < 200:
                if 20 < x1 < 250:
                    header = overlayList[0]
                    drawColor = (0, 0, 0)
                elif 400 < x1 < 600:
                    header = overlayList[1]
                    drawColor = (0, 0, 255)
                elif 680 < x1 < 880:
                    header = overlayList[2]
                    drawColor = (0, 128, 0)
                elif 920 < x1 < 1120:
                    header = overlayList[3]
                    drawColor = (255, 0, 0)
            cv2.rectangle(img,(x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # If Drawing Mode – Index finger is up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print('Drawing Mode')
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

        xp, yp = x1, y1

        # Clear Canvas when all fingers are up
        # if all (x >= 1 for x in fingers):
        #     imgCanvas = np.zeros((720, 1280, 3), np.uint8)

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)

    # Setting the header image
    img[0:184, 0:1280] = header
    
    # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow('Image', img)
    cv2.imshow('Canvas', imgCanvas)
    # cv2.imshow('Inv', imgInv)
    # cv2.waitKey(1)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()