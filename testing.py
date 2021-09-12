from entities.entity import Entity
from entities.types import EntTypes
from entities.apple import Apple
from entities.herbivores import Herbivore

from world.area import World

from engine.window import Window
from engine.mathfunctions import *
from engine.drawable import DrawTypes


import pygame
import random

# CONSTANTS
WIDTH = 1366
HEIGHT = 768

# Init Pygame and window
pygame.init()

win = Window(WIDTH, HEIGHT)

# Import ONLY after initializing window!!!!!!
from images import loaded_images

#win.toggle_fullscreen()

creatures = []
apples = []

for x in range(500):
    pos: Vector = Vector(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    size: Vector = Vector(10, 10)
    color: Color = DefinedColors.black
    senserange: float = 50

    ent: Herbivore = Herbivore(EntTypes.herbivores, pos, size, senserange, DefinedColors.black, loaded_images.EntImages.Herbivore)

    creatures.append(ent)
    
    pos: Vector = Vector(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    size: Vector = Vector(10, 10)
    color: Color = DefinedColors.red

    apple: Apple = Apple(EntTypes.apples, pos, size, color, loaded_images.EntImages.Herbivore)
    apples.append(apple)
   
sceneObjects = {    EntTypes.herbivores: creatures, 
                    EntTypes.apples: apples
                    }

WorldMap: World = World(60, sceneObjects)

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

                    cell = WorldMap.key(entity)
                    
                    # Entity functions
                    entity.draw_entity(win.screen, DrawTypes.IMAGE)
                    movement: int = 2
                    entity.move(Vector(random.randint(-movement, movement), random.randint(-movement, movement)), win.config)
                    
                    if cell != WorldMap.key(entity):   
                        WorldMap.remove_from_key(cell, entity)
                        WorldMap.insert(entity)
                        
                    for apple in WorldMap.query(entity, EntTypes.apples):
                        
                        if entity.collides(apple):
                                key = WorldMap.key(apple)
                                WorldMap.remove_from_key(key, apple)
                                
                                entity.energy += apple.glucose
                                break
                
    

    ## End

    # Draw fps
    win.screen.blit(win.update_fps(), (10,0))

    # Finishing touches
    win.CLOCK.tick(120)

    # Flip the display
    pygame.display.flip()