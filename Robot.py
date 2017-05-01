import cv2
from redbird import Utilities
import numpy as np
import time

             
class Robot():

#_______________________________________________________#
    #INITIALIZERS
#---------------------------------------------------#

    def __init__(self, number):
        self.n = number
        self.lostNum = 0
        self.color = "Unknown"
        self.type = "Unknown"
        self.coords = [[0,0,0,0]]
        self.vector = [0,0]
        #self.uuid =
        return

#_______________________________________________________#
    #LOST NUMBER METHODS
#---------------------------------------------------#
    def setLostNum(self, lostNum):
        self.lostNum = lostNum
        return 

    def incLostNum(self):
        self.lostNum = self.lostNum + 1
        return

    def checkLostNum(self, threshold):
        if self.lostNum == threshold:
            print "kicked"
            self.ROI = None
            self.lostNum = 0
        return

#_______________________________________________________#
    #COORDINATE / ROI METHODS
#---------------------------------------------------#
    def setCoords(self, new_coords):        
        old_coords = np.asarray(self.coords)
        numRows = old_coords.shape
        row = (numRows[0] - 1)
        #if old coords and new coords are not equal
        if not (np.array_equal(old_coords[row,:], new_coords)):
            self.coords = np.vstack((old_coords, new_coords))
        return

    def setROI(self, image, coords, pad):
##        print "ROI COORDS"
##        print coords
        if not np.all(coords == 0):
            x = int(coords[0])
            y = int(coords[1])
            w = int(coords[2])
            h = int(coords[3])
            self.ROI = image[y:y+h+pad, x:x+w+pad] 
##            cv2.imshow("ROI", self.ROI)
##            time.sleep(15)
##        print "ROI"
##        print self.ROI
        return


#_______________________________________________________#
    #VECTOR / LOGIC METHODS
#---------------------------------------------------#
    def getValues(self):
        coords = np.asarray(self.coords)
        shape = coords.shape
        row = (shape[0] - 1)
        set1 = coords[row,:]
        


#_______________________________________________________#
    #OTHER
#---------------------------------------------------#
    def setColor(self, Color):
        self.color = Color
        return
    
    def setType(self, botType):
        self.type = botType
        return
