from engine.window import Window
from entities.entity import Entity
from entities.types import EntTypes
from engine.mathfunctions import *

import pygame
import random

def generate_apples(win: Window, config: dict, nEntities: int, image: pygame.image) -> list:
    
    apples = []

    for _ in range(nEntities):   
        size: Vector = Vector(config["apple_size"], config["apple_size"])
        pos: Vector = Vector(random.randint(0, win.config.screen_width - size.x - 10), random.randint(0, win.config.screen_height - size.y - 10))
        color: Color = DefinedColors.red

        apple: Apple = Apple(EntTypes.apples, pos, size, color, image)
        apples.append(apple)

    return apples

class Apple(Entity):
    """
    Apples are the main foodsource for herbivores. 
    Apples cant do anything but eaten by herbivores/omnivores on collision.
    When apples are eaten they give the amount of glucose stored in them away to the entity that eats them and the apple gets destroyed.
    """
    def __init__(self, entityType: int, position: Vector, size: Vector, color: Color, image: pygame.image) -> None:
        super().__init__(entityType, position, size, color, image)
        self.glucose: int = 1000 # The energy the apple gives when eating it 
    