import random
from dataclasses import dataclass
from entities.apple import Apple
from engine.drawable import Drawable

@dataclass
class Tile(Drawable): # Tiles are always square format, each tile will contain information about its contents, such like food
    x: int # xpos
    y: int # ypos
    
    size: int # tilesize

    apple: Apple = None # Begins with no apples on the grid



class Grid: # Grid is always square format

    def __init__(self, size, tileSize = 40): # TileSize is relative to the grid, grid can be zoomed in and out 

        self.tiles = []

        for x in range(size//tileSize):
            tilePosX = x * tileSize
            tempArray = []

            for y in range(size//tileSize):
                tilePosY = y * tileSize
                tempArray.append(Tile(tilePosX, tilePosY, tileSize))

            self.tiles.append(tempArray)
