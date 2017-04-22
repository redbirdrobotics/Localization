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
roboList = [Marky, Ricky, Danny, Terry, Mikey, Davey]
emptyBot = 0
#tester = np.array([[200,200,50,50],[100,100,50,50],[300,300,50,50],[300,100,50,50],[200,50,50,50],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])


#While location of all robots is not known look for unfound robots and track found robots
while emptyBot != 14:
    #Get newest frame from camera
    frame = Utilities.get_Frame(cap)
    #Create list of addresses for Robots whos location was known in last frame
    foundList = Utilities.getAll_takenRows(cur_pos)
    
    #Remove location of all located robots
    newframe = Utilities.removeAll_Rect(frame, cur_pos) 
    #cv2.imshow('img',newframe)
    #Look for new robot & store rectangle that contains robot in variable "eye"
    eye = Utilities.getAll_Loc(eye_cascade, newframe)
    #Look for open row in current position matrix to store coordinates
    emptyBot = Utilities.get_openRow(cur_pos)
    print emptyBot
    #Assign coordinates to specific robot object
    roboList[emptyBot].setCoords(eye)
    
    #Store location rectangle in current position matrix
    Utilities.replace_Rows(cur_pos, eye, emptyBot)
    #ESC
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    #update current position of found robots

#while emptyBot == 14:
    #Update locations
cap.release()
cv2.destroyAllWindows()   

