import pygame
from pygame.locals import *
import sys

class NarrativeScroller(object):
    
    def __init__(self, surf, textFileName):
        
        self.SURF = surf
        file = open(textFileName, 'r')
        size = surf.get_size()[0]
        size = size//25
        self.POS = [0, surf.get_size()[1]//2]
        
        textGenerator = pygame.font.SysFont('Ariel', size, bold=1)
        
        textSurfacelist = []
        
        black = (0, 0, 0, 0)
        self.white = (150, 150, 150, 0)
        
        y = 0
        
        for line in file:
            textSurfacelist.append(textGenerator.render(line, True, black))
            
        for surface in textSurfacelist:
            y += surface.get_size()[1]
            
        self.masterSurf = pygame.surface.Surface((surf.get_size()[0], y), depth=32, flags=SRCALPHA)
        
        y = 0
        
        for surface in textSurfacelist:
            self.masterSurf.blit(surface, (0, y))
            y += surface.get_size()[1]
            
        
            
    def display(self):
        pygame.mixer.music.load('Resources/Sound/Music/Music_Box.wav')
        pygame.mixer.music.play()
        while True:
            
            self.SURF.fill(self.white)
            self.SURF.blit(self.masterSurf, self.POS)
            self.POS[1] -= 1
            
            pygame.time.wait(17)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    return
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    return
                
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                
        
        
        
    
