# HeadHunter_Class.py
# Team Windstorm
# Spring 2016

import pygame
from pygame.locals import *
import math
from Pyganim import PygAnimation
from Sword_Collision_Class import SwordCollison


class HeadHunter(object):
    
    def __init__(self, tileSize, pos, soundController):
        
        self.POS = list(pos)
        self.SIZE = int(tileSize * .9)
        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])
        
        self.SOUND = soundController
        self.DAMAGESOUND = self.SOUND.HeadHunter.playDamage
        self.CHASINGSOUND = self.SOUND.HeadHunter.playChasing
        self.NOTICESOUND = self.SOUND.HeadHunter.playNotice
        self.ATTACKSOUND = self.SOUND.HeadHunter.playAttack
        
        # Load image
        self.ActiveImage = None # Later assigned to an image from the animation      
        self.FACING = 0
        
        # Flags
        self.active = True
        self.tracking = False
        self.onScreen = False
        self.collidedChar = False # used to keep track of if the zombie just attacked
        self.damageDone = False
        self.stunned = False
        self.moveL = [0,0]
        
        
        # Stats
        self.health = 100
        self.maxhealth = 100
        self.healthOld = self.health # Used to calculate if damage was damage in the knockback function
        
        self.damage = 10
        self.collidedCharDelay = .7 # the time, in seconds, the zombie stops after colliding with the player
        # Half way through the above delay the zombie will do damage to the character if they have not moved away
        self.SprRange = self.SIZE
        
        self.BASESPEED = 5
        self.speed = self.BASESPEED
        
        self.AgroRange = .4 # this is the portion of the X resolution the mob will start tracking at
        
        self.knockBackRange = self.SIZE//2 # the distance the zombie gets knocked back when it takes damage
        self.stunTime = 400 # time, in milleseconds, the enemy is stunned when it takes damage
        self.stunnedAtTime = 0
        self.stunRemaining = 0
        
        self.__setUpPyganim()
        
    def __setUpPyganim(self):
        temp = pygame.image.load('Resources/Sprites/headhunter/stand.png')
        refXY = temp.get_size()
        
        self.STAND_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/headhunter/stand.png'), refXY)
        
        self.WALK_L_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/headhunter/WalkL.png'), refXY)
        self.WALK_R_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/headhunter/WalkR.png'), refXY)
        
        self.ATT_1_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/headhunter/Att1.png'), refXY)
        self.ATT_2_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/headhunter/Att2.png'), refXY)
        
        self.STUN_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/headhunter/stun.png'), refXY)
        
        walkTime = .2
        hitTime = self.collidedCharDelay/2
        
        self.WALK_ANIM = PygAnimation([(self.STAND_IMAGE, walkTime),
                                       (self.WALK_L_IMAGE, walkTime),
                                       (self.STAND_IMAGE, walkTime),
                                       (self.WALK_R_IMAGE, walkTime)])
        
        self.ATT_ANIM = PygAnimation([(self.ATT_1_IMAGE, hitTime),
                                      (self.ATT_2_IMAGE, hitTime * 2)])
            
            
        
    def __autoScale(self, image, refXY):
        x,y = image.get_size()
        scaleTuple = (x/refXY[1], y/refXY[1])
        image = pygame.transform.scale(image, (int(self.SIZE * scaleTuple[0]), int(self.SIZE * scaleTuple[1])))
        image = image.convert_alpha()
        return image   
        
    def __getImageRot(self): # If onscreen, rotates the zombie image to face the proper direction
        imageRot = pygame.transform.rotate(self.ActiveImage, self.FACING)
        self.IMAGE = imageRot
            
    def __updateFacing(self, Char): # updates the direction the zombie is facing
        x = (self.POS[0] + self.SIZE//2) - (Char.POS[0] + Char.SIZE//2)
        y = (self.POS[1] + self.SIZE//2) - (Char.POS[1] + Char.SIZE//2)
        x = -x
        
        if x == 0: x += 1
        deg =  math.atan(y/x) * 57.32 + 90
        if x > 0: deg += 180
        self.FACING = round(deg)
   
    def __move(self): # Moves the zombie to the direction they are facing
        
        moveL = []
        moveL.append(-(round(math.cos((self.FACING- 90)/57.32) * self.speed)))
        moveL.append(round(math.sin((self.FACING - 90)/57.32) * self.speed))
        
        self.POS[0] += moveL[0]
        self.POS[1] += moveL[1]
        
        self.moveL[0] += moveL[0]
        self.moveL[1] += moveL[1]
        
        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])
        
    def __collision_correction(self, colRects):
        collidedBoxes = []
        for box in colRects: 
            if self.RECT.colliderect(box):
                collidedBoxes.append(box)
    
        if collidedBoxes != []: # Additional check to allow independent x/y movement
            self.POS[0] -= self.moveL[0]
            self.POS[1] -= self.moveL[1]
            self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])  
            for x in range(2): 
                self.POS[x] += self.moveL[x]
                self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])
                for box in collidedBoxes:
                    if self.RECT.colliderect(box):
                        self.POS[x] -= self.moveL[x]
                        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])
                        
        self.moveL = [0,0]
        
    def __updateAttack(self, Char):
        
        if self.RECT.colliderect(Char.RECT) and not self.collidedChar:
            self.collidedChar = True
            self.timeAttacked = pygame.time.get_ticks()
            self.ATT_ANIM.play()
            
        elif (self.collidedChar and pygame.time.get_ticks() - self.timeAttacked > self.collidedCharDelay * 500 
              and not self.damageDone):
            self.__attack([Char])
            self.damageDone = True
            
        elif self.collidedChar and pygame.time.get_ticks() - self.timeAttacked > self.collidedCharDelay * 1000:
            self.collidedChar = False
            self.damageDone = False
            self.ATT_ANIM.stop()
            
    def __attack(self, enemyList):
        self.attacking = True
        cenChar = (self.POS[0] + self.SIZE//2, self.POS[1] + self.SIZE//2)
        self.timeAttacked = pygame.time.get_ticks()
        self.ATTACKSOUND()
        
        tempL = []
        for enemy in enemyList:
            tempL.append(enemy.RECT)
        
        endPos = (-(round(math.cos((self.FACING- 90)/57.32) * self.SprRange)),
                    round(math.sin((self.FACING - 90)/57.32) * self.SprRange))
        endPos = (endPos[0] + cenChar[0], endPos[1] + cenChar[1])
        
        tempSwrdColObject = SwordCollison(tempL, cenChar, self.SprRange, 
                                 (cenChar, endPos))
        
        hitBoxes = tempSwrdColObject.returnResult()
        del tempSwrdColObject
        
        if hitBoxes != []:
            for enemy in enemyList:
                if enemy.RECT in hitBoxes:
                    enemy.health -= self.damage
            
    def __checkStun(self):
        
        if self.healthOld > self.health:
            self.stunned = True
            self.stunnedAtTime = pygame.time.get_ticks()
            self.stunRemaining += self.stunTime
            self.DAMAGESOUND()
        
        self.healthOld = self.health
        
    def __updateStun(self):
        if self.stunRemaining > 0:
            if pygame.time.get_ticks() - self.stunnedAtTime > self.stunRemaining:
                self.stunRemaining -= pygame.time.get_ticks() - self.stunnedAtTime
        else:
            self.stunned = False
            
    def returnBlitPos(self, displayRect):
        x1, y1 = self.IMAGE.get_size()
        x = (self.POS[0] - (x1//2 - self.SIZE//2)) - displayRect[0]
        y = (self.POS[1] - (y1//2 - self.SIZE//2)) - displayRect[1]
        return (x,y)
    
    def __updateActiveImage(self):
        if not self.tracking:
            self.ActiveImage = self.STAND_IMAGE
        elif self.collidedChar:
            self.ActiveImage = self.ATT_ANIM.returnImage()
        elif self.stunned:
            self.ActiveImage = self.STUN_IMAGE        
        elif self.tracking and not self.collidedChar:
            self.ActiveImage = self.WALK_ANIM.returnImage()

            
    def __removeRect(self, colRects):
        for rect in colRects:
            if rect == self.RECT:
                colRects.pop(colRects.index(rect))
        
        return colRects
        
    def update(self, screenRect, Char, colRects):
        self.onScreen = self.RECT.colliderect(screenRect) # updates the on screen flag if the zombie is on screen
        if not self.tracking and ((self.POS[0] - Char.POS[0])**2 + (self.POS[1] - Char.POS[1])**2)**.5 < screenRect[2] * self.AgroRange:
            self.tracking = True
            self.WALK_ANIM.play()
            self.NOTICESOUND()
        elif self.tracking and ((self.POS[0] - Char.POS[0])**2 + (self.POS[1] - Char.POS[1])**2)**.5 > screenRect[2] * self.AgroRange * 2:
            self.tracking = False
            self.WALK_ANIM.stop()
        
        if self.tracking:
            colRects = self.__removeRect(colRects)
            self.__checkStun()
            self.__updateStun()
            if not self.collidedChar and not self.stunned:
                self.__updateFacing(Char)
                self.__move()
            self.__updateAttack(Char)
            self.__collision_correction(colRects)
            self.CHASINGSOUND()
            
        if self.onScreen:
            self.__updateActiveImage()
            self.__getImageRot()
                            
    def returnImage(self):
        return self.IMAGE
        