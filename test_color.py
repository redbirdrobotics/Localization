import numpy as np
import cv2
import time

green = False
red = False

def test_color(img, threshold_min, threshold_max, min_pixel):
    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

    mask = cv2.inRange(yuv, threshold_min, threshold_max)
    #res = cv2.bitwise_and(img, img, mask = mask)
    
    #array = np.asarray(mask)
    #count = np.count_nonzero(array)
    count = cv2.countNonZero(mask)

    print count
    
    if(count > min_pixel):
        return True
    else:
        return False



cap = cv2.VideoCapture(1)

# Discard the first 30 frames so the camera can properly startup
for x in xrange(30):
    _, frame = cap.read()

# Grab the frame a final time
_, frame = cap.read()

min_pixel = 1000

thresh_min1 = np.array([36,87,103])
thresh_max1 = np.array([113,113,142])
green = test_color(frame, thresh_min1, thresh_max1, min_pixel)

thresh_min2 = np.array([4,162,99])
thresh_max2 = np.array([154,200,156])
red = test_color(frame, thresh_min2, thresh_max2, min_pixel)

print "GREEN:" + str(green)
print "RED:" + str(red)

cap.release()




#red min(175,70,26)
#red max(180,255,255)

#red2 min(0,70,26)
#red2 max(6,255,255)

#green min(50,70,26)
#green max(76,255,255)
