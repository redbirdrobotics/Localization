import cv2
import numpy as np
import time
from redbird import Robot
from redbird import Utilities
from redbird import Camera

#INITIALIZERS

#CAMERAS
cam0 = Camera(0, (1280, 720), 60, (130, 90), (0, 45))
cam0.create_angleAxis()
##cam1 = Camera(1, (1280, 720), 60, (130, 90), (120, 45))
##cam1.create_angleAxis()
##cam2 = Camera(2, (1280, 720), 60, (130, 90), (240, 45))
##cam2.create_angleAxis()

#ROBOTS
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

#DETECTORS

#HAAR
#eye_cascade = cv2.CascadeClassifier('C:\Users\Alex\Desktop\Robotics\Cascades\haarcascade_frontalface_alt.xml')
#eye_cascade = cv2.CascadeClassifier('C:\Users\Alex\Desktop\Robotics\Cascades\top_plate_stg2.xml')
eye_cascade = cv2.CascadeClassifier('C:\Users\Alex\Desktop\Robotics\Cascades\haarcascade_eye.xml')
cascadeList = [eye_cascade]

#BLOB
robotParams = cv2.SimpleBlobDetector_Params()
Utilities.get_Parameters(robotParams, 0)
groundRobot = cv2.SimpleBlobDetector_create(robotParams)
blobList = [groundRobot]

#GLOBAL VARIABLES

#Array that holds the current positions of detected objects
cur_pos = np.zeros((14,4), dtype=int)

#Loop Condition
foundBot = 0


#While location of all robots is not known look for unfound robots and track found robots
while not (foundBot == 13):
    
    #Get newest frame from camera
    #Create list of Robots whos location was known in last frame
    #Search all regions where a Robot was last seen.  Maximum of 3 frames may pass before Robot is considered lost
    #Remove each rectangle containing located robots
    frame = cam0.getFrame()
    working_frame = frame.copy()    
    foundList = Utilities.getAll_takenRows(cur_pos)
    Robot.searchAll_ROI(roboList, cur_pos, foundList, eye_cascade, 3)
    image_wtxt = Utilities.label_ROI(working_frame, cur_pos)    
    working_frame = Utilities.removeAll_Rect(working_frame, cur_pos)

    #Escape, press ESC
    esc = cam0.showFrame(working_frame, "cam0")
    if esc == True:
        break
    
    #Look for new robot & store rectangle that contains robot in variable "robot"
    #Look for open row in current position matrix to store coordinates
    #Store location rectangle in current position matrix
    #Assign current coordinates and ROIs to all robot objects
    #update current position of found robots
    robot = Utilities.getAll_Loc(eye_cascade, working_frame)    
    foundBot = Utilities.get_openRow(cur_pos)      
    Utilities.replace_Rows(cur_pos, robot, foundBot)
    print cur_pos
    Robot.syncAll_Bots(roboList, cur_pos, frame, 25)

cam0.detach()
cv2.destroyAllWindows()   

