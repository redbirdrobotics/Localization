import numpy as np
import cv2
import time

def getBotColorUsingHSV(img, minPixel, minPixelW):
    
    thrMinGreen = np.array([32,38,26])
    thrMaxGreen = np.array([76,255,255])
    thrMinRed1 = np.array([0,179,26])
    thrMaxRed1 = np.array([6,255,255])
    thrMinRed2 = np.array([175,179,26])
    thrMaxRed2 = np.array([180,255,255])
    thrMinWhite = np.array([0,0,200]) 
    thrMaxWhite = np.array([180,255,255]) 
    
    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	
    maskGreen = cv2.inRange(yuv, thrMinGreen, thrMaxGreen)
    maskRed1 = cv2.inRange(yuv, thrMinRed1, thrMaxRed1)
    maskRed2 = cv2.inRange(yuv, thrMinRed2, thrMaxRed2)
    maskWhite = cv2.inRange(yuv, thrMinWhite, thrMaxWhite)
	
    countGreen = cv2.countNonZero(maskGreen)
    countRed1 = cv2.countNonZero(maskRed1)
    countRed2 = cv2.countNonZero(maskRed2)
    countRed = countRed1 + countRed2
    countWhite = cv2.countNonZero(maskWhite)
    
    print "Green: " + str(countGreen)
    print "Red: " + str(countRed)
    print "White: " + str(countWhite)
	
    if countGreen >= minPixel and countRed >= minPixel:
        return "conflict"
    elif countGreen >= minPixel:
        return "green"
    elif countRed >= minPixel:
        return "red"
    elif countWhite >= minPixelW:
        return "white"
    else:
        return "none"

def getGrayscaleImage(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def getRedImageUsingHSV(img):
    thrMinRed1 = np.array([0,179,26])
    thrMaxRed1 = np.array([6,255,255])
    thrMinRed2 = np.array([175,179,26])
    thrMaxRed2 = np.array([180,255,255])
	
    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	
    maskRed1 = cv2.inRange(yuv, thrMinRed1, thrMaxRed1)
    maskRed2 = cv2.inRange(yuv, thrMinRed2, thrMaxRed2)
	
    maskRed = maskRed1 + maskRed2
    imgRed = cv2.bitwise_and(img, img, mask = maskRed)
    
    cv2.imshow('Red', imgRed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
	
    return imgRed
	
def getGreenImageUsingHSV(img):
    thrMinGreen = np.array([32,38,26])
    thrMaxGreen = np.array([76,255,255])
	
    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	
    maskGreen = cv2.inRange(yuv, thrMinGreen, thrMaxGreen)
    maskGreen = cv2.erode(maskGreen, None, iterations=2)
    maskGreen = cv2.dilate(maskGreen, None, iterations=2)
	
    imgGreen = cv2.bitwise_and(img, img, mask = maskGreen)
    
    cv2.imshow('Green', imgGreen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
	
    return imgGreen
		
# ----- TEST CODE ----- 

frame = cv2.imread('red.png')
min_pixel = 25000
min_pixel_w = 25000
color = getBotColorUsingHSV(frame, min_pixel, min_pixel_w)
print "\nColor: " + color

im = cv2.imread("both2.png")
detector = cv2.SimpleBlobDetector_create()
im = getGrayscaleImage(getRedImageUsingHSV(im)) + getGrayscaleImage(getGreenImageUsingHSV(im))
keypoints = detector.detect(im)
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("Blobs", im_with_keypoints)
cv2.waitKey(0)