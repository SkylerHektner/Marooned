# Consumable_Class.py
# Spring 2016
# Team Windstorm

import pygame
from pygame.locals import Rect

class consumable(object):
    
    def __init__(self, position, tileSize):
        self.POS = position
        self.SIZE = int(tileSize * .4)
        
        self.IMAGE = pygame.transform.scale(self.IMAGE, (self.SIZE, self.SIZE))
        
        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])
        
        self.CONSUMED = False
        
    def update(self, screenRect):
        self.onScreen = self.RECT.colliderect(screenRect)
    
    def returnImage(self):
        return self.IMAGE
    
    def returnBlitPos(self, displayRect):
        x1, y1 = self.IMAGE.get_size()
        x = (self.POS[0] - (x1//2 - self.SIZE//2)) - displayRect[0]
        y = (self.POS[1] - (y1//2 - self.SIZE//2)) - displayRect[1]
        return (x,y)
    
    def collideChar(self, Char):
        pass

class consumableHealth(consumable):
    
    def __init__(self, position, tileSize, soundController):
        self.IMAGE = pygame.image.load('Resources/Sprites/Health.png')
        consumable.__init__(self, position, tileSize)
        self.healAmount = 25
        self.SOUND = soundController
        
    def collideChar(self, Char):
        if self.RECT.colliderect(Char.RECT) and not self.CONSUMED:
            Char.health += self.healAmount
            if Char.health > Char.healthMax:
                Char.health = Char.healthMax
            self.CONSUMED = True
            self.SOUND.Consumables.playGulp()

class consumableAmmo(consumable):
    
    def __init__(self, position, tileSize, soundController):
        self.IMAGE = pygame.image.load('Resources/Sprites/Ammo.png')
        consumable.__init__(self, position, tileSize)
        self.AmmoRecovery = 3
        self.SOUND = soundController
    
    def collideChar(self, Char):
        if self.RECT.colliderect(Char.RECT) and not self.CONSUMED:
            Char.ammo += self.AmmoRecovery
            self.CONSUMED = True
            self.SOUND.Consumables.playReload()