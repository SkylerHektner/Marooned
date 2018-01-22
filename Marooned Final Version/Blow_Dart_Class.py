# Blow_Dart_Class.py
# Spring 2016
# Team Windstorm

import pygame
from pygame.locals import Rect
from Vector_Class import vec2

class BlowDart(object):
    
    def __init__(self, displayRect, startPos, charPos, facing, damage):
        
        self.SIZE = int(displayRect[2] * .04)
        self.IMAGE = pygame.image.load('Resources/Sprites/Blow_Dart.png')
        self.IMAGE = pygame.transform.scale(self.IMAGE, (self.SIZE//3, self.SIZE))
        self.IMAGE = pygame.transform.rotate(self.IMAGE, facing)
        self.IMAGE = self.IMAGE.convert_alpha()
        
        self.damage = damage
        
        x,y = self.IMAGE.get_size()
        
        self.POS = list(startPos)
        self.VEC = vec2.vecFromPoints(startPos, charPos)
        self.VEC.normalizeIP()
        self.RECT = Rect(startPos + [x, y])
        
        self.SPEED = 10
        
        self.onScreen = True
        self.hit = False
        
    def returnBlitPos(self, displayRect):
        x = self.POS[0] - displayRect[0]
        y = self.POS[1] - displayRect[1]
        return (x,y)
    
    def returnImage(self):
        return self.IMAGE
    
    def __damageChar(self, char):
        cenDart = (self.RECT[0] + self.RECT[2]//2, self.RECT[1] + self.RECT[3]//2)
        if not self.hit and char.RECT[0] < cenDart[0] < char.RECT[0] + char.RECT[2] and char.RECT[1] < cenDart[1] < char.RECT[1] + char.RECT[3]:
            char.health -= self.damage
            self.hit = True
            
        
    def update(self, displayRect, Char):
        self.POS = [self.POS[0] + int(self.VEC.x * self.SPEED), self.POS[1] + int(self.VEC.y * self.SPEED)]
        self.RECT.x, self.RECT.y = self.POS[0], self.POS[1]
        self.onScreen = self.RECT.colliderect(displayRect)
        self.__damageChar(Char)
        
        
        
        