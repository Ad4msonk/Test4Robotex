import cv2
import numpy as np
import os


#file for trackbars
try:
    file = open('trackbar_values.txt', 'r')
    rl = int(file.readline())
    gl = int(file.readline())
    bl = int(file.readline())
    ru = int(file.readline())
    gu = int(file.readline())
    bu = int(file.readline())
    file.close()

except IOError:
    rl = gl = bl = ru = gu = bu = 0
    file = open('trackbar_values.txt', 'w+')
    file.write(str(rl) + "\n" + str(gl) + "\n" + str(bl) + "\n" +
               str(ru) + "\n" + str(gu) + "\n" + str(bu) + "\n")
    file.close()



cap = cv2.VideoCapture(1)

def nothing(x):
    pass

# Create a black image, a window
#img = np.zeros((200, 512, 3), np.uint8)
cv2.namedWindow('image', flags=cv2.WINDOW_NORMAL)
#cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('RLower', 'image', rl, 255, nothing)
cv2.createTrackbar('GLower', 'image', gl, 255, nothing)
cv2.createTrackbar('BLower', 'image', bl, 255, nothing)
cv2.createTrackbar('RUpper', 'image', ru, 255, nothing)
cv2.createTrackbar('GUpper', 'image', gu, 255, nothing)
cv2.createTrackbar('BUpper', 'image', bu, 255, nothing)


while (1):
    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # get current positions of four trackbars
    rl = cv2.getTrackbarPos('RLower', 'image')
    gl = cv2.getTrackbarPos('GLower', 'image')
    bl = cv2.getTrackbarPos('BLower', 'image')
    ru = cv2.getTrackbarPos('RUpper', 'image')
    gu = cv2.getTrackbarPos('GUpper', 'image')
    bu = cv2.getTrackbarPos('BUpper', 'image')

    # define range of blue color in HSV
    #lower_blue = np.array([110, 50, 50])
    #upper_blue = np.array([130,255,255])
    lower = np.array([rl, gl, bl])
    upper = np.array([ru, gu, bu])

    # Threshold the HSV image to get only expected color
    mask = cv2.inRange(hsv, lower, upper)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    #finding and drawing contours
    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if (len(contours) > 10):    # esimene frame voib olla tyhi(nagu ka moni muu)

        cnt = contours[0]
        M = cv2.moments(cnt)
        #print M
        #cx = int(M['m10'] / M['m00'])
        #cy = int(M['m01'] / M['m00'])
        #epsilon = 0.1 * cv2.arcLength(cnt, True)
        #approx = cv2.approxPolyDP(cnt, epsilon, True)
        kernel = np.ones((5, 5), np.uint8)
        closing = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)

        cv2.drawContours(frame, contours, 3, (0, 255, 0), 3)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask) #black'n'white
    cv2.imshow('res', res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        file = open('trackbar_values.txt', 'w')
        file.write(str(rl) + "\n" + str(gl) + "\n" + str(bl) + "\n" +
                   str(ru) + "\n" + str(gu) + "\n" + str(bu) + "\n")
        file.close()
        break

cv2.destroyAllWindows()