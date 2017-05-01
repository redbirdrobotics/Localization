import cv2
import numpy as np
import time
from redbird import Robot
from redbird import Utilities

#GLOBALS
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('C:\Users\Alex\Desktop\Robotics\Cascades\haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier('C:\Users\Alex\Desktop\Robotics\Cascades\haarcascade_eye.xml')
cur_pos = np.zeros((14,4)) #Array that holds the current positions of detected objects
Marky = Robot(1)
Ricky = Robot(2)
Danny = Robot(3)
Terry = Robot(4)
Mikey = Robot(5)
Davey = Robot(6)
Timmy = Robot(7)
Tommy = Robot(8)
Joey = Robot(9)
Robby = Robot(10)
Johnny = Robot(11)
Brian = Robot(12)
Willy = Robot(13)
Benny = Robot(14)
roboList = [Marky, Ricky, Danny, Terry, Mikey, Davey, Timmy, Tommy, Joey, Robby, Johnny, Brian, Willy, Benny]
foundBot = 0
#tester = np.array([[200,200,50,50],[100,100,50,50],[300,300,50,50],[300,100,50,50],[200,50,50,50],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

#Hybrid Methods

def syncAll_Bots(image ,pad):
    lgth = len(roboList)
    for i in range(lgth):
        roboList[i].setCoords(cur_pos[i,:])
        roboList[i].setROI(image, cur_pos[i,:], pad)
    return

def searchAll_ROI(list_found, cascade, threshold):
    if not (list_found == () ):
        lgth = len(list_found)
        for i in range(lgth):
            bot = list_found[i]
            ROI = roboList[bot].ROI
            #These are coordinates relative to resolution of camera
            true_coords = cur_pos[bot,:]
            #These are coordinates relative to ROI
            rel_coords = Utilities.get_Loc(cascade, ROI)
            if not np.all(rel_coords == 0):
                x = true_coords[0]
                y = true_coords[1]
                rx = rel_coords[0]
                ry = rel_coords[1]
                rw = rel_coords[2]
                rh = rel_coords[3]
                new_Loc = [x+rx, y+ry, rw, rh]
                cur_pos[bot,:] = new_Loc
                #cv2.imshow("found", ROI)
            else:
                #cv2.imshow("kicked", ROI)
                #cur_pos[bot,:] = [0,0,0,0]
                #Get a number for how many frames object has been missing from and increment
                roboList[bot].incLostNum()
                #If that number is greater than "threshold" set position to [0,0,0,0]
                cur_pos[bot,:] = Utilities.compare_Equals(true_coords, roboList[bot].lostNum, threshold)
                #set missing frame number to 0 if it is equal to threshold
                roboList[bot].checkLostNum(threshold)
    return

#While location of all robots is not known look for unfound robots and track found robots
while not (foundBot == 13):
    #Get newest frame from camera
    frame = Utilities.get_Frame(cap)
    working_frame = frame.copy()
    #Create list of addresses for Robots whos location was known in last frame
    foundList = Utilities.getAll_takenRows(cur_pos)
    #Search all regions where a Robot was last seen.  Maximum of 3 frames may pass before Robot is considered lost
    searchAll_ROI(foundList, eye_cascade, 3)
    image_wtxt = Utilities.label_ROI(working_frame, cur_pos)
    #Remove location of all located robots
    working_frame = Utilities.removeAll_Rect(working_frame, cur_pos)
    #showing_frame = Utilities.drawAll_Rect(frame, cur_pos)
    cv2.imshow('img', working_frame)
    #Look for new robot & store rectangle that contains robot in variable "eye"
    eye = Utilities.getAll_Loc(eye_cascade, working_frame)
    #Look for open row in current position matrix to store coordinates
    foundBot = Utilities.get_openRow(cur_pos)  
    #Store location rectangle in current position matrix
    Utilities.replace_Rows(cur_pos, eye, foundBot)
    print cur_pos
    #Assign current coordinates and ROIs to all robot objects
    syncAll_Bots(frame, 25)
    #ESC
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    #update current position of found robots

#while emptyBot == 14:
    #Update locations
cap.release()
cv2.destroyAllWindows()   

