# Char_Class.py
# Spring 2016
# Team Windstorm

import pygame
from pygame.locals import *
import math
from Sword_Collision_Class import SwordCollison
from BlunderBuss_Collision_Class import BlunderCollision
from Pyganim import PygAnimation

class Char(object):

    def __init__(self, pos, tileSize, soundController):
        try: self.POS = list(pos)
        except: self.POS = [0,0]
        
        self.SIZE = int(tileSize * .8)
        self.RECT = Rect(self.POS+ [self.SIZE, self.SIZE])
        
        self.SOUND = soundController

        self.ActiveImage = None # Later assigned to one of our Base Images

        self.FACING = 0 # Where the character is facing in degrees (0 = up, goes counterclockwise)
        
        # Used in the movement speed modifier formula for direction facing
        self.sModDict = {(-1,-1): 45, (-1,0): 90, (-1,1): 135, (0,1): 180,
                         (1,1): 225, (1,0): 270, (1,-1): 315, (0,-1): 360,
                         (0,0): 0}

        # Stats
        self.health = 100
        self.healthMax = 100
        self.oldHealth = self.health
        
        self.staminaRegen = 3 #stamina regen per game loop
        self.staminaMax = 1000
        self.stamina = self.staminaMax
        
        self.dashtime = .15 # length of dash in seconds
        self.dashmodifier = 2 # Speed increase while dashing. 0 means no speed increase. .5 means 50% speed increase
        self.dashCost = 500 # Stamina Cost of Dash
        
        self.sprintmodifier = 1.4 # speed increase while sprinting. 1 = no speed increase. 2 = double speed
        self.sprintDegen = 8 # Make sure to account for the stamina regen
        
        self.BASESPEED = 8 # Char Speed
        self.speed = self.BASESPEED # self.speed is a variable that changes depending on sprint/dash
        
        self.swrdDamage = 30 # Damage the sword does
        self.swrdRad = self.SIZE * 1.3 # range the sword reaches
        self.swrdDelay = .5 # The time you have to wait to attack again after swinging
        
        self.blndrDamage = 30
        self.blndrRad = self.SIZE * 16
        self.blndrDelay = 1
        self.bldnrSpread = 10
        self.ammo = 10 # The starting ammo for the blunderBuss

        # Flags
        self.active = True #Controls of the character is displayed
        self.dashing = False # Controls if the character is currently dashing
        self.sprinting = False # Controls if the character is currently trying to sprint
        self.attacking = False # Controls if the character is currently in an attack animation
        self.firing = False # Controls if the character is currently in a firing animation
        self.moving = False # Controls if the character is currently in a walk animation
        self.equiped = 'swrd' # the currently equiped weapon
        self.past_moveL = [0,0] # a record of the previous frames move
        
        # Create pyganim animations
        self.__setUpPyganim()
        
    def __setUpPyganim(self):
        temp = pygame.image.load('Resources/Sprites/Character/swrd_stand.png')
        refXY = temp.get_size()
        
        self.STAND_SWORD_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/Character/swrd_stand.png'), refXY)
        self.STAND_BLNDR_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/Character/blndr_stand.png'), refXY)
    
        walk1_sword_image = self.__autoScale(pygame.image.load('Resources/Sprites/Character/swrd_walk1.png'), refXY)
        walk2_sword_image = self.__autoScale(pygame.image.load('Resources/Sprites/Character/swrd_walk2.png'), refXY)
    
        walk1_blndr_image = self.__autoScale(pygame.image.load('Resources/Sprites/Character/blndr_walk1.png'), refXY)
        walk2_blndr_image = self.__autoScale(pygame.image.load('Resources/Sprites/Character/blndr_walk2.png'), refXY)
    
        att1_swrd_image = self.__autoScale(pygame.image.load('Resources/Sprites/Character/swrd_att1.png'), refXY)
        att2_swrd_image = self.__autoScale(pygame.image.load('Resources/Sprites/Character/swrd_att2.png'), refXY)
    
        att1_blndr_image = self.__autoScale(pygame.image.load('Resources/Sprites/Character/blndr_att1.png'), refXY) 
        att2_blndr_image = self.__autoScale(pygame.image.load('Resources/Sprites/Character/blndr_att2.png'), refXY)
        att3_blndr_image = self.__autoScale(pygame.image.load('Resources/Sprites/Character/blndr_att3.png'), refXY)
    
        swrd_walk_time = .25
        blndr_walk_time = .25
        swrd_hit_time = self.swrdDelay/3
        blndr_fire_time = .2
    
        self.WALK_SWRD_ANIM = PygAnimation([(self.STAND_SWORD_IMAGE, swrd_walk_time),
                                            (walk1_sword_image, swrd_walk_time),
                                            (self.STAND_SWORD_IMAGE, swrd_walk_time),
                                            (walk2_sword_image, swrd_walk_time)])
    
        self.WALK_BLNDR_ANIM = PygAnimation([(self.STAND_BLNDR_IMAGE, blndr_walk_time),
                                             (walk1_blndr_image, blndr_walk_time),
                                             (self.STAND_BLNDR_IMAGE, blndr_walk_time),
                                             (walk2_blndr_image, blndr_walk_time)])
    
        self.HIT_SWRD_ANIM = PygAnimation([(att1_swrd_image, swrd_hit_time),
                                           (att2_swrd_image, swrd_hit_time),
                                           (self.STAND_SWORD_IMAGE, swrd_hit_time * 2)])
    
        self.FIRE_BLNDR_ANIM = PygAnimation([(att1_blndr_image, blndr_fire_time),
                                             (att2_blndr_image, blndr_fire_time),
                                             (att3_blndr_image, blndr_fire_time),
                                             (self.STAND_BLNDR_IMAGE, blndr_fire_time)], loop = False)
                
    def __autoScale(self, image, refXY):
        x,y = image.get_size()
        scaleTuple = (x/refXY[1], y/refXY[1])
        image = pygame.transform.scale(image, (int(self.SIZE * scaleTuple[0]), int(self.SIZE * scaleTuple[1])))
        image = image.convert_alpha()
        return image

    def __getSurfRot(self, screenRect, mousePos):
        x = mousePos[0] - screenRect[2]//2
        y = -(mousePos[1] - screenRect[3]//2)
        if x == 0: x += 1
        deg =  math.atan(y/x) * 57.32 + 90
        if x > 0: deg += 180
        self.IMAGEROT = pygame.transform.rotate(self.ActiveImage, deg)
        self.FACING = int(deg)

        self.IMAGE = self.IMAGEROT

    def __move(self, screenRect, colRects, moveL):
        # Creates the speed modifier so the player moves slower when going backwards
        directMod = self.sModDict[tuple(moveL)]
        sMod = .25 * math.cos((self.FACING - directMod)/57.32) + .75

        # sets speed (also checks for diagonal movemet)
        speed = self.speed * sMod
        if abs(moveL[0]) == abs(moveL[1]) and moveL[0] != 0:
            speed = speed/math.sqrt(2)

        # Creates List for the position change, moves player, and resets the rect
        posChangeL = [round(speed) * moveL[0], round(speed) * moveL[1]]
        self.POS[0] += posChangeL[0]
        self.POS[1] += posChangeL[1]
        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])

        # Checks for all collision in the map
        collidedBoxes = []
        for box in colRects: 
            if self.RECT.colliderect(box):
                collidedBoxes.append(box)

        if collidedBoxes != []: # Additional check to allow independent x/y movement
            self.POS[0] -= posChangeL[0]
            self.POS[1] -= posChangeL[1]
            self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])  
            for x in range(2): 
                self.POS[x] += posChangeL[x]
                self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])
                for box in collidedBoxes:
                    if self.RECT.colliderect(box):
                        self.POS[x] -= posChangeL[x]
                        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])
                        
    def __dash(self): # Calls the dash
        self.speed += self.BASESPEED * self.dashmodifier
        self.__DashedAtTime = pygame.time.get_ticks()
        self.stamina -= self.dashCost
        self.dashing = True
    
    def __sprint(self):
        if self.stamina > 2:
            self.speed = self.BASESPEED * self.sprintmodifier            
            self.stamina -= self.sprintDegen
        else:
            self.speed = self.BASESPEED

            
    def __checkControls(self, events, pressed, screenRect, colRects, enemyList):
        
        # Update Movement
        moveL = [0,0]
        if pressed[K_w]:
            moveL[1] -= 1
        if pressed[K_s]:
            moveL[1] += 1
        if pressed[K_a]:
            moveL[0] -= 1
        if pressed[K_d]:
            moveL[0] += 1
        if moveL != [0,0]:
            self.__move(screenRect, colRects, moveL)
            self.moving = True
        else:
            self.moving = False
            
        # compare moveL to control pyganim on walking and audio
        if self.past_moveL == [0,0] and moveL != [0,0]:
            if self.equiped == 'swrd': self.WALK_SWRD_ANIM.play()
            elif self.equiped == 'blndr': self.WALK_BLNDR_ANIM.play()
            self.SOUND.Char.playWalking()
        elif self.past_moveL != [0,0] and moveL == [0,0]:
            if self.equiped == 'swrd': self.WALK_SWRD_ANIM.stop()
            elif self.equiped == 'blndr': self.WALK_BLNDR_ANIM.stop()
            self.SOUND.Char.stopWalking()
            
        self.past_moveL = moveL
                 
        # Check Dash
        if pressed[K_SPACE] and not self.dashing and self.stamina >= self.dashCost and moveL != [0,0]:
            self.__dash()        
            
        # Check Sprint
        for event in events:
            if event.type == KEYDOWN and event.key == K_LSHIFT:
                self.sprinting = True
            elif event.type == KEYUP and event.key == K_LSHIFT:
                self.sprinting = False
                self.speed = self.BASESPEED
        
        if pressed[K_LSHIFT] and self.sprinting and not self.dashing:
            self.__sprint()
            
        # Check Attack
        if pygame.mouse.get_pressed()[0] and not self.attacking and self.equiped == 'swrd':
            self.__attack(enemyList)
        elif pygame.mouse.get_pressed()[0] and not self.firing and self.equiped == 'blndr':
            self.__fire(enemyList)
            
        # Check Weapon Select
        if pressed[K_1] and not self.firing:
            self.equiped = 'swrd'
            self.WALK_BLNDR_ANIM.stop()
            self.WALK_SWRD_ANIM.play()
        elif pressed[K_2] and not self.attacking:
            self.equiped = 'blndr'
            self.WALK_SWRD_ANIM.stop()
            self.WALK_BLNDR_ANIM.play()
            
    def __fire(self, enemyList):
        if self.ammo > 0:
            self.ammo -= 1
            self.firing = True
            cenChar = (self.POS[0] + self.SIZE//2, self.POS[1] + self.SIZE//2)
            self.__FiredAtTime = pygame.time.get_ticks()
            self.FIRE_BLNDR_ANIM.play()
            self.SOUND.Char.playBlunder()
            
            tempL = []
            for enemy in enemyList:
                tempL.append(enemy.RECT)
            
            for x in range(5):
                endPos = (-(round(math.cos((self.FACING - 90 - ((x-2) * self.bldnrSpread))/57.32) * self.blndrRad)),
                            round(math.sin((self.FACING - 90 - ((x-2) * self.bldnrSpread))/57.32) * self.blndrRad))
                endPos = (endPos[0] + cenChar[0], endPos[1] + cenChar[1])
                
                tempBlndrCollisionObject = BlunderCollision(tempL, cenChar, self.blndrRad, 
                                         (cenChar, endPos))
                
                hitBoxes = tempBlndrCollisionObject.returnResult()
                del tempBlndrCollisionObject
                
                if hitBoxes != []:
                    for enemy in enemyList:
                        if enemy.RECT in hitBoxes:
                            enemy.health -= self.blndrDamage


    def __attack(self, enemyList):
        self.attacking = True
        cenChar = (self.POS[0] + self.SIZE//2, self.POS[1] + self.SIZE//2)
        self.timeAttacked = pygame.time.get_ticks()
        self.HIT_SWRD_ANIM.play()
        self.SOUND.Char.playSlash()
        
        tempL = []
        for enemy in enemyList:
            tempL.append(enemy.RECT)
        
        endPos = (-(round(math.cos((self.FACING- 90)/57.32) * self.swrdRad)),
                    round(math.sin((self.FACING - 90)/57.32) * self.swrdRad))
        endPos = (endPos[0] + cenChar[0], endPos[1] + cenChar[1])
        
        tempSwrdColObject = SwordCollison(tempL, cenChar, self.swrdRad, 
                                 (cenChar, endPos))
        
        hitBoxes = tempSwrdColObject.returnResult()
        del tempSwrdColObject
        
        if hitBoxes != []:
            for enemy in enemyList:
                if enemy.RECT in hitBoxes:
                    enemy.health -= self.swrdDamage
                    
    def __updateAttack(self):
        if self.attacking: 
            if pygame.time.get_ticks() - self.timeAttacked > self.swrdDelay * 1000:
                self.attacking = False
                self.HIT_SWRD_ANIM.stop()
    
    def __updateDash(self): # call once per update to check for ending the dash
        if self.dashing:
            if pygame.time.get_ticks() - self.__DashedAtTime > self.dashtime*1000:
                self.speed -= self.BASESPEED * self.dashmodifier
                self.dashing = False
                
    def __updateFire(self):
        if self.firing:
            if pygame.time.get_ticks() - self.__FiredAtTime > self.blndrDelay*1000:
                self.firing = False
                self.FIRE_BLNDR_ANIM.stop()
                
    def __updateStamina(self): # call once per update to regen stamina
        if self.stamina < self.staminaMax:
            self.stamina += self.staminaRegen
            
    def __updateBaseImage(self):
        if self.attacking:
            self.ActiveImage = self.HIT_SWRD_ANIM.returnImage()
        elif self.firing:
            self.ActiveImage = self.FIRE_BLNDR_ANIM.returnImage()
        elif self.moving and self.equiped == 'swrd':
            self.ActiveImage = self.WALK_SWRD_ANIM.returnImage()
        elif self.moving and self.equiped == 'blndr':
            self.ActiveImage = self.WALK_BLNDR_ANIM.returnImage()
        elif not self.moving and self.equiped == 'swrd':
            self.ActiveImage = self.STAND_SWORD_IMAGE
        elif not self.moving and self.equiped == 'blndr':
            self.ActiveImage = self.STAND_BLNDR_IMAGE
            
    def __updateDamaged(self):
        if self.health < self.oldHealth:
            self.SOUND.Char.playDamage()
        
        self.oldHealth = self.health
        
    def returnBlitPos(self, displayRect):
        x1, y1 = self.IMAGE.get_size()
        x = (self.POS[0] - (x1//2 - self.SIZE//2)) - displayRect[0]
        y = (self.POS[1] - (y1//2 - self.SIZE//2)) - displayRect[1]
        return (x,y)
      
    def update(self, mousePos, events, pressed, screenRect, colRects, enemyList):
        self.__updateBaseImage()
        self.__getSurfRot(screenRect, mousePos)
        
        self.__updateStamina()
        self.__updateDash()
        self.__updateAttack()
        self.__updateFire()
        self.__updateDamaged()
        self.__checkControls(events, pressed, screenRect, colRects, enemyList)
        
    
    def returnImage(self):
        if self.active:
            return self.IMAGE
