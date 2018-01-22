# Sword_Collision_Class.py
# Team Windstorm
# Spring 2016

import math

class SwordCollison(object):

    def __init__(self, boxes, cenChar, swrdRad, line):

        testL = self.__calcBoxTestList(boxes, cenChar, swrdRad)
        if testL != []:
            self.result = self.__calcCollide(testL, line)
        else:
            self.result = []
        
    def __calcBoxTestList(self, boxes, cenChar, swrdRad):

        boxL = []

        for box in boxes:
            TL = (box[0],box[1])
            TR = (box[0] + box[2], box[1])
            BL = (box[0], box[1] + box[3])
            BR = (box[0] + box[2], box[1] + box[3])
            tempL = [TL, TR, BL, BR]
            for corn in tempL:
                 if math.sqrt((corn[0]-cenChar[0])**2 + (corn[1]-cenChar[1])**2) < swrdRad:
                     boxL.append(box)
                     break

        return boxL

    def __calcCollide(self, testL, line):
        result = []
        for box in testL:
            if self.__pointInBox(box, line[0]):
                result.append(box)
            elif self.__pointInBox(box, line[1]):
                result.append(box)
            else:
                for x in range(5):
                    point = ((line[1][0] - line[0][0])/(x+1) + line[0][0],
                             (line[1][1] - line[0][1])/(x+1) + line[0][1])
                    if self.__pointInBox(box, point):
                        result.append(box)
                        break
        return result

    def __pointInBox(self, box, point):
        if box[0] < point[0] < box[0] + box[2]:
            if box[1] < point[1] < box[1] + box[3]:
                return True
        else:
            return False

    def returnResult(self):
        return self.result