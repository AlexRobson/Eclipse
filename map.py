#usr/bin/env python

from __future__ import division
import os, pygame, math
from pygame.locals import *
import pdb
import numpy as np
import itertools
from collections import OrderedDict


RESOLUTIONX = 1640
RESOLUTIONY = 960
MAPX = 3
MAPY = 3
THETA = math.pi/ 3.0
HEXSIZE = 50
HEXWIDTH = 20
HEXHEIGHT = 20
NEIGHBORS = OrderedDict([('se',[0,+1]), ('s',[1,0]),('sw',[1,-1]),('nw',[0,-1]),('n',[-1,0]),('ne',[-1,+1])]) 
scolor = pygame.color.Color('#000019')
r1color = pygame.color.Color(0,0,0)
r2color = pygame.color.Color(0,0,0)
ccolor = 0,0,0
hcolor = 1,1,1

# Main function

#def drawarrow(x0, y0, rot, Surface):
#    x1 = x0
#    pygame.draw.polygon(Surface, acolor, ((-5,0), (


class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


class Map(object):


    def __init__(self, x0, y0):
        self.map = []
        self.x0 = x0
        self.y0 = y0
    def pixel2HexMap(self,x, y):
        # Invert the coordinates, and then convert to intergers (with a cast)
        r = int(round((2/3) * (x-self.x0) / HEXSIZE))
        q = int(round((1/3 * math.sqrt(3) * (y-self.y0) -(1/3)*(x-self.x0)) / HEXSIZE))
        return q,r

    def Hex2Pixel(self, q, r):
        yp = HEXSIZE * math.sqrt(3) * (math.sqrt(1)*q+r/2)+ self.y0
        xp = HEXSIZE * (3/2) * r + self.x0
        return xp,yp

    def selectHex(self, V):
        # Take in a coordinate, return the index in self.map that corresponds to this Hex
        for i,HEX in enumerate(self.map):
            if (HEX.coords[0]==V[0] and HEX.coords[1]==V[1]):       
                    return i
        # Return false otherwise
        return False

    def TraverseRing(self, R, V0):
        H = []
#        pdb.set_trace()
        # This function returns the Hexes in the ring of radius  about the coordinates, q, r
        # First go R north of that Hx
        VR_all = []
        VR = np.array(V0) + R*np.array(NEIGHBORS['n'])
        # Calcualte subsequent hexes
        for word in NEIGHBORS.iterkeys():
            for _ in itertools.repeat(None, R):                         
                H.append( self.neighbor(VR,word))
                VR_all.append(VR)
                VR = VR+np.array(NEIGHBORS[word])
        return H,VR_all

    def neighbor(self, V0, direction):
        for case in switch(direction):
            if case('n'):
                V = [-1,0]
                break
            if case('ne'):
                V = [-1,+1]
                break
            if case('se'):
                V = [0,+1]
                break
            if case('s'):
                V = [1,0]
                break
            if case('sw'):
                V = [1,-1]
                break
            if case('nw'):
                V = [0, -1]
                break

        Vn = np.array(V0)+np.array(V) 
        return self.selectHex(Vn)







class Hex(object):
    # A hex on the map, used to characterise a hex tile
    def __init__(self, x0, y0, s, ID, coords, exit):
        self.x = x0
        self.y = y0
        self.s = s
        self.ID = ID
        self.coords = coords
        self.height = 2*s
        self.width = math.sqrt(3)/2 * s
        self.bg()
        self.exit = exit
        self.randhex()

    def randhex():
        exits = np.arange(6)
        np.random.shuffle(exits)
        self.exits = exits[0:4]

    def bg(self):
        self.surface = pygame.Surface((RESOLUTIONX, RESOLUTIONY))
        self.surface.set_colorkey([0, 0, 0])
        self.surface.set_alpha(100)

    def returnpoints(self):
        for i in range(6):
#            pdb.set_trace()
#            self.coords[i,:] = list([math.cos(THETA * i) *self.s + self.x, math.sin(THETA * i) * self.s + self.y])
            yield math.cos(THETA * i) *self.s + self.x, math.sin(THETA * i) * self.s + self.y




