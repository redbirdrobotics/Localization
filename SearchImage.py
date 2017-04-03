import numpy as np
import math 
from matplotlib import path 

class SearchImage:

    #Center of Image
    originx = 310
    originy = 240

    #Format Grid
    np.zeros(480,620)

    #Region 1
    poly_verts_one = [(280,240), (280,300), (340,300), (340,240), (280,240)]

    grid = path.Path.clip_to_bbox(poly_verts_one, points)
    regionOne = grid.reshape((ny,nx))

    #Region 2
    poly_verts_two = [(280,300), (280,360), (340,360), (340,300)]

    grid = path.Path.contains_points(points, poly_verts_two)
    regionTwo = grid.reshape((ny,nx))

    #Region 3
    poly_verts_three = [(280,360), (280,420), (340,420), (340,360)]

    grid = path.Path.contains_points(points, poly_verts_three)
    regionThree = grid.reshape((ny,nx))

    #Region 4
    poly_verts_four = [(280,420), (280,480), (340,480), (340,420)]

    grid = path.Path.contains_points(points, poly_verts_four)
    regionFour = grid.reshape((ny,nx))

    def rotateRegion(self, region, theta):
        originx = 310
        originy = 240
        region.rotate_around(originx, originy, theta)
        return







