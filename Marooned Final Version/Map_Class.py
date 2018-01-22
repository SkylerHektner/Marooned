# Map_Class.py
# Spring 2016
# Team

import pygame
from pygame.locals import *
from Tile_Class import Tile
import random

class Map(object):

    def __init__(self, mapFile, mapPixX, mapPixY, tileSize):

        #globals
        self.TILESIZE = tileSize
        self.MAPFILE = mapFile
        self.mapPixY = mapPixY
        self.mapPixX = mapPixX

        self.__preLoadTileImages()
        
        # Create the mapsurfaces and stores them in self.SURF_LIST
        # Also creates the mapRects and stores them in self.MAP_RECT_LIST
        self.maxTiles = 5000//self.TILESIZE # the max tiles in any mapSurface EG 50 --> (50,50)
        self.__createMapSurfaces()

        # Create the list of tile objects we will use for collision areas on the map
        self.TILELIST = self.__createMapTileList(mapPixY, mapPixX, tileSize, mapFile)

        # Call update on every tile in the tile list so they blit their image onto the map surface
        self.updateMapImage()

    def __preLoadTileImages(self): # Pre Loads and renders tile images for faster load times
        # The tile objects will take in these images and "point" to them instead of creating their own images for each tile

        self.TILESHEET = pygame.image.load('Resources/Tiles/tile_sheet.png')
        self.TILESHEET = pygame.transform.scale(self.TILESHEET, (self.TILESIZE * 10, self.TILESIZE * 3))
        self.TILESHEET = self.TILESHEET.convert_alpha()
        
        self.SMALL_ROCK_SHEET = pygame.image.load('Resources/Sprites/Map_Sprites/tiny_rock_spritesheet.png')
        self.SMALL_ROCK_SHEET = pygame.transform.scale(self.SMALL_ROCK_SHEET, (self.TILESIZE * 6, self.TILESIZE))
        self.SMALL_ROCK_SHEET = self.SMALL_ROCK_SHEET.convert_alpha()
        
        self.PATH_SHEET = pygame.image.load('Resources/Sprites/Map_Sprites/dirt_path_spritesheet.png')
        self.PATH_SHEET = pygame.transform.scale(self.PATH_SHEET, (self.TILESIZE * 4, self.TILESIZE))
        self.PATH_SHEET = self.PATH_SHEET.convert_alpha()
        
        self.DIRT_PATH_IMAGE = self.__autoLoader('Resources/Tiles/dirt_path.png')
        
        self.BRIDGE_VERT_IMAGE = self.__autoLoader('Resources/Sprites/Map_Sprites/bridge_vert.png')
        
        self.BRIDGE_HORIZ_IMAGE = self.__autoLoader('Resources/Sprites/Map_Sprites/bridge_horiz.png')
        
        self.BRIDGE_CENT_IMAGE = self.__autoLoader('Resources/Sprites/Map_Sprites/bridge_cent.png')
        
        self.SHRUB_IMAGE = self.__autoLoader('Resources/Sprites/Map_Sprites/shrub.png')
        
        self.WALL_IMAGE = self.__autoLoader('Resources/Sprites/Map_Sprites/wood wall.png')
        
        
    def __autoLoader(self, imageString):
        temp = pygame.image.load(imageString)
        temp = pygame.transform.scale(temp, (self.TILESIZE, self.TILESIZE))
        temp = temp.convert_alpha()
        
        return temp
        
    def __createMapSurfaces(self):
        tempX = self.mapPixX
        tempY = self.mapPixY
        
        
        xCordList = []
        while tempX > self.maxTiles:
            xCordList.append(self.maxTiles)
            tempX -= self.maxTiles
        xCordList.append(tempX)
        
        yCordList = []
        while tempY > self.maxTiles:
            yCordList.append(self.maxTiles)
            tempY -= self.maxTiles
        yCordList.append(tempY)
        
        SurfaceList = []
        tempList = []
        for xCord in xCordList:
            for yCord in yCordList:
                tempList.append(pygame.surface.Surface((xCord * self.TILESIZE, yCord * self.TILESIZE), depth = 32, flags = SRCALPHA))
            SurfaceList.append(tempList)
            tempList = []
        
        self.SURF_LIST = SurfaceList
        
        self.SURF_RECT_LIST = []
        tempList = []
        for x in range(len(self.SURF_LIST)):
            for y in range(len(self.SURF_LIST[0])):
                tempList.append(Rect(x * self.maxTiles * self.TILESIZE, y * self.maxTiles * self.TILESIZE,
                                     self.SURF_LIST[x][y].get_size()[0],
                                     self.SURF_LIST[x][y].get_size()[1]))
            self.SURF_RECT_LIST.append(tempList)
            tempList = []
            

    def __createMapTileList(self, mapY, mapX, tileSize, mapFile): # Reads the map file we inputed

        source = pygame.image.load(mapFile)
        temp = mapFile.find('.')
        tempString = mapFile[0:temp] + 'Collision' + mapFile[temp:]
        source2 = pygame.image.load(tempString)
        tempString = mapFile[0:temp] + 'Spawn' + mapFile[temp:]
        source3 = pygame.image.load(tempString)

        tileList = []
        tempList = []

        for x in range(mapX): # Creates every tile object and chucks them in the tile list
            for y in range(mapY):
                color = source.get_at((x,y))
                tempList.append(self.__tilePicker(color, tileSize, (x*tileSize, y*tileSize)))
            tileList.append(tempList)
            tempList = []
            
        for x in range(mapX): # Checks the collision image and assings collison where needed
            for y in range(mapY):
                color = source2.get_at((x,y))
                if color == (0,0,0,255):
                    tileList[x][y].setCollide(True)

        for x in range(mapX): # Checks the spawn image for the map and assigns spawn where needed
            for y in range(mapY):
                color = source3.get_at((x,y))
                # Dynamic spawns require their own class and are instantiated later in the interface class
                # Static spawns are simply art which is blitted onto the map surf 
                if color == (255,0,255,255):
                    tileList[x][y].setSpawn('player') # Dynamic 
                elif color == (0,200,0,200):
                    tileList[x][y].setSpawn('HeadHunter') # Dynamic
                elif color == (0,0,200,200):
                    tileList[x][y].setSpawn('WitchDoctor') # Dynamic
                elif color == (200,0,0,200):
                    tileList[x][y].setSpawn('Brute') # Dynamic
                elif color == (180,130,90,255):
                    tileList[x][y].setSpawn('LargeTree') # Dynamic
                elif color == (180,130,90,205):
                    tileList[x][y].setSpawn('MediumTree') # Dynamic
                elif color == (250,200,50,255):
                    tileList[x][y].setSpawn('HutDown') # Dynamic
                elif color == (250,200,50,205):
                    tileList[x][y].setSpawn('HutLeft') # Dynamic
                elif color == (250,200,50,155):
                    tileList[x][y].setSpawn('HutUp') # Dynamic
                elif color == (250,200,50,105):
                    tileList[x][y].setSpawn('HutRight') # Dynamic    
                elif color == (255,150,80,255):
                    tileList[x][y].setSpawn('firePit') # Dynamic
                elif color == (255,0,0,100):
                    tileList[x][y].setSpawn('consumableHealth') # Dynamic
                elif color == (70,70,70,100):
                    tileList[x][y].setSpawn('consumableAmmo') # Dynamic
                elif color == (255,255,255,255):
                    tileList[x][y].setSpawn('boatDown') # Dynamic
                elif color == (255,255,255,205):
                    tileList[x][y].setSpawn('boatLeft') # Dynamic
                elif color == (255,255,255,155):
                    tileList[x][y].setSpawn('boatUp') # Dynamic
                elif color == (255,255,255,105):
                    tileList[x][y].setSpawn('boatRight') # Dynamic
                elif color == (40,40,40,255):
                    tileList[x][y].setSpawn('LargeRock') # Dynamic
                elif color == (40,40,40,205):
                    tileList[x][y].setSpawn('MediumRock') # Dynamic
                elif color == (40,40,40,155):
                    tileList[x][y].setSpawn('smallRock') # Static
                elif color == (120,50,0,255):
                    tileList[x][y].setSpawn('bridge_vert') # Static
                elif color == (120,50,0,205):
                    tileList[x][y].setSpawn('bridge_horiz') # Static
                elif color == (110,50,0,255):
                    tileList[x][y].setSpawn('bridge_cent') # Static
                elif color == (0,115,0,255):
                    tileList[x][y].setSpawn('shrub') # Static
                elif color == (40,10,10,255):
                    tileList[x][y].setSpawn('wall') # Static
                elif color == (125,125,125,255):
                    tileList[x][y].setSpawn('ChestUp') # Dynamic
                elif color == (125,125,125,205):
                    tileList[x][y].setSpawn('ChestLeft') # Dynamic
                elif color == (125,125,125,155):
                    tileList[x][y].setSpawn('ChestDown') # Dynamic
                elif color == (125,125,125,105):
                    tileList[x][y].setSpawn('ChestRight') # Dynamic
                elif color[0] == color[1] == color[2] and color[3] != 0 and color[0] <= 30: # STATIIIIIICCCCCCC (dirth path)
                    GeorgeBush = color[0]//10
                    r = (255 - color[3])//50
                    tempString = 'path' + str(GeorgeBush) + str(r)
                    tileList[x][y].setSpawn(tempString)
                    
        return tileList

    def __tilePicker(self, color, tileSize, pos): # A small helper function for the above createMapTileList function
        for temp in range(3):
            if color[temp] != 0:
                y = tileSize * temp
                x = ((255 - color[temp])//10 ) * self.TILESIZE
                r = ((255 - color[3]) // 10) * 18
            
        try: x + 1
        except:
            y = tileSize * 2
            x = tileSize * 9
            r = 0
            
        sheetRect = Rect(x, y, self.TILESIZE, self.TILESIZE)

        return Tile(pos, tileSize, self.TILESHEET, sheetRect, r)

    def updateMapImage(self): # Goes through every tile in the tile list and has it blit its image to the revelant map surfaces
        for x in range(len(self.TILELIST)):
            for y in range(len(self.TILELIST[0])):
                for x2 in range(len(self.SURF_LIST)):
                    for y2 in range(len(self.SURF_LIST[0])):
                        if self.SURF_RECT_LIST[x2][y2].colliderect(self.TILELIST[x][y].RECT):
                            pos = (self.TILELIST[x][y].POS[0] - self.SURF_RECT_LIST[x2][y2][0],
                                   self.TILELIST[x][y].POS[1] - self.SURF_RECT_LIST[x2][y2][1])
                            self.SURF_LIST[x2][y2].blit(self.TILELIST[x][y].returnImage(), pos)
                            if self.TILELIST[x][y].spawn != '':
                                if self.TILELIST[x][y].spawn == 'bridge_vert':
                                    self.SURF_LIST[x2][y2].blit(self.BRIDGE_VERT_IMAGE, pos)
                                elif self.TILELIST[x][y].spawn == 'bridge_horiz':
                                    self.SURF_LIST[x2][y2].blit(self.BRIDGE_HORIZ_IMAGE, pos)
                                elif self.TILELIST[x][y].spawn == 'bridge_cent':
                                    self.SURF_LIST[x2][y2].blit(self.BRIDGE_CENT_IMAGE, pos)
                                elif self.TILELIST[x][y].spawn == 'shrub':
                                    self.SURF_LIST[x2][y2].blit(self.SHRUB_IMAGE, pos)
                                elif self.TILELIST[x][y].spawn == 'wall':
                                    self.SURF_LIST[x2][y2].blit(self.WALL_IMAGE, pos)
                                elif self.TILELIST[x][y].spawn == 'smallRock':
                                    r = random.randint(0,5)
                                    self.SURF_LIST[x2][y2].blit(self.SMALL_ROCK_SHEET, pos, area = Rect(r * self.TILESIZE, 0, self.TILESIZE, self.TILESIZE))
                                elif self.TILELIST[x][y].spawn[0:4] == 'path':
                                    GeorgeBush = int(self.TILELIST[x][y].spawn[4]) * self.TILESIZE
                                    r = int(self.TILELIST[x][y].spawn[5]) * 90
                                    tempSurf = pygame.surface.Surface((self.TILESIZE, self.TILESIZE), flags = SRCALPHA, depth = 32)
                                    tempSurf.blit(self.PATH_SHEET, (0,0), area = Rect(GeorgeBush, 0, self.TILESIZE, self.TILESIZE))
                                    tempSurf = pygame.transform.rotate(tempSurf, r)
                                    self.SURF_LIST[x2][y2].blit(tempSurf, pos)
                                    del tempSurf


    def getPlayerSpawnPos(self):
        for x in range(self.mapPixX):
            for y in range(self.mapPixY):
                if self.TILELIST[x][y].spawn == 'player':
                    return self.TILELIST[x][y].POS
    
    def getSpawnPositions(self, entityName):
        tempL = []
        for x in range(self.mapPixX):
            for y in range(self.mapPixY):
                if self.TILELIST[x][y].spawn == entityName:
                    tempL.append(self.TILELIST[x][y].POS)
        return tempL 
    
    def getChest(self):
        for x in range(self.mapPixX):
            for y in range(self.mapPixY):
                if self.TILELIST[x][y].spawn[0:5] == 'Chest':
                    return (self.TILELIST[x][y].POS, self.TILELIST[x][y].spawn)
                
                
    def getCollisionRects(self):
        tempList = []
        for x in range(self.mapPixX):
            for y in range(self.mapPixY):
                if self.TILELIST[x][y].collide:
                    tempList.append(self.TILELIST[x][y].RECT)
                    

        change = True
        while change: # This section combines rects, making the list shorter
            change = False
            for rect in tempList:
                for rect2 in tempList:
                    if (rect.x == rect2.x and
                        rect.y + rect.h == rect2.y and
                        rect.w == rect2.w and
                        rect.y != rect2.y or
                        rect.y == rect2.y and
                        rect.x + rect.w == rect2.x and
                        rect.h == rect2.h and
                        rect.x != rect2.x):
                        
                        newRect = rect.union(rect2)
                        tempList.append(newRect)
                        del tempList[tempList.index(rect)]
                        del tempList[tempList.index(rect2)]
                        change = True
                        break
                 
        return tempList

    def blitToDisplaySurf(self, surf, rect): # Takes in the display surf and blits relevant map sections
        for x in range(len(self.SURF_LIST)):
            for y in range(len(self.SURF_LIST[0])):
                if self.SURF_RECT_LIST[x][y].colliderect(rect):
                    
                    tempX = self.SURF_RECT_LIST[x][y][0] - rect[0]
                    if tempX < 0: tempX = 0
                        
                    tempY = self.SURF_RECT_LIST[x][y][1] - rect[1]
                    if tempY <0: tempY = 0
                    
                    if rect[0] < self.SURF_RECT_LIST[x][y][0]: tempX2 = 0
                    else: tempX2 = rect[0] - self.SURF_RECT_LIST[x][y][0]
                    
                    if rect[1] < self.SURF_RECT_LIST[x][y][1]: tempY2 = 0
                    else: tempY2 = rect[1] - self.SURF_RECT_LIST[x][y][1]
                    
                    tempX3 = rect[2] + (rect[0] - self.SURF_RECT_LIST[x][y][0])
                    if tempX3 > rect[2]: tempX3 = rect[2]
                    
                    tempY3 = rect[3] + (rect[1] - self.SURF_RECT_LIST[x][y][1])
                    if tempY3 > rect[3]: tempY3 = rect[3]
                        
                    surf.blit(self.SURF_LIST[x][y], (tempX, tempY),
                              area = Rect(tempX2, tempY2, tempX3, tempY3))
                    
                    
class mapNew(object):
    
    
    
        def __init__(self, mapFile, mapPixX, mapPixY, tileSize):
    
            #globals
            self.TILESIZE = tileSize
            self.MAPFILE = mapFile
            self.mapPixY = mapPixY
            self.mapPixX = mapPixX
    
            self.__preLoadTileImages()
            
            self.MapSurf = None # Later used to contain a small surface object of needed map pixel data

            # Create the list of tile objects we will use for collision areas on the map
            self.TILELIST = self.__createMapTileList(mapPixY, mapPixX, tileSize, mapFile)
    
        def __preLoadTileImages(self): # Pre Loads and renders tile images for faster load times
            # The tile objects will take in these images and "point" to them instead of creating their own images for each tile
    
            self.TILESHEET = pygame.image.load('Resources/Tiles/tile_sheet.png')
            self.TILESHEET = pygame.transform.scale(self.TILESHEET, (self.TILESIZE * 10, self.TILESIZE * 3))
            self.TILESHEET = self.TILESHEET.convert_alpha()
            
            self.SMALL_ROCK_SHEET = pygame.image.load('Resources/Sprites/Map_Sprites/tiny_rock_spritesheet.png')
            self.SMALL_ROCK_SHEET = pygame.transform.scale(self.SMALL_ROCK_SHEET, (self.TILESIZE * 6, self.TILESIZE))
            self.SMALL_ROCK_SHEET = self.SMALL_ROCK_SHEET.convert_alpha()
            
            self.PATH_SHEET = pygame.image.load('Resources/Sprites/Map_Sprites/dirt_path_spritesheet.png')
            self.PATH_SHEET = pygame.transform.scale(self.PATH_SHEET, (self.TILESIZE * 4, self.TILESIZE))
            self.PATH_SHEET = self.PATH_SHEET.convert_alpha()
            
            self.DIRT_PATH_IMAGE = self.__autoLoader('Resources/Tiles/dirt_path.png')
            
            self.BRIDGE_VERT_IMAGE = self.__autoLoader('Resources/Sprites/Map_Sprites/bridge_vert.png')
            
            self.BRIDGE_HORIZ_IMAGE = self.__autoLoader('Resources/Sprites/Map_Sprites/bridge_horiz.png')
            
            self.BRIDGE_CENT_IMAGE = self.__autoLoader('Resources/Sprites/Map_Sprites/bridge_cent.png')
            
            self.SHRUB_IMAGE = self.__autoLoader('Resources/Sprites/Map_Sprites/shrub.png')
            
            self.WALL_IMAGE = self.__autoLoader('Resources/Sprites/Map_Sprites/wood wall.png')
            
            
        def __autoLoader(self, imageString):
            temp = pygame.image.load(imageString)
            temp = pygame.transform.scale(temp, (self.TILESIZE, self.TILESIZE))
            temp = temp.convert_alpha()
            
            return temp
                
    
        def __createMapTileList(self, mapY, mapX, tileSize, mapFile): # Reads the map file we inputed
    
            source = pygame.image.load(mapFile)
            temp = mapFile.find('.')
            tempString = mapFile[0:temp] + 'Collision' + mapFile[temp:]
            source2 = pygame.image.load(tempString)
            tempString = mapFile[0:temp] + 'Spawn' + mapFile[temp:]
            source3 = pygame.image.load(tempString)
    
            tileList = []
            tempList = []
    
            for x in range(mapX): # Creates every tile object and chucks them in the tile list
                for y in range(mapY):
                    color = source.get_at((x,y))
                    tempList.append(self.__tilePicker(color, tileSize, (x*tileSize, y*tileSize)))
                tileList.append(tempList)
                tempList = []
                
            for x in range(mapX): # Checks the collision image and assings collison where needed
                for y in range(mapY):
                    color = source2.get_at((x,y))
                    if color == (0,0,0,255):
                        tileList[x][y].setCollide(True)
    
            for x in range(mapX): # Checks the spawn image for the map and assigns spawn where needed
                for y in range(mapY):
                    color = source3.get_at((x,y))
                    # Dynamic spawns require their own class and are instantiated later in the interface class
                    # Static spawns are simply art which is blitted onto the map surf 
                    if color == (255,0,255,255):
                        tileList[x][y].setSpawn('player') # Dynamic 
                    elif color == (0,200,0,200):
                        tileList[x][y].setSpawn('HeadHunter') # Dynamic
                    elif color == (0,0,200,200):
                        tileList[x][y].setSpawn('WitchDoctor') # Dynamic
                    elif color == (200,0,0,200):
                        tileList[x][y].setSpawn('Brute') # Dynamic
                    elif color == (180,130,90,255):
                        tileList[x][y].setSpawn('LargeTree') # Dynamic
                    elif color == (180,130,90,205):
                        tileList[x][y].setSpawn('MediumTree') # Dynamic
                    elif color == (250,200,50,255):
                        tileList[x][y].setSpawn('HutDown') # Dynamic
                    elif color == (250,200,50,205):
                        tileList[x][y].setSpawn('HutLeft') # Dynamic
                    elif color == (250,200,50,155):
                        tileList[x][y].setSpawn('HutUp') # Dynamic
                    elif color == (250,200,50,105):
                        tileList[x][y].setSpawn('HutRight') # Dynamic    
                    elif color == (255,150,80,255):
                        tileList[x][y].setSpawn('firePit') # Dynamic
                    elif color == (255,0,0,100):
                        tileList[x][y].setSpawn('consumableHealth') # Dynamic
                    elif color == (70,70,70,100):
                        tileList[x][y].setSpawn('consumableAmmo') # Dynamic
                    elif color == (255,255,255,255):
                        tileList[x][y].setSpawn('boatDown') # Dynamic
                    elif color == (255,255,255,205):
                        tileList[x][y].setSpawn('boatLeft') # Dynamic
                    elif color == (255,255,255,155):
                        tileList[x][y].setSpawn('boatUp') # Dynamic
                    elif color == (255,255,255,105):
                        tileList[x][y].setSpawn('boatRight') # Dynamic
                    elif color == (40,40,40,255):
                        tileList[x][y].setSpawn('LargeRock') # Dynamic
                    elif color == (40,40,40,205):
                        tileList[x][y].setSpawn('MediumRock') # Dynamic
                    elif color == (40,40,40,155):
                        tileList[x][y].setSpawn('smallRock') # Static
                    elif color == (120,50,0,255):
                        tileList[x][y].setSpawn('bridge_vert') # Static
                    elif color == (120,50,0,205):
                        tileList[x][y].setSpawn('bridge_horiz') # Static
                    elif color == (110,50,0,255):
                        tileList[x][y].setSpawn('bridge_cent') # Static
                    elif color == (0,115,0,255):
                        tileList[x][y].setSpawn('shrub') # Static
                    elif color == (40,10,10,255):
                        tileList[x][y].setSpawn('wall') # Static
                    elif color == (125,125,125,255):
                        tileList[x][y].setSpawn('ChestUp') # Dynamic
                    elif color == (125,125,125,205):
                        tileList[x][y].setSpawn('ChestLeft') # Dynamic
                    elif color == (125,125,125,155):
                        tileList[x][y].setSpawn('ChestDown') # Dynamic
                    elif color == (125,125,125,105):
                        tileList[x][y].setSpawn('ChestRight') # Dynamic
                    elif color[0] == color[1] == color[2] and color[3] != 0 and color[0] <= 30: # STATIIIIIICCCCCCC (dirth path)
                        GeorgeBush = color[0]//10
                        r = (255 - color[3])//50
                        tempString = 'path' + str(GeorgeBush) + str(r)
                        tileList[x][y].setSpawn(tempString)
                        
            return tileList
    
        def __tilePicker(self, color, tileSize, pos): # A small helper function for the above createMapTileList function
            for temp in range(3):
                if color[temp] != 0:
                    y = tileSize * temp
                    x = ((255 - color[temp])//10 ) * self.TILESIZE
                    r = ((255 - color[3]) // 10) * 18
                
            try: x + 1
            except:
                y = tileSize * 2
                x = tileSize * 9
                r = 0
                
            sheetRect = Rect(x, y, self.TILESIZE, self.TILESIZE)
    
            return Tile(pos, tileSize, self.TILESHEET, sheetRect, r)
    
        def makeMapSurf(self, screenRect): # ADD LATER
            tempL = []
            for x in range(self.mapPixX): # Extract RECT data from collided tiles
                for y in range(self.mapPixY):
                    if screenRect.colliderect(self.TILELIST[x][y].RECT):
                        tempL.append(self.TILELIST[x][y].RECT)
            
            self.MapSurfRect = tempL[0]
            for x in range(len(tempL) - 1): # Merges all RECT data into one Rect
                self.MapSurfRect.union_ip(tempL[x+1])
                
            self.MapSurfRect.w += self.TILESIZE 
            self.MapSurfRect.h += self.TILESIZE
                
            self.MapSurf = pygame.surface.Surface((self.MapSurfRect[2], self.MapSurfRect[3]), depth = 32, flags = SRCALPHA)
            
            
            for x in range(self.mapPixX):
                for y in range(self.mapPixY):
                    if self.MapSurfRect.colliderect(self.TILELIST[x][y].RECT): # Blit all tiles onto the Map Surf that collide with it
                        pos = (self.TILELIST[x][y].POS[0] - self.MapSurfRect[0],
                               self.TILELIST[x][y].POS[1] - self.MapSurfRect[1])
                        self.__blitTile(self.TILELIST[x][y], pos, self.MapSurf)
                        
        def __blitTile(self, tile, pos, surf): # helper function for map tile blitting
                        surf.blit(tile.returnImage(), pos)
                        if tile.spawn != '':
                            if tile.spawn == 'bridge_vert':
                                surf.blit(self.BRIDGE_VERT_IMAGE, pos)
                            elif tile.spawn == 'bridge_horiz':
                                surf.blit(self.BRIDGE_HORIZ_IMAGE, pos)
                            elif tile.spawn == 'bridge_cent':
                                surf.blit(self.BRIDGE_CENT_IMAGE, pos)
                            elif tile.spawn == 'shrub':
                                surf.blit(self.SHRUB_IMAGE, pos)
                            elif tile.spawn == 'wall':
                                surf.blit(self.WALL_IMAGE, pos)
                            elif tile.spawn == 'smallRock':
                                r = random.randint(0,5)
                                surf.blit(self.SMALL_ROCK_SHEET, pos, area = Rect(r * self.TILESIZE, 0, self.TILESIZE, self.TILESIZE))
                            elif tile.spawn[0:4] == 'path':
                                GeorgeBush = int(tile.spawn[4]) * self.TILESIZE
                                r = int(tile.spawn[5]) * 90
                                tempSurf = pygame.surface.Surface((self.TILESIZE, self.TILESIZE), flags = SRCALPHA, depth = 32)
                                tempSurf.blit(self.PATH_SHEET, (0,0), area = Rect(GeorgeBush, 0, self.TILESIZE, self.TILESIZE))
                                tempSurf = pygame.transform.rotate(tempSurf, r)
                                surf.blit(tempSurf, pos)
                                del tempSurf
    
    
        def getPlayerSpawnPos(self):
            for x in range(self.mapPixX):
                for y in range(self.mapPixY):
                    if self.TILELIST[x][y].spawn == 'player':
                        return self.TILELIST[x][y].POS
        
        def getSpawnPositions(self, entityName):
            tempL = []
            for x in range(self.mapPixX):
                for y in range(self.mapPixY):
                    if self.TILELIST[x][y].spawn == entityName:
                        tempL.append(self.TILELIST[x][y].POS)
            return tempL 
        
        def getChest(self):
            for x in range(self.mapPixX):
                for y in range(self.mapPixY):
                    if self.TILELIST[x][y].spawn[0:5] == 'Chest':
                        return (self.TILELIST[x][y].POS, self.TILELIST[x][y].spawn)
                    
                    
        def getCollisionRects(self):
            tempList = []
            for x in range(self.mapPixX):
                for y in range(self.mapPixY):
                    if self.TILELIST[x][y].collide:
                        tempList.append(self.TILELIST[x][y].RECT)
                        
    
            change = True
            while change: # This section combines rects, making the list shorter
                change = False
                for rect in tempList:
                    for rect2 in tempList:
                        if (rect.x == rect2.x and
                            rect.y + rect.h == rect2.y and
                            rect.w == rect2.w and
                            rect.y != rect2.y or
                            rect.y == rect2.y and
                            rect.x + rect.w == rect2.x and
                            rect.h == rect2.h and
                            rect.x != rect2.x):
                            
                            newRect = rect.union(rect2)
                            tempList.append(newRect)
                            del tempList[tempList.index(rect)]
                            del tempList[tempList.index(rect2)]
                            change = True
                            break
                     
            return tempList
        
        def __shiftMap(self, direction):
            if direction == 'right':
                self.MapSurf.scroll(dx = -self.TILESIZE) # Moves over the tiles on the MapSurf
                self.MapSurfRect.x += self.TILESIZE # Shifts the MapSurf Rect over 
                startTile = ((self.MapSurfRect[0] + self.MapSurfRect[2])//self.TILESIZE - 1, self.MapSurfRect[1]//self.TILESIZE)
                numTiles = self.MapSurfRect[3]//self.TILESIZE
                for x in range(numTiles):
                    pos = (self.TILELIST[startTile[0]][startTile[1] + x].POS[0] - self.MapSurfRect[0],
                           self.TILELIST[startTile[0]][startTile[1] + x].POS[1] - self.MapSurfRect[1])
                    self.__blitTile(self.TILELIST[startTile[0]][startTile[1] + x], pos, self.MapSurf)
                    
            elif direction == 'left':
                self.MapSurf.scroll(dx = self.TILESIZE) # Moves over the tiles on the MapSurf
                self.MapSurfRect.x -= self.TILESIZE # Shifts the MapSurf Rect over 
                startTile = (self.MapSurfRect[0]//self.TILESIZE, self.MapSurfRect[1]//self.TILESIZE)
                numTiles = self.MapSurfRect[3]//self.TILESIZE
                for x in range(numTiles):
                    pos = (self.TILELIST[startTile[0]][startTile[1] + x].POS[0] - self.MapSurfRect[0],
                           self.TILELIST[startTile[0]][startTile[1] + x].POS[1] - self.MapSurfRect[1])
                    self.__blitTile(self.TILELIST[startTile[0]][startTile[1] + x], pos, self.MapSurf)
                    
            elif direction == 'down':
                self.MapSurf.scroll(dy = -self.TILESIZE) # Moves over the tiles on the MapSurf
                self.MapSurfRect.y += self.TILESIZE # Shifts the MapSurf Rect over 
                startTile = (self.MapSurfRect[0]//self.TILESIZE, (self.MapSurfRect[1] + self.MapSurfRect[3])//self.TILESIZE - 1)
                numTiles = self.MapSurfRect[2]//self.TILESIZE
                for x in range(numTiles):
                    pos = (self.TILELIST[startTile[0] + x][startTile[1]].POS[0] - self.MapSurfRect[0],
                           self.TILELIST[startTile[0] + x][startTile[1]].POS[1] - self.MapSurfRect[1])
                    self.__blitTile(self.TILELIST[startTile[0] + x][startTile[1]], pos, self.MapSurf)
                    
            elif direction == 'up':
                self.MapSurf.scroll(dy = self.TILESIZE) # Moves over the tiles on the MapSurf
                self.MapSurfRect.y -= self.TILESIZE # Shifts the MapSurf Rect over 
                startTile = (self.MapSurfRect[0]//self.TILESIZE, self.MapSurfRect[1]//self.TILESIZE)
                numTiles = self.MapSurfRect[2]//self.TILESIZE
                for x in range(numTiles):
                    pos = (self.TILELIST[startTile[0] + x][startTile[1]].POS[0] - self.MapSurfRect[0],
                           self.TILELIST[startTile[0] + x][startTile[1]].POS[1] - self.MapSurfRect[1])
                    self.__blitTile(self.TILELIST[startTile[0] + x][startTile[1]], pos, self.MapSurf)
    
        def blitToDisplaySurf(self, surf, rect): # Takes in the display surf and blits relevant map sections
            if self.MapSurf == None: self.makeMapSurf(rect)
            
            if rect[0] + rect[2] > self.MapSurfRect[0] + self.MapSurfRect[2]: self.__shiftMap('right')
            elif rect[0] < self.MapSurfRect[0]: self.__shiftMap('left')
            if rect[1] + rect[3] > self.MapSurfRect[1] + self.MapSurfRect[3]: self.__shiftMap('down')
            elif rect[1] < self.MapSurfRect[1]: self.__shiftMap('up')
            
            pos = (self.MapSurfRect[0] - rect[0], self.MapSurfRect[1] - rect[1])
            surf.blit(self.MapSurf, pos)
    