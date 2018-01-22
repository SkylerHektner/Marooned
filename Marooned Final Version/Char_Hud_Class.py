# Char_Hud_Class.py
# Team Windstorm
# Sprign 2016

import pygame
from pygame.locals import Rect

class CHAR_HUD(object):
    
    def __init__(self, HP, stamina, ammo, healthTotal, staminaTotal, mapName, tileSize, surf):
        
        self.stamina = stamina
        self.health = HP
        self.ammo = ammo
        self.staminaTotal = staminaTotal
        self.healthTotal = healthTotal
        self.SURF = surf
        
        x,y = self.SURF.get_size()
        
        self.width = x//15
        self.height = y//60
        self.borderWidth = self.width//40
        self.tbsize = 75
        
        self.swrdImg, self.blndrImg = self.instantiateTb()
        self.equiped = 0
        self.swrdHL = 1
        self.blndrHL = 0
       
        self.tbPos = (x//2 - self.tbsize, y - self.tbsize)
        self.tbPos2 = (x//2, y - self.tbsize)
        self.tbTxtPos = (x//2 + x//14 - x//50, y - self.tbsize + self.tbsize//3)
        self.healthBarPos = (self.tbPos[0] - self.tbsize - self.tbsize//2 - x//90, self.tbPos[1] + x//70)
        self.staminaBarPos = ( self.tbPos[0] - self.tbsize - self.tbsize//2 - x//90, self.tbPos[1] + x//70 + x//70)
        
        self.RED = (230,10,10)
        self.WHITE = (230,230,230)
        self.GREY = (96,96,96)
        self.BLACK = (0,0,0)
        self.GREEN = (0,255,0)
        
        self.ammoFSIZE = x//90
        self.ammoFont = pygame.font.SysFont('Arial', self.ammoFSIZE)
        
        mapName = mapName[0:mapName.find('.')] + 'Mini.png'
        self.MiniMap = pygame.image.load(mapName)
        self.MiniMap = self.MiniMap.convert_alpha()
        self.TILESIZE = tileSize
        self.MiniMapX = x - 25 - self.MiniMap.get_size()[0]
        self.MiniMapY = 25
        
    def changeHealthTotal(self, newValue):
        self.healthTotal = newValue
    
    def changeStaminaTotal(self, newValue):
        self.staminaTotal = newValue
        
    def instantiateTb(self):
        tbImg1 = [pygame.image.load('Resources/Sprites/tb_sword.png'), pygame.image.load('Resources/Sprites/tb_sword_sel.png')]
        tbImg2 = [pygame.image.load('Resources/Sprites/tb_blunder.png'), pygame.image.load('Resources/Sprites/tb_blunder_sel.png')]
        
        return tbImg1, tbImg2
    
    def tbImgSwitch(self, equiped):
        if equiped == 0:
            self.swrdHL = 1
            self.blndrHL = 0
        elif equiped == 1:
            self.swrdHL = 0
            self.blndrHL = 1
            
    #Text rendering
    def fontRender(self, font, string):
        text = font.render(string, True, self.GREY, None)
        return text    
    
    def __setPixels(self, surf, xy, size = 3):
        for x in range(size):
            for y in range(size):
                surf.set_at((xy[0] - size//2 + x,
                             xy[1] - size//2 + y), self.RED)
                
        return surf

    def update(self, HP, stamina, ammo, equiped, pos):
        self.health = HP
        self.stamina = stamina
        self.ammo = ammo
        
        if equiped == 'swrd': self.equiped = 0
        else: self.equiped = 1
        
        # Draw HP Bar
        temp = int((self.health/self.healthTotal) * self.width)
        pygame.draw.rect(self.SURF, self.RED, Rect(self.healthBarPos[0], self.healthBarPos[1],  temp, self.height))
        pygame.draw.rect(self.SURF, self.BLACK, Rect(self.healthBarPos[0] - self.borderWidth,
                                                     self.healthBarPos[1] - self.borderWidth,
                                                     self.width + 2 * self.borderWidth,
                                                     self.height + 2 * self.borderWidth), 2 * self.borderWidth)
        
        # Draw Stamina Bar
        temp = int((self.stamina/self.staminaTotal) * self.width)
        pygame.draw.rect(self.SURF, self.GREEN, Rect(self.staminaBarPos[0], self.staminaBarPos[1],  temp, self.height))
        pygame.draw.rect(self.SURF, self.BLACK, Rect(self.staminaBarPos[0] - self.borderWidth,
                                                     self.staminaBarPos[1] - self.borderWidth,
                                                     self.width + 2 * self.borderWidth,
                                                     self.height + 2 * self.borderWidth), 2 * self.borderWidth)
        
        # Draw toolbar
        self.tbImgSwitch(self.equiped)
        self.SURF.blit(self.swrdImg[self.swrdHL], (self.tbPos[0], self.tbPos[1]))
        self.SURF.blit(self.blndrImg[self.blndrHL], (self.tbPos2[0], self.tbPos2[1]))
        ammoTxt = self.fontRender(self.ammoFont, 'x ' + str(self.ammo))
        self.SURF.blit(ammoTxt, self.tbTxtPos)
        
        # Draw MiniMap
        pygame.draw.rect(self.SURF, self.BLACK, Rect(self.MiniMapX - 10, self.MiniMapY - 10, self.MiniMap.get_size()[0] + 20, self.MiniMap.get_size()[1] + 20))
        temp = self.MiniMap.copy()
        xy = (pos[0]//self.TILESIZE, pos[1]//self.TILESIZE)
        self.__setPixels(temp, xy, size = 5)
        self.SURF.blit(temp, (self.MiniMapX, self.MiniMapY))
        
       
        

        
        
        
        