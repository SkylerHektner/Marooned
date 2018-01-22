# Tile_Class.py
# Spring 2016
# Team WindStorm

import pygame
from pygame.locals import *

class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, size, tileSheet, sheetRect, Rotation):
        pygame.sprite.Sprite.__init__(self)

        self.POS = list(pos)
        self.SIZE = size
        self.sheetRect = sheetRect
        self.rot = Rotation
        
        self.collide = False
        self.spawn = ''

        self.sheet = tileSheet # This is a pointer to the surface object in the map class

        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE]) # used for calculating collide

    def setCollide(self, bool): # Simple method to change the collide value of a tile
        self.collide = bool

    def setSpawn(self, name): # Simple method to change the spawn attribute of a tile
        self.spawn = name

    def returnImage(self): # Used to update the map surface if there are any changes made to tiles
        temp = pygame.surface.Surface((self.SIZE, self.SIZE), flags = SRCALPHA, depth = 32)
        temp.blit(self.sheet, (0,0), area = self.sheetRect)
        temp = pygame.transform.rotate(temp, self.rot)
        return temp

