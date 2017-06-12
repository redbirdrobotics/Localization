import cv2
from Utilities import Utilities
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
    #ROI METHODS
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
        if not np.all(coords == 0):
            shape = self.coords.shape
            history = shape[0]
            if self.lostNum > 0:
                x,y,w,h = self.getBBOX()
                self.ROI = image[y:y+h, x:x+w]
            elif shape[0] > 1:
                x = int(coords[0])
                y = int(coords[1])
                w = int(coords[2])
                h = int(coords[3])
                self.ROI = image[y:y+h+pad, x:x+w+pad]
        return
    
    @staticmethod
    def syncAll_Bots(objectList, array, image ,pad):
        lgth = len(objectList)
        for i in range(lgth):
            objectList[i].setCoords(array[i,:])       
            objectList[i].setROI(image, array[i,:], pad)
        return

#greenMaskData and redMaskData needs to be made, maybe as init for robot?
#trying to split searchAll_ROI into separate manageable functions
#multiSearch can perform multiples searches on one ROI or just blob or just haar
#multiSearch will need to average all successful searches into single coord
#SearchAll_ROI uses multiSearch per robot and exports Relative Coords array
#A separate function Relative2Pixel converts ROI relative Coords to pixel coords
    def multiSearch(robot_inst, ):
        
        #Case 0: Search using all methods
        #Get variables
        #Make copy of ROI in grayscale for LBP detection
        #Make copy of ROI and apply mask for blob detection
        #Search for robot
        #Save coords and export
        if searchCase == 0:
            mask = robot_inst.mask
            cascadeList = robot_inst.cascades
            hsvROI = ccv2.cvtColor(robot_inst.ROI, cv2.COLOR_BGR2HSV)
            grayROI = cv2.cvtColor(robot_inst.ROI, cv2.COLOR_BGR2GRAY)
            casLen = len(cascadeList)
            relativeCoords = np.zeros((casLen, 4))
            for i in range(casLen):
                relativeCoords[i] = Utilities.get_Loc(cascadeList[i])
            for i in range(casLen, casLen + 1):
                relativeCoords[i] = robot_inst.detector.detect()
                
        return
            
    
    #Makes so that searches are callable
    @staticmethod
    def searchAll_ROI(objectList, array, list_found, cascade, threshold):
        if not (list_found == () ):
            lgth = len(list_found)
            for i in range(lgth):
                bot = list_found[i]
                
                ROI = objectList[bot].ROI
                #These are coordinates relative to resolution of camera
                true_coords = array[bot,:]
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
                    array[bot,:] = new_Loc
                    #cv2.imshow("found", ROI)
                else:
                    #Get a number for how many frames object has been missing from and increment
                    objectlist.incLostNum()                
                    #If that number is greater than "threshold" set position to [0,0,0,0]
                    array[bot,:] = Utilities.compare_Equals(true_coords, objectList[bot].lostNum, threshold)
                    #set missing frame number to 0 if it is equal to threshold
                    objectList[bot].checkLostNum(threshold)
        return

    def getScalar(self):
        num = self.lostNum
        values = np.array([1.5, 3.0, 4.5, 6.0])
        return values[num]
    
    def getNewCoords(self, scalar):
        vectors = self.getVectors()
        vectors = vectors * scalar
        coords = self.getVectCoords()
        shape = coords.shape
        columns = shape[1]
        newCoords = [0,0,0,0]
        for i in range(columns):
            newCoords[i] = int(vectors[0,i]) + coords[0,i]
        return newCoords
    
    def getBBOX(self):
        scalar = self.getScalar()
        oldCoords = self.getVectCoords()
        newCoords = self.getNewCoords(scalar)
        listCoords = np.vstack((oldCoords[0], newCoords))
        pointset = Utilities.create_PointSet(listCoords)
        BBOX = cv2.boundingRect(pointset)
        return BBOX

#_______________________________________________________#
    #VECTOR METHODS
#---------------------------------------------------#
    #Returns coordinates needed to create vector
    def getVectCoords(self):
        #get object coords and format as np array
        coords = np.asarray(self.coords)
        #find how many rows long
        shape = coords.shape
        row = (shape[0] - 1)
        #get most recent set of coords
        set1 = coords[row,]
        #search backwards to find coords that are not equal to most recent or zero
        set2 = Utilities.find_nEqual_nZero(set1, coords, False)
        #stack them
        coordsArray = np.vstack((set1, set2))
        return coordsArray

    #Creates a vector from objects coords
    def getVectors(self):
        #get needed coords
        vectorArray = self.getVectCoords()
        #find how many columns long
        shape = vectorArray.shape
        column = shape[1]
        #create array of correct size
        vector = np.zeros((1,4), dtype=int)
        #subtract past coords from most recent 
        for i in range(column):
            vector[0,i] = vectorArray[0,i] - vectorArray[1,i]
        return vector
        
#_______________________________________________________#
    #OTHER
#---------------------------------------------------#
    def setColor(self, Color):
        self.color = Color
        return
    
    def setType(self, botType):
        self.type = botType
        return
