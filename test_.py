import numpy as np
import cv2
import time

def test_color(img, minPixel, minPixelW):
    
    thrMinGreen = np.array([36,87,103])
    thrMaxGreen = np.array([113,113,142])
    thrMinRed = np.array([4,162,99])
    thrMaxRed = np.array([154,200,156])
    thrMinWhite = np.array([0,0,0]) #Need These Values
    thrMaxWhite = np.array([100,100,100]) #Need These Values
    
    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
	
    maskGreen = cv2.inRange(yuv, thrMinGreen, thrMaxGreen)
    maskRed = cv2.inRange(yuv, thrMinRed, thrMaxRed)
    maskWhite = cv2.inRange(yuv, thrMinWhite, thrMaxWhite)
	
    countGreen = cv2.countNonZero(maskGreen)
    countRed = cv2.countNonZero(maskRed)
    countWhite = cv2.countNonZero(maskWhite)
    #print "Green: " + countGreen
    #print "Red: " + countRed
    #print "White: " + countWhite
	
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
		
cap = cv2.VideoCapture(0)
for x in xrange(30):
    _, frame = cap.read()
_, frame = cap.read()
min_pixel = 1000
min_pixel_w = 1000
color = test_color(frame, min_pixel, min_pixel_w)
print color
cap.release()
