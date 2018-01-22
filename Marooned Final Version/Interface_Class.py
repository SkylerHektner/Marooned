# Level_Class.py
# Spring 2016
# Team

import pygame
from pygame.locals import *
from Map_Class import Map, mapNew
from Char_Class import Char
from Char_Hud_Class import CHAR_HUD
from HeadHunter_Class import HeadHunter
from MapSprite_Classes import LargeTree, MediumTree, Hut, firePit, Boat, MediumRock, LargeRock, TreasureChest
from Witch_Doctor_Class import WitchDoctor
from Brute_Class import Brute
from Consumable_Class import consumableAmmo, consumableHealth
from Sound_Class import SoundController

class Level(object):

    def __init__(self, DISPLAYSURF, mapName, mapPixX, mapPixY):
        self.DISPLAYSURF = DISPLAYSURF
        self.DISPLAYSIZE = list(DISPLAYSURF.get_size())
        self.DISPLAYPOS = [0,0]
        self.DISPLAYRECT = Rect(self.DISPLAYPOS + self.DISPLAYSIZE)
        self.THROTTLERECT = self.DISPLAYRECT.inflate(self.DISPLAYRECT[2] * 3, self.DISPLAYRECT[3] * 3)
        self.win = False
        
        self.SOUNDCONT = SoundController()
        
        # Creates the Map class (This will get deleted then changed when the character moves to new islands)
        self.showLoadScreen()
        self.TILESIZE = self.DISPLAYSIZE[0]//12
        self.MAP = mapNew(mapName, mapPixX, mapPixY, self.TILESIZE)
        

        self.mapCollisionRects = self.MAP.getCollisionRects()

        # Create Character
        charSpawn = self.MAP.getPlayerSpawnPos()
        self.CHAR = Char(charSpawn, self.TILESIZE, self.SOUNDCONT)
        self.CHARHUD = CHAR_HUD(self.CHAR.health, self.CHAR.stamina, self.CHAR.ammo, self.CHAR.healthMax, self.CHAR.staminaMax,
                                mapName, self.TILESIZE, self.DISPLAYSURF)
        
        self.DARTLIST = [] #Used to keep track of darts on screen   
        
        self.__LoadAllEntities()
        
        self.SOUNDCONT.Music.PlayingMusic.play(loops = -1)
                
        self.endLoadScreen()
        
    def __LoadAllEntities(self):
        # LOAD MOBS
        self.MOBLIST = []
        # Load HeadHunters
        mobPositions = self.MAP.getSpawnPositions('HeadHunter')
        for pos in mobPositions:
            self.MOBLIST.append(HeadHunter(self.TILESIZE, pos, self.SOUNDCONT))
            
        # Load WitchDoctors
        mobPositions = self.MAP.getSpawnPositions('WitchDoctor')
        for pos in mobPositions:
            self.MOBLIST.append(WitchDoctor(self.TILESIZE, pos, self.SOUNDCONT))
        
        # Load Brutes
        mobPositions = self.MAP.getSpawnPositions('Brute')
        for pos in mobPositions:
            self.MOBLIST.append(Brute(self.TILESIZE, pos, self.SOUNDCONT))  
         
        # LOAD NON MOB DYNAMIC OBJECTS    
        # Load Trees
        self.TREELIST = []
        treePositions = self.MAP.getSpawnPositions('LargeTree')
        for pos in treePositions:
            self.TREELIST.append(LargeTree(self.TILESIZE, pos))
        treePositions = self.MAP.getSpawnPositions('MediumTree')
        for pos in treePositions:
            self.TREELIST.append(MediumTree(self.TILESIZE, pos))
        
        # Load Huts
        self.HUTLIST = []
        hutPositions = self.MAP.getSpawnPositions('HutDown')
        for pos in hutPositions:
            self.HUTLIST.append(Hut(self.TILESIZE, pos, self.SOUNDCONT, facing = 'down'))
        hutPositions = self.MAP.getSpawnPositions('HutUp')
        for pos in hutPositions:
            self.HUTLIST.append(Hut(self.TILESIZE, pos, self.SOUNDCONT, facing = 'up'))
        hutPositions = self.MAP.getSpawnPositions('HutLeft')
        for pos in hutPositions:
            self.HUTLIST.append(Hut(self.TILESIZE, pos, self.SOUNDCONT, facing = 'left'))            
        hutPositions = self.MAP.getSpawnPositions('HutRight')
        for pos in hutPositions:
            self.HUTLIST.append(Hut(self.TILESIZE, pos, self.SOUNDCONT, facing = 'right')) 
        
        # Load firePits
        self.PITLIST = []
        pitPositions = self.MAP.getSpawnPositions('firePit')
        for pos in pitPositions:
            self.PITLIST.append(firePit(self.TILESIZE, pos, self.SOUNDCONT))
            
        # Load Boring Things (boat and rocks)
        self.BORINGLIST = []
        
        positions = self.MAP.getSpawnPositions('boatUp')
        for pos in positions:
            self.BORINGLIST.append(Boat(self.TILESIZE, pos, facing = 'up'))
        positions = self.MAP.getSpawnPositions('boatDown')
        for pos in positions:
            self.BORINGLIST.append(Boat(self.TILESIZE, pos, facing = 'down'))
        positions = self.MAP.getSpawnPositions('boatLeft')
        for pos in positions:
            self.BORINGLIST.append(Boat(self.TILESIZE, pos, facing = 'left'))   
        positions = self.MAP.getSpawnPositions('boatRight')
        for pos in positions:
            self.BORINGLIST.append(Boat(self.TILESIZE, pos, facing = 'right'))  
        positions = self.MAP.getSpawnPositions('MediumRock')
        for pos in positions:
            self.BORINGLIST.append(MediumRock(self.TILESIZE, pos))  
        positions = self.MAP.getSpawnPositions('LargeRock')
        for pos in positions:
            self.BORINGLIST.append(LargeRock(self.TILESIZE, pos)) 
            
        # LOAD CONSUMABLES
        self.CONS_LIST = []
        
        # Load consumableHealth
        consPositions = self.MAP.getSpawnPositions('consumableHealth')
        for pos in consPositions:
            self.CONS_LIST.append(consumableHealth(pos, self.TILESIZE, self.SOUNDCONT))  
                
        # Load consumableAmmo
        consPositions = self.MAP.getSpawnPositions('consumableAmmo')
        for pos in consPositions:
            self.CONS_LIST.append(consumableAmmo(pos, self.TILESIZE, self.SOUNDCONT)) 
            
        # LOAD TREASURE CHEST
        temp = self.MAP.getChest()
        self.TREASURECHEST = TreasureChest(temp[0], self.TILESIZE, self.SOUNDCONT, facing = temp[1][5:])

    def showLoadScreen(self): # Blits the load screen and plays us some nice music (:
        temp = pygame.image.load('Resources/loading.png')
        temp = pygame.transform.scale(temp, self.DISPLAYSIZE)
        self.DISPLAYSURF.blit(temp, (0,0))
        pygame.display.flip()

    def endLoadScreen(self): # Stops the music
        pygame.mixer.music.fadeout(2000)
        
    def DeathAnim(self, events, pressed):
        self.SOUNDCONT.Music.PlayingMusic.stop()
        self.SOUNDCONT.Music.DeathMusic.play()
        
        spawn = self.MAP.getPlayerSpawnPos()
        del self.CHAR
        self.CHAR = Char(spawn, self.TILESIZE, self.SOUNDCONT)
        self.CHAR.update(pygame.mouse.get_pos(), events, pressed, self.DISPLAYRECT, 
                           self.mapCollisionRects + self.MOBCOLLISONRECTS, self.MOBLIST)
        
        self.__LoadAllEntities()
        
        tempSurf = pygame.surface.Surface((self.DISPLAYRECT[2], self.DISPLAYRECT[3]), flags = SRCALPHA, depth = 32)
        tempSurf.fill((255,0,0,10))
        textGen = pygame.font.SysFont('Ariel', self.DISPLAYRECT[2]//10, bold = 1)
        x,y = textGen.size('YOU DIED')
        DeathText = textGen.render('YOU DIED', True, (255,70,70))
        
        for x in range(80):
            self.DISPLAYSURF.blit(tempSurf, (0,0))
            self.DISPLAYSURF.blit(DeathText, (self.DISPLAYRECT[2]//2 - x//3, self.DISPLAYRECT[3]//2 - y//2))
            pygame.time.wait(40)
            pygame.display.flip()
            
        self.SOUNDCONT.Music.PlayingMusic.play(loops = -1)
        
    def __updateDisplayRects(self):
        self.DISPLAYPOS = [self.CHAR.POS[0] - self.DISPLAYSIZE[0]//2 + self.CHAR.SIZE//2,
                           self.CHAR.POS[1] - self.DISPLAYSIZE[1]//2 + self.CHAR.SIZE//2]
        
        self.DISPLAYRECT = Rect(self.DISPLAYPOS + self.DISPLAYSIZE)
        
        self.THROTTLERECT = self.DISPLAYRECT.inflate(self.DISPLAYRECT[2] * 3, self.DISPLAYRECT[3] * 3)
        
    def update(self, pressed, events):
        # Check Mob List for actions that need to be taken
        for mob in self.MOBLIST:
            if mob.health < 0: # Delete dead mobs
                self.MOBLIST.pop(self.MOBLIST.index(mob))
            if type(mob) is WitchDoctor: # Checks to see if any witch doctors fired a dart
                temp = mob.checkDartReturn(self.DISPLAYRECT, self.CHAR.POS)
                if temp[0]:
                    self.DARTLIST.append(temp[1])
        
        # Check for consumed consumables and remove them
        for cons in self.CONS_LIST:
            if cons.CONSUMED:
                self.CONS_LIST.pop(self.CONS_LIST.index(cons))       
        
        # Update displayRect, and blit over map
        self.__updateDisplayRects()
        self.MAP.blitToDisplaySurf(self.DISPLAYSURF, self.DISPLAYRECT)
        
        # Get proximal collision rects
        self.MOBCOLLISONRECTS = []
        for mob in self.MOBLIST:
            if mob.RECT.colliderect(self.THROTTLERECT):
                self.MOBCOLLISONRECTS.append(mob.RECT)
            
        mapColRects = []    
        for rect in self.mapCollisionRects:
            if rect.colliderect(self.THROTTLERECT):
                mapColRects.append(rect)
        
        # Update all Darts
        for dart in self.DARTLIST:
            dart.update(self.DISPLAYRECT, self.CHAR)
            if dart.onScreen:
                self.DISPLAYSURF.blit(dart.returnImage(), dart.returnBlitPos(self.DISPLAYRECT))
            if not dart.onScreen or dart.hit:
                self.DARTLIST.pop(self.DARTLIST.index(dart))

        # Update Player
        self.CHAR.update(pygame.mouse.get_pos(), events, pressed, self.DISPLAYRECT, 
                         mapColRects + self.MOBCOLLISONRECTS, self.MOBLIST)
        
        if self.CHAR.health <= 0:
            self.DeathAnim(events, pressed)
        
        # Update all mobs and Blit all on screen Mobs
        for mob in self.MOBLIST:
            mob.update(self.DISPLAYRECT, self.CHAR, mapColRects + self.MOBCOLLISONRECTS + [self.CHAR.RECT])
            if mob.onScreen:
                self.DISPLAYSURF.blit(mob.returnImage(), mob.returnBlitPos(self.DISPLAYRECT))
         
        # Update/blit Charhud and blit Char
        self.DISPLAYSURF.blit(self.CHAR.returnImage(), self.CHAR.returnBlitPos(self.DISPLAYRECT))
        
        # Update/Blit/test huts for spawn
        for hut in self.HUTLIST:
            hut.update(self.DISPLAYRECT)
            if hut.onScreen:
                self.DISPLAYSURF.blit(hut.returnImage(), hut.returnBlitPos(self.DISPLAYRECT))
                temp = hut.checkSpawn(self.DISPLAYRECT)
                if temp[0]:
                    self.MOBLIST.append(temp[1])
                    
        # Update and blit any firePits
        for pit in self.PITLIST:
            pit.update(self.DISPLAYRECT)
            if pit.onScreen:
                self.DISPLAYSURF.blit(pit.returnImage(), pit.returnBlitPos(self.DISPLAYRECT))
                
        # Update and blit all boring things (rocks, boat, etc..)
        for bor in self.BORINGLIST:
            bor.update(self.DISPLAYRECT)
            if bor.onScreen:
                self.DISPLAYSURF.blit(bor.returnImage(), bor.returnBlitPos(self.DISPLAYRECT))
                
        # Update and display consumables
        for cons in self.CONS_LIST:
            cons.update(self.DISPLAYRECT)
            if cons.onScreen:
                cons.collideChar(self.CHAR)
                self.DISPLAYSURF.blit(cons.returnImage(), cons.returnBlitPos(self.DISPLAYRECT))
                
        # Update and display Treasure Chest
        self.TREASURECHEST.update(self.DISPLAYRECT, self.CHAR.RECT, self.DISPLAYSURF)
        if self.TREASURECHEST.win:
            self.win = True
            return
        
        if self.TREASURECHEST.onScreen:
            self.DISPLAYSURF.blit(self.TREASURECHEST.returnImage(), self.TREASURECHEST.returnBlitPos(self.DISPLAYRECT))
        
        # Update and Blit trees(they have to blit over the char)
        for tree in self.TREELIST:
            tree.update(self.DISPLAYRECT)
            if tree.onScreen:
                self.DISPLAYSURF.blit(tree.returnImage(), tree.returnBlitPos(self.DISPLAYRECT))
        
        # Update and Blit CharHud
        self.CHARHUD.update(self.CHAR.health, self.CHAR.stamina, self.CHAR.ammo, self.CHAR.equiped, self.CHAR.POS)
        
        # Update Display
        pygame.display.flip()

