# Vector_Class.py
# Skyler Hektner
# Spring 2016

import math

class vec2():

    def __init__(self, x, y):

        self.x = float(x)
        self.y = float(y)
        self.vec = (self.x,self.y)

    def __str__(self):

        return str(self.vec)

    def __add__(self, RV):

        x = self.x + RV.x
        y = self.y + RV.y

        return vec2(x,y)

    def __sub__(self, RV):

        x = self.x - RV.x
        y = self.y - RV.y

        return vec2(x,y)

    def __mul__(self, mult):

        x = self.x * mult
        y = self.y * mult

        return vec2(x,y)

    @staticmethod
    def vecFromPoints(p1, p2):
        x = p2[0] - p1[0]
        y = p2[1] - p1[1]

        return vec2(x,y)
    
    def normalizeIP(self):
        mag = (self.x**2 + self.y**2)**.5
        x = self.x/mag
        y = self.y/mag
        self.x = x
        self.y = y

    

