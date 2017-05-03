import cv2
import numpy as np
import time

camera = cv2.VideoCapture(0)
if (camera.isOpened()): 
    print("Camera Opened Successfully.")
    def get_image(): 
        retval, im = camera.read()
        return im
    time.sleep(1)
    image = get_image()
    cv2.imwrite('test.png', image)
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    del(camera)
    img = cv2.imread('test.png')
    img_cvt = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    ALL_MIN = np.array([0,0,0]) # HSV 0,0,0 -> 0, 0, 0
    ALL_MAX = np.array([180,255,255]) # HSV 360,100,100 -> 180, 255, 255
    dst_all = cv2.inRange(img_cvt, ALL_MIN, ALL_MAX)
    no_all = cv2.countNonZero(dst_all)
    RED_MIN_1 = np.array([0,179,26]) # HSV 0, 70, 10 -> 0, 179, 26
    RED_MAX_1 = np.array([6,255,255]) # HSV 11, 100, 100 -> 6, 255, 255
    dst_red_1 = cv2.inRange(img_cvt, RED_MIN_1, RED_MAX_1)
    no_red_1 = cv2.countNonZero(dst_red_1)
    RED_MIN_2 = np.array([175,179,26]) # HSV 351, 70, 10 -> 0, 179, 26
    RED_MAX_2 = np.array([180,255,255]) # HSV 360, 100, 100 -> 180, 255, 255
    dst_red_2 = cv2.inRange(img_cvt, RED_MIN_2, RED_MAX_2)
    no_red_2 = cv2.countNonZero(dst_red_2)
    no_red = no_red_1 + no_red_2
    GREEN_MIN = np.array([32,38,26]) #HSV 64, 15, 10 -> 32, 38, 26
    GREEN_MAX = np.array([76,255,255]) #HSV 150, 100, 100 -> 76, 255, 255
    dst_green = cv2.inRange(img_cvt, GREEN_MIN, GREEN_MAX)
    no_green = cv2.countNonZero(dst_green)
    print('Total pixels: ' + str(no_all))
    print('Red pixels: ' + str(no_red))
    print('Green pixels: ' + str(no_green))
    img_red_1 = cv2.bitwise_and(img, img, mask=dst_red_1)
    img_red_2 = cv2.bitwise_and(img, img, mask=dst_red_2)
    img_green = cv2.bitwise_and(img, img, mask=dst_green)
    img_red = img_red_1 + img_red_2
    cv2.imshow('Original', img)
    cv2.imshow('Red1', img_red_1)
    cv2.imshow('Red2', img_red_2)
    cv2.imshow('Red', img_red)
    cv2.imshow('Green', img_green)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if no_red > 25000 and no_red > no_green * 10:
        print("Red Object Found")
    elif no_green > 25000 and no_green > no_red * 10:
        print("Green Object Found")
    else:
	    print("No Object Found")
else: 
    print("Camera Failed To Open.")