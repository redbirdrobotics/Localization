import cv2
import math
import numpy as np
from Camera import Camera 
import time

class Utilities():

#_______________________________________________________#
    #General Array Manipulation Functions
#---------------------------------------------------#

    #Takes a matrix and replaces rows of matrix with given rows
    #starting with given row number
    
    @staticmethod
    def replace_Rows(matrix, rows, rowNumber):
        numRows = rows.shape
        for i in range(numRows[0]):
            matrix[(rowNumber+i),:] = rows[i]
        return

    #Replaces values in array with values in list 

    @staticmethod
    def replace_Values(array_row, listValues, array_start, list_inc = True):
        length = len(listValues)
        x = 0
        for i in range(array_start, length):
            if list_inc == True:
                array[i] = listvalues[x]
                x += 1
            else:
                array[i] = listValues[(length - 1) - x]
                x -= 1
        return
        
            

    #Returns number of first row of matrix for which all members are not zero

    @staticmethod
    def get_openRow(matrix):
        numRows = matrix.shape
        for i in range(numRows[0]):
            if np.all(matrix[i,:] == 0):
                row = i
                break
            else:
                row = numRows[0]
        return  row

    #Returns a list of row numbers in a matrix for which all members are not zero
    #extend is like append but for lists    
    @staticmethod
    def getAll_takenRows(array):
        foundList = []
        shape = array.shape
        for i in range(shape[0]):
            if np.all(array[i,:] != 0):
                foundList.extend([i])
        return foundList

    #Compares a value to a set of values, finds a value that is not equal to itself or zero
    #Function can start from either end of the list via bool argument
    @staticmethod
    def find_nEqual_nZero(value, array, FtoL = True):
        shape = array.shape
        rows = shape[0]
        found = value
        if FtoL == False:
            for i in range(rows-1, -1, -1):
                if not (np.all(value == array[i]) or np.all(array[i] == 0)):
                    found = array[i]
                    break
        else:
            for i in range(0, rows):
                if not (np.all(value == array[i]) or np.all(array[i] == 0)):
                    found = array[i]
                    break
        return found

    #If value1 equals value2 set the row to all zeros
    
    @staticmethod
    def compare_Equals(array_row, value1, value2):
        if value1 == value2:
            array_row = np.array([0,0,0,0])
        return array_row

    @staticmethod
    def zero_ifLessThan(array, minSum):
        shape = array.shape
        for i in range(shape[0]):
            if (np.sum(array[i]) < minSum):
                array[i,:] = 0
        for i in range(shape[1]):
            if (np.sum(array[:,i]) < minSum):
                array[:,i] = 0
        return array 
                
#_______________________________________________________#
    #Localization Functions
#---------------------------------------------------#

    #Returns oppDist:x-distance & adjDist:y-distance of object given its pixel coordinates
    #Distances are in the unit given by height
    @staticmethod
    def get_dis(xrow, yrow, coords, height):
        xangle = xrow[coords[0]]
        yangle = yrow[coords[1]]
        adjDist = height* math.tan(yangle)
        oppDist = adjDist*math.tan(xangle)
        return (oppDist, adjDist)
    
#_______________________________________________________#
    #Image Editing Functions
#---------------------------------------------------#
   
    #Takes current position of all objects out of image
    
    @staticmethod
    def removeAll_Rect(image, matrix):
        newImage = image
        numRows = matrix.shape
        for i in range(numRows[0]):
            if not np.all(matrix[i,:] == 0):
                x = int(matrix[i,0])
                y = int(matrix[i,1])
                w = int(matrix[i,2])
                h = int(matrix[i,3])
                newImage = cv2.rectangle(newImage, (x,y), (x+w, y+h), (255,255,255), -1)
        return newImage

    @staticmethod
    def drawAll_Rect(image, matrix):
        newImage = image
        numRows = matrix.shape
        for i in range(numRows[0]):
            if not np.all(matrix[i,:] == 0):
                x = int(matrix[i,0])
                y = int(matrix[i,1])
                w = int(matrix[i,2])
                h = int(matrix[i,3])
                newImage = cv2.rectangle(newImage, (x,y), (x+w, y+h), (255,255,255), 2)
        return newImage

    @staticmethod
    def label_ROI(image, cur_pos):
        image_text = image
        rowList = Utilities.getAll_takenRows(cur_pos)
        length = len(rowList)
        for i in range(length):
            bot = rowList[i]
            x = int(cur_pos[bot,0])
            y = int(cur_pos[bot,1])
            h = int(cur_pos[bot,3])
            image_text = cv2.putText(image_text, ("%s"% i), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, 255, 2)
        return image_text
    
    #Gets rectangle that encapsulates area of detected object

    @staticmethod
    def create_PointSet(array):
        shape = array.shape
        rows = (shape[0])
        pointset = np.reshape(array, ((2*rows),2))
        for i in range(rows):
            subarray = np.reshape(array[i], (2,2))
            true_coord = subarray.sum(0)
            pointset[((2*i)+1)] = true_coord
        return pointset

#_______________________________________________________#
    #Detection Methods
#---------------------------------------------------#


#__________________________#
    #Haar/LBP Based Detection
#------------------------#
    @staticmethod
    def get_Loc(cascade, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        obj = cascade.detectMultiScale(gray, 1.3, 5)
        array_loc = np.array([0,0,0,0])
        if not obj == ():
            for (x,y,w,h) in obj:
                array_loc = np.array([x,y,w,h])
        return array_loc
    
    @staticmethod
    def getAll_Loc(cascade, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mat = np.array([[0,0,0,0]])
        detect = True
        while detect == True:
            obj = cascade.detectMultiScale(gray, 1.3, 5)
            if obj == ():
                detect = False
            else:
                for (x,y,w,h) in obj:
                    if np.all(mat == 0):
                        mat = np.array([[x,y,w,h]])
                    else:
                        old_array = mat
                        new_row = np.array([[x,y,w,h]])
                        mat = np.vstack((old_array, new_row))
            gray = Utilities.removeAll_Rect(gray, mat)            
        return mat 

#__________________________#
    #Blob Based Detection
#------------------------#
    @staticmethod
    def get_Parameters(object, detectorType):
        if detectorType == 0:            
            #Thresholds
            object.minThreshold = 0
            object.maxThreshold = 256

            #Filter by Color
            object.filterByColor = True
            object.blobColor = 255

            #Filter by Area
            object.filterByArea = True
            object.minArea = 100
        return

    @staticmethod
    def create_Mask(img, minThresh, maxThresh, minPixel):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, minThresh, maxThresh)
        count = cv2.countNonZero(mask)

        if (count > minPixel):
            ret = True
        else:
            ret = False
        return ret, mask



##tester = np.array([[1,1,1,1], [2,2,2,2,], [0,0,0,0,], [3,3,3,3]])   
##print Utilities.getAll_takenRows(tester)  
##cam0 = Camera(0, (1280, 720), 60, (130, 90), (0, 45))
##frame = cam0.getFrame()
##newFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
##while True:
##    esc1 = Camera.showFrame(newFrame, 'GRAY')
##    esc2 = Camera.showFrame(frame, 'Orig')
##    if (esc1 == True) or (esc2 ==True):
##        break
##cam0.detach()
##cv2.destroyAllWindows()




    

