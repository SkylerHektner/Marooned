# Brute_Class.py
# Spring 2016
# Team Windstorm

import pygame
from pygame.locals import *
import math
from Pyganim import PygAnimation
from Sword_Collision_Class import SwordCollison
from HeadHunter_Class import HeadHunter

class Brute(HeadHunter):
    
    def __init__(self, tileSize, pos, soundController):
        
        self.POS = list(pos)
        self.SIZE = tileSize
        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])
        
        self.SOUND = soundController
        
        self.DAMAGESOUND = self.SOUND.Brute.playDamage
        self.CHASINGSOUND = self.SOUND.Brute.playChasing
        self.NOTICESOUND = self.SOUND.Brute.playNotice
        self.ATTACKSOUND = self.SOUND.Brute.playAttack        
        
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
        self.health = 150
        self.maxhealth = 150
        self.healthOld = self.health # Used to calculate if damage was damage in the knockback function
        
        self.damage = 20
        self.collidedCharDelay = 1 # the time, in seconds, the zombie stops after colliding with the player
        # Half way through the above delay the zombie will do damage to the character if they have not moved away
        self.SprRange = self.SIZE
        
        self.BASESPEED = 4
        self.speed = self.BASESPEED
        
        self.AgroRange = .4 # this is the portion of the X resolution the mob will start tracking at
        
        self.knockBackRange = self.SIZE//2 # the distance the zombie gets knocked back when it takes damage
        self.stunTime = 200 # time, in milleseconds, the enemy is stunned when it takes damage
        self.stunnedAtTime = 0
        self.stunRemaining = 0
        
        self.__setUpPyganim()
        
    def __setUpPyganim(self):
        self.STAND_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/brute/stand.png'), scaleTuple = (1,0.9))
        
        self.WALK_L_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/brute/WalkL.png'), scaleTuple = (1,0.9))
        self.WALK_R_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/brute/WalkR.png'), scaleTuple = (1,0.9))
        
        self.ATT_1_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/brute/Att1.png'), scaleTuple= (1.56,1.28))
        self.ATT_2_IMAGE = self.__autoScale(pygame.image.load('Resources/Sprites/brute/Att2.png'), scaleTuple= (1.56, 1.7))
        
        self.STUN_IMAGE = self.STAND_IMAGE # NEED TO REPLACE WITH ITS OWN STUN IMAGE
        
        walkTime = .2
        hitTime = self.collidedCharDelay/2
        
        self.WALK_ANIM = PygAnimation([(self.STAND_IMAGE, walkTime),
                                       (self.WALK_L_IMAGE, walkTime),
                                       (self.STAND_IMAGE, walkTime),
                                       (self.WALK_R_IMAGE, walkTime)])
        
        self.ATT_ANIM = PygAnimation([(self.ATT_1_IMAGE, hitTime),
                                      (self.ATT_2_IMAGE, hitTime)])
            
            
        
    def __autoScale(self, image, scaleTuple = (1,1)):
        x,y = image.get_size()
        image = pygame.transform.scale(image, (int(self.SIZE * scaleTuple[0]), int(self.SIZE * scaleTuple[1])))
        image = image.convert_alpha()
        return image    