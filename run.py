import pygame

from engine.window import Window
from engine.mathfunctions import *

# CONSTANTS
WIDTH = 800
HEIGHT = 600


# Init Pygame and window
pygame.init()

win = Window(WIDTH, HEIGHT)

sceneObjects = {"creatures": [], "apples": []}


# Main Game Loop
while win.running:

    # Getting all the events
    win.check_events()

    # Fill background
    win.screen.fill(tuple(DefinedColors.green))

    ## Here the scene objects get drawn ##
    

    ## End

    # Draw Fps
    win.screen.blit(win.update_fps(), (10,0)) 

    # Finishing touches
    win.CLOCK.tick(120)

    # Flip the display
    pygame.display.flip()

# Quit (calling destructors)
pygame.quit()