import cv2
import numpy as np
import time

class Utilities():
    @staticmethod
    def replace_Rows(matrix, rows, rowNumber):
        numRows = rows.shape
        for i in range(numRows[0]):
            matrix[(rowNumber+i),:] = rows[i]
        return
    
    #Takes current position of all objects out of image
    @staticmethod
    def removeAll_Rect(image, matrix):
        numRows = matrix.shape
        for i in range(numRows[0]):
            if not np.all(matrix[i,:] == 0):
                x = int(matrix[i,0])
                y = int(matrix[i,1])
                w = int(matrix[i,2])
                h = int(matrix[i,3])
                image = cv2.rectangle(image, (x,y), (x+w, y+h), (255,255,255), -1)
        return image

    #Finds empty row of current position matrix
    @staticmethod
    def get_openRow(cur_pos):
        for i in range(14):
            if np.all(cur_pos[i,:] == 0):
                row = i
                break
            else:
                row = 14
        return  row

    @staticmethod
    def getAll_takenRows(cur_pos):
        foundList = []
        for i in range(14):
            if np.all(cur_pos[i,:] != 0):
                foundList.extend([i])
        return foundList

    @staticmethod
    def get_Frame(video):        
        ret, frame = video.read()
        return frame
    
    #Gets rectangle that encapsulates area of detected object
    @staticmethod
    def get_Loc(cascade, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        obj = cascade.detectMultiScale(gray, 1.3, 5)
        mat = np.array([0,0,0,0])
        if obj == ():
            mat = np.array([0,0,0,0])
        else:
            for (x,y,w,h) in obj:
                mat = np.array([x,y,w,h])
        return mat
    
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
    
##cur_pos = np.array([[1,2,3,4],[0,0,0,0],[1,2,3,4],[0,0,0,0],[1,2,3,4],[0,0,0,0],[1,2,3,4],[0,0,0,0],[1,2,3,4],[0,0,0,0],[1,2,3,4],[0,0,0,0],[1,2,3,4],[0,0,0,0]])
##foundList = Utilities.get_all_openRow(cur_pos)
##print foundList
 
