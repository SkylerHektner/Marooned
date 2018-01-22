# Witch_Doctor_Class.py
# Team Windstorm
# spring 2016

import pygame
from pygame.locals import *
import math
from Pyganim import PygAnimation
from Blow_Dart_Class import BlowDart

class WitchDoctor(object):
    
    def __init__(self, tileSize, pos, soundController):
        
        self.POS = list(pos)
        self.SIZE = int(tileSize * .6)
        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])
        
        self.SOUND = soundController
        
        # Load image
        self.ActiveImage = None # Later assigned to an image from the animation      
        self.FACING = 0
        
        # Flags
        self.active = True
        self.tracking = False
        self.onScreen = False
        self.stunned = False
        self.attacking = False
        self.shot = False
        self.returnDart = False
        self.moveL = [0,0]
        
        
        # Stats
        self.health = 70
        self.maxhealth = 70
        self.healthOld = self.health # Used to calculate if damage was damage in the knockback function
        
        self.damage = 5
        self.shootDelay = 2 # the time, in seconds, the mob takes to shoot
        # one quarter way through the above delay the mob will shoot
        self.shootDistance = int(self.SIZE * 4.5) # how close the mob will be to the player before it fires its dart
        
        self.BASESPEED = 7
        self.speed = self.BASESPEED
        
        self.AgroRange = .4 # this is the portion of the X resolution the mob will start tracking at
        
        self.stunTime = 300 # time, in milleseconds, the enemy is stunned when it takes damage
        self.stunnedAtTime = 0
        self.stunRemaining = 0
        
        self.__setUpPyganim()
        
    def __setUpPyganim(self):
        temp = pygame.image.load('Resources/Sprites/witchDoctor/stand.png')
        refXY = temp.get_size()
        
        self.STAND_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/witchDoctor/stand.png'), refXY)
        
        self.WALK_L_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/witchDoctor/WalkL.png'), refXY)
        self.WALK_R_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/witchDoctor/WalkR.png'), refXY)
        
        self.ATT_1_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/witchDoctor/Att1.png'), refXY)
        self.ATT_2_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/witchDoctor/Att2.png'), refXY)
        
        self.STUN_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/witchDoctor/Stun.png'), refXY)
        
        walkTime = .15
        shootTime = self.shootDelay/4
        
        self.WALK_ANIM = PygAnimation([(self.STAND_IMAGE, walkTime),
                                       (self.WALK_L_IMAGE, walkTime),
                                       (self.STAND_IMAGE, walkTime),
                                       (self.WALK_R_IMAGE, walkTime)])
        
        self.ATT_ANIM = PygAnimation([(self.ATT_1_IMAGE, shootTime),
                                      (self.ATT_2_IMAGE, self.shootDelay - shootTime)])
            
            
        
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
        
        if not self.attacking and ((self.POS[0] - Char.POS[0])**2 + (self.POS[1] - Char.POS[1])**2)**.5 < self.shootDistance:
            self.attacking = True
            self.timeAttacked = pygame.time.get_ticks()
            self.ATT_ANIM.play()
            
        elif self.attacking and not self.shot and pygame.time.get_ticks() - self.timeAttacked > self.shootDelay * 250:
            self.shot = True
            self.returnDart = True
            
        elif self.attacking and pygame.time.get_ticks() - self.timeAttacked > self.shootDelay * 1000:
            self.attacking = False
            self.shot = False
            self.ATT_ANIM.stop()
            
            
    def __checkStun(self):
        
        if self.healthOld > self.health:
            self.stunned = True
            self.stunnedAtTime = pygame.time.get_ticks()
            self.stunRemaining += self.stunTime
            self.SOUND.WitchDoctor.playDamage()
        
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
        elif self.attacking:
            self.ActiveImage = self.ATT_ANIM.returnImage()
        elif self.stunned:
            self.ActiveImage = self.STUN_IMAGE
        elif self.tracking and not self.attacking:
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
            self.SOUND.WitchDoctor.playNotice()
        elif self.tracking and ((self.POS[0] - Char.POS[0])**2 + (self.POS[1] - Char.POS[1])**2)**.5 > screenRect[2] * self.AgroRange * 2:
            self.tracking = False
            self.WALK_ANIM.stop()
        
        if self.tracking:
            colRects = self.__removeRect(colRects)
            self.__checkStun()
            self.__updateStun()
            if not self.attacking and not self.stunned:
                self.__move()
            self.__updateFacing(Char)
            self.__updateAttack(Char)
            self.__collision_correction(colRects)
            
        if self.onScreen:
            self.__updateActiveImage()
            self.__getImageRot()
                            
    def returnImage(self):
        return self.IMAGE
    
    def checkDartReturn(self, displayRect, CharPos):
        if self.returnDart:
            self.returnDart = False
            CharPos = (CharPos[0] + 20, CharPos[1] + 20)
            result = (True, BlowDart(displayRect, self.POS, CharPos, self.FACING, self.damage))
            self.SOUND.WitchDoctor.playBlowGun()
        else:
            result = (False, None)
            
        return result
        