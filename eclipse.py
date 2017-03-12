#usr/bin/env python

import os, pygame, math
from pygame.locals import *
import pdb

MAP_WIDTH = 38
MAP_HEIGHT = 31
HEXSIZE = 38

HEX_HEIGHT = HEXSIZE * 2
HEX_WIDTH = math.sqrt(3)/2 * HEX_HEIGHT

TILE_WIDTH = HEX_WIDTH
TILE_HEIGHT = HEX_HEIGHT

TILE_WIDTH = 38
TILE_HEIGHT = 41

HEXSIZE = TILE_HEIGHT /2

GRID_WIDTH = 38
GRID_HEIGHT = 31
RESOLUTIONX = 640
RESOLUTIONY = 480
NHEXX = 7
NHEXY = 4
NCENTER = (3,3)
NRINGS = NHEXX / 2

ROW_HEIGHT = 31
ODD_ROW_X_MOD = 19

HEX2HEXVEC = [[-1,0], [0,-1],[1,-1], [1,0], [1,1], [0,1]]

# INITIALISE WINDOW

class Hex():
    # A hex on the map, used to characterise a hex tile
    def __init__(self, x0, y0, s):
        self.x = x0
        self.y = y0
        self.height = 2*s
        self.width = math.sqrt(3)/2 * s




class eclipse:

    def __init__(self):
        self.screen = pygame.display.set_mode((640, 480), 1)
        pygame.display.set_caption('ECLIPSE')
        
        self.loadTiles()
    
        self.drawMap()
        self.gridmap = pygame.Rect(0,0, MAP_WIDTH, MAP_HEIGHT)
 
    def hexMapToPixel(self,mapX,mapY):
        """
        Returns the top left pixel location of a hexagon map location.
        """
        # Calculate offsets to place in centre

        OFFX = RESOLUTIONX/2 - TILE_WIDTH*NHEXX/2
        OFFY = RESOLUTIONY/2 - TILE_HEIGHT*NHEXY/2

        if mapY & 1:
            # Odd rows will be moved to the right.
            return (OFFX+mapX*TILE_WIDTH+ODD_ROW_X_MOD,OFFY+mapY*ROW_HEIGHT)
        else:
            return (OFFX+mapX*TILE_WIDTH,OFFY+mapY*ROW_HEIGHT)

    def HexAxialCoordsToPixel(self, q, r):
        """
        Returns the top left pixel location of a hexagon map location in axial coordinates
        """
        # Calculate offsets to place in centre

        OFFX = RESOLUTIONX/2 - TILE_WIDTH*NHEXX/2
        OFFY = RESOLUTIONY/2 - TILE_HEIGHT*NHEXY/2
        OFFX = RESOLUTIONX/2
        OFFY = RESOLUTIONY/2

        return (OFFX+TILE_WIDTH * 1 * q, OFFY+TILE_HEIGHT * r)

    def Hex(x, y):
        """ Hex is the base class tile """
        
    

    def drawMap(self):       
        """
        Draw the tiles.
        """

        fnt = pygame.font.Font(pygame.font.get_default_font(),12)
 #       pdb.set_trace()
        self.mapimg = pygame.Surface((RESOLUTIONX,RESOLUTIONY),1)
        self.mapimg= self.mapimg.convert()
        self.mapimg = pygame.image.load("./starmap.jpg").convert()
        self.mapimg = pygame.transform.scale(self.mapimg, (RESOLUTIONX, RESOLUTIONY) )
        #self.mapimg.fill((0,0,0))

        for q in range(-NHEXX/2, NHEXX/2):
            for r in range(-NHEXY/2, NHEXY/2):
                # Get the top left location of the tile.
                #pixelX,pixelY = self.hexMapToPixel(x,y)
                pixelX,pixelY = self.HexAxialCoordsToPixel(q,r)
                # Blit the tile to the map image.
                self.mapimg.blit(self.tile,(pixelX,pixelY))

                # Show the hexagon map location in the center of the tile.
                location = fnt.render("%d,%d" % (q,r), 0, (0xff,0xff,0xff))
                lrect=location.get_rect()
#                lrect.center = (pixelX+(TILE_WIDTH/2),pixelY+(TILE_HEIGHT/2))                
                lrect.center = (pixelX+TILE_WIDTH/2, pixelY+TILE_WIDTH/2)
                self.mapimg.blit(location,lrect.topleft)

        self.gridRect = pygame.Rect(0, 0, GRID_WIDTH, GRID_HEIGHT)

    def drawMapzones(self):
        # Starting from center hex, workoutwards
        for x in range(NRINGS):
            # Create the array of coordinates of this ring
            for i in range(6):
                    print "%d,%d", NCENTER[0]+HEX2HEXVEC[i][0], NCENTER[0]+HEX2HEXVEC[i][1]

    def loadTiles(self):
        """
        Load the tile
        """
        self.tile = pygame.image.load("./hextile.png").convert()
        self.tile.set_colorkey((0x80, 0x00, 0x80), RLEACCEL)                


    def mainloop(self):
        clock = pygame.time.Clock()
#        pdb.set_trace()
        showGridRect = True

        while 1:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 

            self.screen.blit(self.mapimg, (0, 0))
            if showGridRect:
                pygame.draw.rect(self.screen, (0xff, 0xff, 0xff), self.gridRect, 1)

            pygame.display.flip()


def main():
    pygame.init()
    g = eclipse()
    g.drawMapzones() 
    g.mainloop()

    
#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
