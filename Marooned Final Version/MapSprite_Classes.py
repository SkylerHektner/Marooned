# MapSprite_Classes.py
# Team Windstorm
# spring 2016

import pygame, sys
from pygame.locals import *
import random
from HeadHunter_Class import HeadHunter
from Pyganim import PygAnimation

class LargeTree(object):
    
    def __init__(self, tileSize, pos):
        
        self.POS = list(pos)
        self.SIZE = tileSize * 5
        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])  
        self.onScreen = False
        
        # Load image
        rTree = str(random.randint(1, 3))
        self.IMAGE = pygame.image.load('Resources/Sprites/Map_Sprites/large_tree' + rTree + '.png')
        self.IMAGE = pygame.transform.scale(self.IMAGE, (self.SIZE, self.SIZE))
        self.IMAGE = self.IMAGE.convert_alpha()
        
        r = random.randint(0,3)
        self.IMAGE = pygame.transform.rotate(self.IMAGE, r * 90)
        
    def returnBlitPos(self, displayRect):
        x1, y1 = self.IMAGE.get_size()
        x = (self.POS[0] - (x1//2 - self.SIZE//2)) - displayRect[0]
        y = (self.POS[1] - (y1//2 - self.SIZE//2)) - displayRect[1]
        
        return (x,y)
                
    def update(self, screenRect):
        self.onScreen = self.RECT.colliderect(screenRect)
        
    def returnImage(self):
        return self.IMAGE
    
class MediumTree(object):
    
    def __init__(self, tileSize, pos):
        
        self.POS = list(pos)
        self.SIZE = tileSize * 3
        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])  
        self.onScreen = False
        
        # Load image
        rTree = str(random.randint(1, 3))
        self.IMAGE = pygame.image.load('Resources/Sprites/Map_Sprites/small_tree' + rTree + '.png')
        self.IMAGE = pygame.transform.scale(self.IMAGE, (self.SIZE, self.SIZE))
        self.IMAGE = self.IMAGE.convert_alpha()
        
        r = random.randint(0,3)
        self.IMAGE = pygame.transform.rotate(self.IMAGE, r * 90)
        
    def returnBlitPos(self, displayRect):
        x1, y1 = self.IMAGE.get_size()
        x = (self.POS[0] - (x1//2 - self.SIZE//2)) - displayRect[0]
        y = (self.POS[1] - (y1//2 - self.SIZE//2)) - displayRect[1]
        
        return (x,y)
                
    def update(self, screenRect):
        self.onScreen = self.RECT.colliderect(screenRect)
        
    def returnImage(self):
        return self.IMAGE
    
    
class Hut(object):
    
    def __init__(self, tileSize, pos, soundController, facing = 'down'):
            
        self.POS = list(pos)
        self.SIZE = tileSize * 3
        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])  
        self.onScreen = False
        self.FACING = facing
        self.CenHut = (self.POS[0] + self.SIZE//2, self.POS[1] + self.SIZE//2)
        self.SpawnRange = .3 # The portion of the screeen width the player must be close to the hut for spawning to occur
        self.TILESIZE = tileSize
        self.SPAWNED = False
        self.SOUND = soundController
        
        
        # Load image
        self.IMAGE = pygame.image.load('Resources/Sprites/Map_Sprites/hut.png')
        self.IMAGE = pygame.transform.scale(self.IMAGE, (self.SIZE, self.SIZE))
        self.IMAGE = self.IMAGE.convert_alpha()  
        
        # Mob Spawn Inst:
        if self.FACING == 'down':
            r = 0
            self.MOBSPAWN = (self.POS[0] + tileSize, self.POS[1] + tileSize * 3)
        elif self.FACING == 'left':
            r = 270
            self.MOBSPAWN = (self.POS[0] - tileSize, self.POS[1] + tileSize)
        elif self.FACING == 'up':
            r = 180
            self.MOBSPAWN = (self.POS[0] + tileSize, self.POS[1] - tileSize)
        elif self.FACING == 'right':
            r = 90
            self.MOBSPAWN = (self.POS[0] + tileSize * 3, self.POS[1] + tileSize)
            
        self.IMAGE = pygame.transform.rotate(self.IMAGE, r)
            
        
    def returnBlitPos(self, displayRect):
        x1, y1 = self.IMAGE.get_size()
        x = (self.POS[0] - (x1//2 - self.SIZE//2)) - displayRect[0]
        y = (self.POS[1] - (y1//2 - self.SIZE//2)) - displayRect[1]
        
        return (x,y)
    
    def checkSpawn(self, screenRect):
        cenScreen = (screenRect[0] + screenRect[2]//2, screenRect[1] + screenRect[3]//2)
        if not self.SPAWNED and ((self.CenHut[0] - cenScreen[0])**2 + (self.CenHut[1] - cenScreen[1])**2)**.5 < screenRect[2] * self.SpawnRange:
            result = (True, HeadHunter(self.TILESIZE, self.MOBSPAWN, self.SOUND))
            self.SPAWNED = True
        else:
            result = (False, None)
            
        return result
                
    def update(self, screenRect):
        self.onScreen = self.RECT.colliderect(screenRect)
        
    def returnImage(self):
        return self.IMAGE   
    
class Boat(object):
    
    def __init__(self, tileSize, pos, facing = 'down'):
            
        self.POS = list(pos)
        self.SIZE = tileSize * 5
        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])  
        self.onScreen = False
        
        # Load image
        self.IMAGE = pygame.image.load('Resources/Sprites/Map_Sprites/boat1.png')
        self.IMAGE = pygame.transform.scale(self.IMAGE, (self.SIZE, self.SIZE))
        self.IMAGE = self.IMAGE.convert_alpha()
        
        # Rotation
        if facing == 'down': r = 0
        elif facing == 'left': r = 270
        elif facing == 'up': r = 180
        elif facing == 'right': r = 90
            
        self.IMAGE = pygame.transform.rotate(self.IMAGE, r)
            
    def returnBlitPos(self, displayRect):
        x1, y1 = self.IMAGE.get_size()
        x = (self.POS[0] - (x1//2 - self.SIZE//2)) - displayRect[0]
        y = (self.POS[1] - (y1//2 - self.SIZE//2)) - displayRect[1]
        
        return (x,y)
                
    def update(self, screenRect):
        self.onScreen = self.RECT.colliderect(screenRect)
        
    def returnImage(self):
        return self.IMAGE
    
class MediumRock(object):
    
    def __init__(self, tileSize, pos):
            
        self.POS = list(pos)
        self.SIZE = tileSize * 3
        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])  
        self.onScreen = False
        
        # Load image
        sheet = pygame.image.load('Resources/Sprites/Map_Sprites/medium_rock_spritesheet.png')
        sheet = pygame.transform.scale(sheet, (self.SIZE * 6, self.SIZE))
        sheet = sheet.convert_alpha()
        r = random.randint(0,5)
        self.IMAGE = pygame.surface.Surface((self.SIZE, self.SIZE), flags = SRCALPHA, depth = 32)
        self.IMAGE.blit(sheet, (0,0), area = Rect(r * self.SIZE, 0, self.SIZE, self.SIZE))
            
    def returnBlitPos(self, displayRect):
        x1, y1 = self.IMAGE.get_size()
        x = (self.POS[0] - (x1//2 - self.SIZE//2)) - displayRect[0]
        y = (self.POS[1] - (y1//2 - self.SIZE//2)) - displayRect[1]
        
        return (x,y)
                
    def update(self, screenRect):
        self.onScreen = self.RECT.colliderect(screenRect)
        
    def returnImage(self):
        return self.IMAGE
    
class LargeRock(object):
    
    def __init__(self, tileSize, pos):
            
        self.POS = list(pos)
        self.SIZE = tileSize * 5
        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])  
        self.onScreen = False
        
        # Load image
        sheet = pygame.image.load('Resources/Sprites/Map_Sprites/large_rock_spritesheet.png')
        sheet = pygame.transform.scale(sheet, (self.SIZE * 6, self.SIZE))
        sheet = sheet.convert_alpha()
        r = random.randint(0,5)
        self.IMAGE = pygame.surface.Surface((self.SIZE, self.SIZE), flags = SRCALPHA, depth = 32)
        self.IMAGE.blit(sheet, (0,0), area = Rect(r * self.SIZE, 0, self.SIZE, self.SIZE))
            
    def returnBlitPos(self, displayRect):
        x1, y1 = self.IMAGE.get_size()
        x = (self.POS[0] - (x1//2 - self.SIZE//2)) - displayRect[0]
        y = (self.POS[1] - (y1//2 - self.SIZE//2)) - displayRect[1]
        
        return (x,y)
                
    def update(self, screenRect):
        self.onScreen = self.RECT.colliderect(screenRect)
        
    def returnImage(self):
        return self.IMAGE
    
class firePit(object):
    
    def __init__(self, tileSize, pos, soundController):
            
        self.POS = list(pos)
        self.SIZE = tileSize
        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])  
        self.onScreen = False
        
        self.SOUND = soundController
        
        self.soundPlayed = False
        
        self.ActiveImage = None # Later assigned using Pyganim 
        
        self.__setUpPyganim()
        
    def __setUpPyganim(self):
        
        self.IMAGE_1 = self.__autoScaler(pygame.image.load('Resources/Sprites/firePit/1.png'))
        self.IMAGE_2 = self.__autoScaler(pygame.image.load('Resources/Sprites/firePit/2.png'))
        self.IMAGE_3 = self.__autoScaler(pygame.image.load('Resources/Sprites/firePit/3.png'))
        
        time = .2
        
        self.ANIM = PygAnimation([(self.IMAGE_1, time),
                                  (self.IMAGE_2, time),
                                  (self.IMAGE_3, time)])
        
        self.ANIM.play()
        
    def __autoScaler(self, image):
        image = pygame.transform.scale(image, (self.SIZE, self.SIZE))
        image = image.convert_alpha()
        return image
        
    def returnBlitPos(self, displayRect):
        x1, y1 = self.ActiveImage.get_size()
        x = (self.POS[0] - (x1//2 - self.SIZE//2)) - displayRect[0]
        y = (self.POS[1] - (y1//2 - self.SIZE//2)) - displayRect[1]
        return (x,y)
                
    def update(self, screenRect):
        self.onScreen = self.RECT.colliderect(screenRect)
        self.ActiveImage = self.ANIM.returnImage()
        
        if self.onScreen and not self.soundPlayed:
            self.SOUND.firePit.playFire()
            self.soundPlayed = True
        elif not self.onScreen and self.soundPlayed:
            self.SOUND.firePit.stopFire()
            self.soundPlayed = False
        
    def returnImage(self):
        return self.ActiveImage
    
class TreasureChest(object):
    
    def __init__(self, pos, tileSize, soundController, facing = 'Down'):
        
        self.POS = list(pos)
        self.SIZE = tileSize
        self.SOUND = soundController
        self.RECT = Rect(self.POS + [self.SIZE, self.SIZE])
        
        self.win = False
        self.onScreen = False
        
        if facing == 'Up': self.r = 0
        elif facing == 'Left': self.r = 90
        elif facing == 'Down': self.r = 180
        elif facing == 'Right': self.r = 270
        
        im1 = self.__autoScale(pygame.image.load('Resources/Sprites/chest/chest1.png'))
        im2 = self.__autoScale(pygame.image.load('Resources/Sprites/chest/chest2.png'))
        im3 = self.__autoScale(pygame.image.load('Resources/Sprites/chest/chest3.png'))
        self.ActiveImage = im1
        
        self.ANIM = PygAnimation([(im1, 1),
                                  (im2, 1),
                                  (im3, 15)])
        
    def __autoScale(self, image):
        image = pygame.transform.scale(image, (self.SIZE, self.SIZE))
        image = pygame.transform.rotate(image, self.r)
        image = image.convert_alpha()
        
        return image
        
    def update(self, screenRect, charRect, surf):
        self.onScreen = self.RECT.colliderect(screenRect)
        if self.RECT.colliderect(charRect):
            self.__winAnimation(surf, screenRect)
            
    def __winAnimation(self, surf, screenRect):
        self.SOUND.TreasureChest.Win.play()
        self.SOUND.Music.PlayingMusic.stop()
        GrowControl = 0
        tempClock = pygame.time.Clock()
        tempSurf = pygame.surface.Surface((screenRect[2], screenRect[3]), depth = 32, flags = SRCALPHA)
        tempSurf.fill((255,255,255,15))
        self.ANIM.play()
        
        for x in range(720):
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
            GrowControl += 1
            if GrowControl % 5 == 0:
                self.ActiveImage = self.ANIM.returnImage()
                self.ActiveImage = pygame.transform.scale(self.ActiveImage, (self.ActiveImage.get_size()[0] + GrowControl//4, 
                                                                             self.ActiveImage.get_size()[1] + GrowControl//4))
                surf.blit(tempSurf, (0,0))
                
            surf.blit(self.ActiveImage, self.returnBlitPos(screenRect))
            tempClock.tick(60)
            pygame.display.flip()
            
        self.win = True
        pygame.mixer.stop()
    
    def returnImage(self):
        return self.ActiveImage


    def returnBlitPos(self, displayRect):
        x1, y1 = self.ActiveImage.get_size()
        x = (self.POS[0] - (x1//2 - self.SIZE//2)) - displayRect[0]
        y = (self.POS[1] - (y1//2 - self.SIZE//2)) - displayRect[1]
        return (x,y)
    
        