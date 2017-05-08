import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(1)


img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('slider_l')
cv2.namedWindow('slider_u')

cv2.createTrackbar('Y_l','slider_l',0,255,nothing)
cv2.createTrackbar('U_l','slider_l',0,255,nothing)
cv2.createTrackbar('V_l','slider_l',0,255,nothing)

cv2.createTrackbar('Y_u','slider_u',0,255,nothing)
cv2.createTrackbar('U_u','slider_u',0,255,nothing)
cv2.createTrackbar('V_u','slider_u',0,255,nothing)


switch = '0: OFF \n1 :ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)

while(1):
    _, frame = cap.read()
    yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    cv2.imshow('slider_l', img)
    cv2.imshow('slider_u', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break


    y_l = cv2.getTrackbarPos('Y_l','slider_l')
    u_l = cv2.getTrackbarPos('U_l','slider_l')
    v_l = cv2.getTrackbarPos('V_l','slider_l')

    y_u = cv2.getTrackbarPos('Y_u','slider_u')
    u_u = cv2.getTrackbarPos('U_u','slider_u')
    v_u = cv2.getTrackbarPos('V_u','slider_u')
    
    s = cv2.getTrackbarPos(switch,'slider_l')

    low = np.array([y_l,u_l,v_l])
    up = np.array([y_u,u_u,v_u])

    mask = cv2.inRange(yuv, low, up)
    res = cv2.bitwise_and(frame, frame, mask = mask)

    cv2.imshow('res', res)

cv2.destroyAllWindows()
cap.release()
