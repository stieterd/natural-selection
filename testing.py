from entities.dna import Dna
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
    color: Color = DefinedColors.black

    size: Vector = Vector(10, 10)
    senserange: float = 30
    speed: int = 2

    dna: Dna = Dna(size, senserange, speed)

    ent: Herbivore = Herbivore(EntTypes.herbivores, pos, dna, DefinedColors.black, loaded_images.EntImages.Herbivore)

    creatures.append(ent)
    
    pos: Vector = Vector(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    size: Vector = Vector(10, 10)
    color: Color = DefinedColors.red

    apple: Apple = Apple(EntTypes.apples, pos, size, color, loaded_images.EntImages.Herbivore)
    apples.append(apple)
   
sceneObjects = {    EntTypes.herbivores: creatures, 
                    EntTypes.apples: apples
                    }

WorldMap: World = World(300, sceneObjects)

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

                    closestApple: Apple = None
                    minDistance: float = entity.dna.senserange + 1 # Very big value

                    currentCell = WorldMap.query(entity, EntTypes.apples)

                    for apple in currentCell:
                        
                        if entity.collides(apple):
                            key = WorldMap.key(apple)
                            WorldMap.remove_from_key(key, apple)
                            
                            entity.energy += apple.glucose
                            
                        else:
                            distance = euclidean(tuple(apple.position), tuple(entity.position))
                            if distance < entity.dna.senserange and distance < minDistance:
                                closestApple = apple
                                minDistance = distance

                
                    # Entity functions
                    entity.draw_entity(win.screen, DrawTypes.IMAGE)
                    pygame.draw.circle(win.screen, tuple(DefinedColors.blue), tuple(entity.position + entity.size//2), entity.dna.senserange, width=2)

                    if closestApple == None:
                        entity.move(Vector(random.randint(-entity.dna.speed, entity.dna.speed), random.randint(-entity.dna.speed, entity.dna.speed)), win.config)
                        #entity.move_towards(Vector(random.randint(0, WIDTH), random.randint(0, HEIGHT)), win.config)
                    else:
                        entity.move_towards(closestApple.position, win.config)

                    if cell != WorldMap.key(entity):   
                        WorldMap.remove_from_key(cell, entity)
                        WorldMap.insert(entity)   
    ## End

    # Draw fps
    win.screen.blit(win.update_fps(), (10,0))

    # Finishing touches
    win.CLOCK.tick(120)

    # Flip the display
    pygame.display.flip()