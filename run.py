from os import abort
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
appleArguments = [win, config, nApples, loaded_images.EntImages.Herbivore]
apples = generate_apples(*appleArguments)
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
                # If entity is apple draw the apple onto the screen
                if entity.entityType == EntTypes.apples: # String comparison takes a lot of processing power, ill probably switch to integers
                    entity.draw_entity(win.screen, DrawTypes.RECT)
                # If entity is herbivore
                elif entity.entityType == EntTypes.herbivores: # String comparions takes a lot of processing power
                    
                    # The minimum distance to/and the apple that is closest to the entity
                    closestApple: Apple = None
                    minDistance: float = entity.dna.senserange.get_value() # Very big value
                    
                    # Amount of tiles to check for entity collision
                    nTiles = int(math.ceil(entity.dna.senserange.get_value() / WorldMap.cell_size))

                    # Herbivore position
                    position = entity.get_center_pos() - Vector(entity.dna.senserange.get_value(), entity.dna.senserange.get_value())
                    
                    # Get the tiles to check for entity collision 
                    tiles = [] 
                    for y in range(nTiles * 2):
                        lst = []
                        for x in range(nTiles * 2):
                            p = Vector(position.x + x * WorldMap.cell_size, position.y + y * WorldMap.cell_size)
                            tup = WorldMap.key_pos(p)
                            lst.append(Vector(tup[0], tup[1]))
                        tiles.append(lst)
                    
                    tiles = [item for sublist in tiles for item in sublist]
                    
                    # Iterate over the tiles for checking collision
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

                            elif distance < entity.dna.senserange.get_value() and distance < minDistance:
                                closestApple = apple
                                minDistance = distance
                                        
                    # Draw Herbivore on screen
                    entity.draw_entity(win.screen, DrawTypes.IMAGE)
                    if win.events_struct.showdbg:
                        pygame.draw.circle(win.screen, tuple(DefinedColors.blue), tuple(entity.get_center_pos()), entity.dna.senserange.get_value(), width=2)                        

                    cell = WorldMap.key(entity) # the key of the cell the entity is inside

                    ## Move the entity
                    if closestApple == None:
                        entity.move(Vector(random.choice([-entity.dna.speed.get_value(), entity.dna.speed.get_value()]), random.choice([-entity.dna.speed.get_value(), entity.dna.speed.get_value()])), win.config)
                        #entity.move_towards(Vector(random.randint(0, WIDTH), random.randint(0, HEIGHT)), win.config)
                    else:
                        entity.move_towards(closestApple.get_center_pos(), win.config)

                    # Remove entity from unused cells
                    if cell != WorldMap.key(entity):   
                        WorldMap.remove_from_key(cell, entity)
                        WorldMap.insert(entity)   

    ## WorldMap functions for every loop 
    WorldMap.current_day.frames_passed += 1

    if WorldMap.current_day.get_passed_seconds() >= config["day_length_s"]:
        WorldMap.new_day(win, config, appleArguments)

    # Passed seconds draw on screen
    secs = str(int(WorldMap.current_day.get_passed_seconds())) + " seconds"
    secs_fnt = win.FONT.render(secs, 1, tuple(DefinedColors.blue))
    win.screen.blit(secs_fnt, (10,30))

    # Passed Days draw on screen
    days = str(WorldMap.current_day.day_nmbr) + " days"
    days_fnt = win.FONT.render(days, 1, tuple(DefinedColors.blue))
    win.screen.blit(days_fnt, (10,60))

    # Amount of entities alive

    n_entities = str(int(WorldMap.n_herbivores)) + " herbivores"
    n_entities_fnt = win.FONT.render(n_entities, 1, tuple(DefinedColors.blue))
    win.screen.blit(n_entities_fnt, (10,90))

    ## End

    # Draw fps
    win.screen.blit(win.update_fps(), (10,0))

    # Finishing touches
    win.CLOCK.tick(AVERAGE_FPS)

    # Flip the display
    pygame.display.flip()
