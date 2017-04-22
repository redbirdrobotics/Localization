import cv2
import numpy as np

#GLOBALS
#ROI_Mat = np.array([[1,2,3,4], [2,3,4,5], [0,0,0,0], [4,5,6,7]]) #Tester
             
class Robot():
    
    def __init__(self, number):
        self.n = number
        self.color = "Unknown"
        self.type = "Unknown"
        self.coords = [0,0,0,0]
        #self.uuid =
        return

    def setColor(self, Color):
        self.color = Color
        return
    
    def setType(self, botType):
        self.type = botType
        return

    def setCoords(self, new_coords):        
        old_coords = np.asarray(self.coords)
        if not (np.all(old_coords == 0) and np.all(new_coords == 0)):
            self.coords = np.vstack((old_coords, new_coords))
        return

    def setROI(self, image, coords, pad):
        for x,y,w,h in coords:
            self.ROI = image[y-pad:y+h+pad, x-pad:x+w+pad]
        return
    
##Marky = Robot(1)
##Ricky = Robot(2)
##Danny = Robot(3)
##RoboList = [Marky, Ricky, Danny]
##RoboList[0].setColor("BLUE")
##print Marky.color
##Marky.setColor("Purple")
##print Marky.color
##RoboList[0].setCoords([5,5,6,7])
###print Marky.coords
##RoboList[0].setCoords([0,6,6,6])
###print Marky.coords
##robo = get_openRow()
##location = np.array([1,2,3,4])
##RoboList[2].setCoords(location)
##print location
##print Danny.coords
##print RoboList[2].coords

