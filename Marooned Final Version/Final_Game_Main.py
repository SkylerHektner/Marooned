# Final_Game_Main.py
# Spring 2016
# Team Windstorm

import pygame, sys
from pygame.locals import *
from Interface_Class import Level
from Menu_Class import Menu
from Nar_Class import NarrativeScroller

pygame.init()

def setUp(): # Set Basic Settings
    FPS = 60
    clock = pygame.time.Clock()
    resolution = (1600, 900)
    DISPLAYSURF = pygame.display.set_mode(resolution, DOUBLEBUF | HWSURFACE)
    pygame.display.set_caption('Marooned')
    Nar_Intro = NarrativeScroller(DISPLAYSURF, 'Resources/narrative.txt')
    Nar_Intro.display()
    return DISPLAYSURF, clock, FPS

def setAllowedEvents():
    pygame.event.set_allowed(None) # makes no events allowed
    pygame.event.set_allowed(MOUSEBUTTONDOWN) # Start setting what events we care about
    pygame.event.set_allowed(MOUSEBUTTONUP)
    pygame.event.set_allowed(KEYDOWN)
    pygame.event.set_allowed(KEYUP)
    pygame.event.set_allowed(QUIT)
    
def loadLevel(level, DISPLAYSURF):
    if level == 1:
        result = Level(DISPLAYSURF, 'Resources/Maps/Map1.png', 200, 50)
    elif level == 2:
        result = Level(DISPLAYSURF, 'Resources/Maps/Map2.png', 60, 60)
    elif level == 3:
        result = Level(DISPLAYSURF, 'Resources/Maps/Map3.png', 210, 120)
    else:
        pygame.quit()
        sys.exit()

    return result
    
def main():
    DISPLAYSURF, clock, FPS = setUp()
    MENU = Menu(DISPLAYSURF)
    MENU.display()
    currentLevel = 1
    LEVEL = loadLevel(currentLevel, DISPLAYSURF)

    # makes sure the pygame event list does not include events we don't need
    setAllowedEvents()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                MENU.pauseDisplay()

        pressed = pygame.key.get_pressed()
        LEVEL.update(pressed, events)
        clock.tick(FPS)
        
        if LEVEL.win:
            currentLevel += 1
            del LEVEL
            LEVEL = loadLevel(currentLevel, DISPLAYSURF)

if __name__ == '__main__': main()
