from entities.dna import Dna
from entities.entity import Entity
from entities.types import EntTypes
from entities.apple import Apple, generate_apples
from entities.herbivores import Herbivore, generate_herbivores

from world.area import World
from world.days import Day

from engine.window import Window
from engine.mathfunctions import *
from engine.drawable import DrawTypes

from multiprocessing import Pool

import math
import pygame
import random
import json


# Read config file

with open("config.json", "r") as fileH:
    config = json.load(fileH) 

# CONSTANTS
WIDTH = config["window_width"]
HEIGHT = config["window_height"]
AVERAGE_FPS = config["window_fps"]

# Init Pygame and window
pygame.init()
win = Window(WIDTH, HEIGHT)

# Import ONLY after initializing window!!!!!!
from images import loaded_images

# Initialize important variables

#win.toggle_fullscreen()

creatures = []


nApples = 400
nHerbivores = 200

# Creating the entity list
apples = generate_apples(win, config, nApples, loaded_images.EntImages.Herbivore)
creatures = generate_herbivores(win, config, nHerbivores, loaded_images.EntImages.Herbivore)

# Generating WorldMap

sceneObjects = {    EntTypes.herbivores: creatures, 
                    EntTypes.apples: apples
                    }

day = Day(AVERAGE_FPS, 0)
WorldMap: World = World(60, sceneObjects, day)

# Main Game Loop
while win.events_struct.event_running:
    
    # Getting all the events
    win.check_events()

    # Fill background
    win.screen.fill(tuple(DefinedColors.white))

    # Check if paused 
    win.paused()   

    ## Here the scene objects get drawn ##
   
    for gridCell in list(WorldMap.grid): # MIGHT REMOVE LIST CAST

        for entityType in list(WorldMap.grid[gridCell]):

            entity: Entity 
            for entity in WorldMap.grid[gridCell][entityType]:

                if entity.entityType == EntTypes.apples: # String comparison takes a lot of processing power, ill probably switch to integers
                    entity.draw_entity(win.screen, DrawTypes.RECT)

                elif entity.entityType == EntTypes.herbivores: # String comparions takes a lot of processing power

                    closestApple: Apple = None
                    minDistance: float = entity.dna.senserange # Very big value
                    
                    nTiles = int(math.ceil(entity.dna.senserange / WorldMap.cell_size))

                    position = entity.get_center_pos() - Vector(entity.dna.senserange, entity.dna.senserange)
                    tiles = [] 
                    
                    for y in range(nTiles * 2):
                        lst = []
                        for x in range(nTiles * 2):
                            p = Vector(position.x + x * WorldMap.cell_size, position.y + y * WorldMap.cell_size)
                            tup = WorldMap.key_pos(p)
                            lst.append(Vector(tup[0], tup[1]))
                        tiles.append(lst)
                    
                    tiles = [item for sublist in tiles for item in sublist]
                    
                    for tile in tiles:
                        
                        if win.events_struct.showdbg:
                            pygame.draw.rect(win.screen, tuple(DefinedColors.black), (tuple(tile), tuple(Vector(WorldMap.cell_size, WorldMap.cell_size))), width=1)

                        #currentCell = WorldMap.query(entity, EntTypes.apples)
                        currentCell = WorldMap.query_from_pos(tile, EntTypes.apples)
                        for apple in currentCell:
                            distance = euclidean(tuple(apple.get_center_pos()), tuple(entity.get_center_pos()))

                            if entity.collides(apple):
                                key = WorldMap.key(apple)
                                WorldMap.remove_from_key(key, apple)
                                entity.energy += apple.glucose

                            elif distance < entity.dna.senserange and distance < minDistance:
                                closestApple = apple
                                minDistance = distance
                                        
                    # Entity functions
                    entity.draw_entity(win.screen, DrawTypes.IMAGE)
                    if win.events_struct.showdbg:
                        pygame.draw.circle(win.screen, tuple(DefinedColors.blue), tuple(entity.get_center_pos()), entity.dna.senserange, width=2)                        

                    cell = WorldMap.key(entity) # the key of the cell the entity is inside
            
                    if closestApple == None:
                        entity.move(Vector(random.randint(-entity.dna.speed, entity.dna.speed), random.randint(-entity.dna.speed, entity.dna.speed)), win.config)
                        #entity.move_towards(Vector(random.randint(0, WIDTH), random.randint(0, HEIGHT)), win.config)
                    else:
                        entity.move_towards(closestApple.get_center_pos(), win.config)

                    if cell != WorldMap.key(entity):   
                        WorldMap.remove_from_key(cell, entity)
                        WorldMap.insert(entity)   

    WorldMap.current_day.frames_passed += 1

    if WorldMap.current_day.get_passed_seconds() >= config["day_length_s"]:
        WorldMap.new_day()

    ## End

    # Draw fps
    win.screen.blit(win.update_fps(), (10,0))

    # Finishing touches
    win.CLOCK.tick(AVERAGE_FPS)

    # Flip the display
    pygame.display.flip()
