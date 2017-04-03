class Robot:

    #defaults
    Type = "Unfound"
    Name = "Unnamed"
    Color = "Unknown"
    x = 0
    y = 0

    def getType(self, botType, printYN):
        Type = botType
        if printYN == 1:
            return Type
        else:
            return

    def getName(self, botName, returnYN):
        Name = botName
        if returnYN == 1:
            return Name
        else:
            return

    def getColor(self, botColor, returnYN):
        Color = botColor
        if returnYN == 1:
            return Color
        else:
            return

    def getVector(self, xcord, ycord, returnYN):
        x = xcord
        y = ycord
        vect = [x,y]
        if returnYN == 1:
            return vect
        else:
            return

ROI = Robot()
print Robot.getType(ROI, "Ground", 1)
print Robot.getName(ROI, "Steve", 1)
print Robot.getColor(ROI, "Red", 1)
print Robot.getVector(ROI, 5, 6, 1)


