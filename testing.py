from entities.apple import Apple
import pygame

from engine.window import Window
from engine.mathfunctions import *
from engine.drawable import DrawTypes
from entities.herbivores import Herbivore


import random

# CONSTANTS
WIDTH = 1366
HEIGHT = 768

# Init Pygame and window
pygame.init()

win = Window(WIDTH, HEIGHT)

# Import ONLY after initializing window!!!!!!
from images import loaded_images

win.toggle_fullscreen()

creatures = []
apples = []

for x in range(500):
    pos: Vector = Vector(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    size: Vector = Vector(10, 10)
    color: Color = DefinedColors.black

    ent: Herbivore = Herbivore(pos, size, DefinedColors.black, loaded_images.EntImages.Herbivore)

    creatures.append(ent)
    
    pos: Vector = Vector(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    size: Vector = Vector(10, 10)
    color: Color = DefinedColors.red

    apple: Apple = Apple(pos, size, color, loaded_images.EntImages.Herbivore)
    apples.append(apple)



sceneObjects = {    "creatures": creatures, 
                    "apples": apples
                    }

# Main Game Loop
while win.events_struct.event_running:
    
    # Getting all the events
    win.check_events()

    # Fill background
    win.screen.fill(tuple(DefinedColors.white))

    # Check if paused 
    win.paused()   

    ## Here the scene objects get drawn ##
    
    
    for apple in sceneObjects["apples"]:
        apple.draw_entity(win.screen, DrawTypes.RECT)


    creature: Herbivore
    for creature in sceneObjects["creatures"]:
        creature.draw_entity(win.screen, DrawTypes.IMAGE)
        movement: int = 5
        creature.move(Vector(random.randint(-movement, movement), random.randint(-movement, movement)), win.config)

    ## End

    # Draw fps
    win.screen.blit(win.update_fps(), (10,0))

    # Finishing touches
    win.CLOCK.tick(120)

    # Flip the display
    pygame.display.flip()

# Quit (calling destructors)
pygame.quit()
