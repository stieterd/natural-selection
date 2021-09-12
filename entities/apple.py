from entities.entity import Entity
from engine.mathfunctions import *

import pygame

class Apple(Entity):
    """
    Apples are the main foodsource for herbivores. 
    Apples cant do anything but eaten by herbivores/omnivores on collision.
    When apples are eaten they give the amount of glucose stored in them away to the entity that eats them and the apple gets destroyed.
    """
    def __init__(self, entityType: int, position: Vector, size: Vector, color: Color, image: pygame.image) -> None:
        super().__init__(entityType, position, size, color, image)
        self.glucose: int = 100 # The energy the apple gives when eating it 
    