class eclipse(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((RESOLUTIONX, RESOLUTIONY), 1)
        pygame.display.set_caption('Eclipse')
        "Set eclipse variables"
        self.mapimg = []
        self.Map = Map(RESOLUTIONX/2, RESOLUTIONY/2)
        self.initmap()
        self.loadbg()
        self.cursorPos = 25,25

    def setCursor(self, x, y):
        #mapX,mapY = self.Map.pixel2HexMap(x,y)
        self.cursorPos = [x,y]


    def initmap(self):
        #maparray = np.vectorize(Hex)
        #init_array = np.arange(MAPX * MAPY).reshape((MAPX, MAPY))
        #lattice = np.empty((MAPX, MAPY), dtype=object)
        #lattice[:,:] = maparray(init_array, init_array, HEXSIZE)
#        self.map = [lattice]
        
        x0 = RESOLUTIONX/2
        y0 = RESOLUTIONY/2
        ID = 0
        HEXORDER = range(-MAPX, MAPX+1)
        HEXORDER.sort(key=lambda x: abs(x))

        # ADd in the centre Hex
        coords = [0,0,0]
        xp,yp = self.Map.Hex2Pixel(coords[0],coords[1])
        self.Map.map.append(Hex(xp,yp, HEXSIZE, ID, coords))

        for R in range(4):
            V = self.Map.TraverseRing(R,[0,0])[1]
            for idx,v in enumerate((V)):

                ID += 1
                xp,yp = self.Map.Hex2Pixel(v[0],v[1])
                coords = [v[0],v[1],-(v[0]+v[1])]
                self.Map.map.append(Hex(xp,yp, HEXSIZE, ID, coords))
                        
    def loadbg(self):
        self.mapimg = pygame.Surface((RESOLUTIONX, RESOLUTIONY), 1)
        self.mapimp = self.mapimg.convert()
        self.mapimg = pygame.image.load("./galaxy.jpg").convert()
        self.mapimg = pygame.transform.scale(self.mapimg, (RESOLUTIONX, RESOLUTIONY) )
#        self.mapimg.set_alpha(90) #Comment out this line to disable motion blur
        self.bg = pygame.Surface((RESOLUTIONX, RESOLUTIONY), 1)
        self.bg.set_colorkey([0,0,0])
        self.bg.set_alpha(10)
        self.bg.fill((255,0,0))

    def mainloop(self):

        fnt = pygame.font.Font(pygame.font.get_default_font(),12)
        while 1:
            for event in pygame.event.get():
                if event.type ==QUIT:
                    return
                
                elif event.type == MOUSEMOTION:
                    self.setCursor(event.pos[0], event.pos[1])

            self.screen.blit(self.mapimg, (0, 0))


            # Print the cursor position and highlight the present hex
#                pdb.set_trace() 
            q,r = self.Map.pixel2HexMap(self.cursorPos[0], self.cursorPos[1])
            coords = [q,r]
            selectedHex = self.Map.selectHex(coords)
            text = fnt.render("%d, %d" % (q,r), 0, (0xff,0xff,0xff))
            lrect=text.get_rect()
            lrect.center = 25,25
            self.screen.blit(text, lrect.center)
            ID = []
            if isinstance(selectedHex,int):
                selectedHex = self.Map.map[selectedHex]
                ID = selectedHex.ID
                Acrds = selectedHex.coords 
                hexsurface = selectedHex.surface
                pygame.draw.polygon(hexsurface, scolor, list(selectedHex.returnpoints()))
                self.screen.blit(hexsurface,(0,0))
                text = fnt.render("%d, %d, %d" % (Acrds[0],Acrds[1], Acrds[2]), 0, (0xff,0xff,0xff))
                lrect.center = 400, 25
                self.screen.blit(text, lrect.center)
                text = fnt.render("%d, %d, %d" % (Acrds[0],Acrds[1], Acrds[2]), 0, (0,0,255))
                lrect = text.get_rect()
                lrect.center = [selectedHex.x, selectedHex.y]
                self.screen.blit(text, lrect.topleft)

            for HEX in (self.Map.map):
                hexpoints = HEX.returnpoints()
                # Color in the hex tiles
                hexsurface = HEX.surface
                pygame.draw.polygon(hexsurface,hcolor, list(hexpoints))
                self.screen.blit(hexsurface,(0,0))

                if HEX.ID!=ID:
                    text =fnt.render("%d,%d,%d" % (HEX.coords[0], HEX.coords[1], HEX.coords[2]),0, (0xff, 0xff,0xff))
                    lrect=text.get_rect()
                    lrect.center = [HEX.x, HEX.y]
                    self.screen.blit(text, lrect.topleft)

            # Color in the rings
            
            H =self.Map.TraverseRing(1,[0,0])[0]                 
#            pdb.set_trace()
            H = [self.Map.map[i] for i in H]
            for hex in H:
                pygame.draw.lines(self.screen, r1color, True, list(hex.returnpoints()),3)
 
            H =self.Map.TraverseRing(2,[0,0])[0]                 
            H = [self.Map.map[i] for i in H]
            for hex in H:
                pygame.draw.lines(self.screen, r2color, True, list(hex.returnpoints()),3)
            
            pygame.display.flip() 
            




def main():
    pygame.init()
    g = eclipse()
    g.mainloop()

if __name__ == '__main__': main()


