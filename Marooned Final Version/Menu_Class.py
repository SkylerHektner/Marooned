# Menu_Class.py
# Spring 2016
# Team

import pygame, sys
from pygame.locals import *

class Menu(object):
    
    def __init__(self, DISPLAYSURF):
        
        #Surface & Mouse
        self.SURF = DISPLAYSURF
        self.x,self.y = self.SURF.get_size()
        self.mouseXY = (0,0)
        
        #Menu Button Creation
        self.menuON = True
        self.menButt = self.menuButton()
        self.mbSize = (200, 100)
        self.ngmbPos = (self.x//2 - self.mbSize[0]//2, self.y//2)
        self.qgmbPos = (self.x//2 - self.mbSize[0]//2, self.y//2 + self.mbSize[1] - 10)
        
        #Menu Font Creation
        self.WHITE = (255, 255, 255)
        self.GREY = (206, 206, 206)
        self.fontSize = [35, 150]        
        self.font = self.gameFont(self.fontSize[0])
        self.font2 = self.gameFont(self.fontSize[1])
        self.menuStrings = ['New Game', 'Quit Game', 'MAROONED', 'Resume Game']
        self.ngTxt = self.fontRender(self.font, self.menuStrings[0])
        self.ngPos = (self.x//2 - self.mbSize[0]//2 + self.fontSize[0], self.y//2 + self.fontSize[0]//2 + 10)
        self.resTxt = self.fontRender(self.font, self.menuStrings[3])
        self.resPos = (self.x//2 - self.mbSize[0]//2 + 5, self.y//2 + self.fontSize[0]//2 + 10)
        self.qgTxt = self.fontRender(self.font, self.menuStrings[1])
        self.qgPos = (self.x//2 - self.mbSize[0]//2 + self.fontSize[0], self.y//2 + self.mbSize[1] + self.fontSize[0]//2)
        self.titleTxt = self.fontRender2(self.font2, self.menuStrings[2])
        self.titlePos = (self.x//2 - self.fontSize[1]*2 - self.fontSize[0]*2, self.fontSize[1])
        self.backg = self.createBKGPIC()
        
        #Button Bools
        self.quitGame = False
        self.newGame = False
        
    #Create a method for button clicking
    def clicked(self, POS, SIZE, MOUSEXY):
        yesNo = False
        P1 = POS
        W, H = SIZE
        P2 = (POS[0] + W, P1[1] + H)
        yesNo = (P1[0] <= MOUSEXY[0] <= P2[0] and
                 P1[1] <= MOUSEXY[1] <= P2[1])

        return yesNo

    #Font creation
    def gameFont(self, size):
        font = pygame.font.SysFont('Arial', size)
        return font

    #Text rendering
    def fontRender(self, font, string):
        text = font.render(string, True, self.WHITE, None)
        return text
    
    #Grey text rendering
    def fontRender2(self, font, string):
        text = font.render(string, True, self.GREY, None)
        return text
    
    #Instantiate the background for the title screen
    def createBKGPIC(self):
        image = pygame.image.load('Resources/Sprites/title_backg.jpeg')
        image = pygame.transform.scale(image, (self.x, self.y))
        image.fill((0,0,0,255))
        return image
    
    #Blits the backg image
    def displayBKGPIC(self):
        self.SURF.blit(self.backg, (0,0))
    
    #Instantiate a button image
    def menuButton(self):
        menButt = pygame.image.load('Resources/Sprites/blue_bar.png')
        return menButt

    #New Game Menu button display
    def ngButtDisplay(self, MOUSEXY):
        yesNo = self.clicked(self.ngmbPos, self.mbSize, MOUSEXY)
        self.SURF.blit(self.menButt, self.ngmbPos)
        return yesNo
    
    #Quit Game Menu button display
    def qgButtDisplay(self, MOUSEXY):
        yesNo = self.clicked(self.qgmbPos, self.mbSize, MOUSEXY)
        self.SURF.blit(self.menButt, self.qgmbPos)
        return yesNo    
    
    #Display text straight to the main screen
    def textDisplay(self, text, pos):
        self.SURF.blit(text, pos)
        
    def buttonHandle(self):
        if self.newGame == True:
            self.menuON = False
        elif self.quitGame == True:
            pygame.quit()
            sys.exit()
        
    #Displays the menu
    def display(self):
        
        while self.menuON == True:
            
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    self.mouseXY = pygame.mouse.get_pos()
            
            self.displayBKGPIC()
            self.newGame = self.ngButtDisplay(self.mouseXY)
            self.textDisplay(self.ngTxt, self.ngPos)
            self.quitGame = self.qgButtDisplay(self.mouseXY)
            self.textDisplay(self.qgTxt, self.qgPos)
            self.textDisplay(self.titleTxt, self.titlePos)
            self.buttonHandle()
                    
            pygame.display.flip()
            pygame.time.wait(300)
            
            
    def pauseDisplay(self):
        
        self.menuON = True
        self.mouseXY = (0,0)
        
        while self.menuON == True:
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    self.mouseXY = pygame.mouse.get_pos()
               
            
            self.displayBKGPIC()
            self.newGame = self.ngButtDisplay(self.mouseXY)
            self.textDisplay(self.resTxt, self.resPos)
            self.quitGame = self.qgButtDisplay(self.mouseXY)
            self.textDisplay(self.qgTxt, self.qgPos)
            self.textDisplay(self.titleTxt, self.titlePos)
            self.buttonHandle()
                    
            pygame.display.flip()   
            pygame.time.wait(300)
     
            
            
        