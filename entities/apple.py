from entities.entity import Entity
from engine.mathfunctions import *

import pygame

class Apple(Entity):

    def __init__(self, position: Vector, size: Vector, color: Color, image: pygame.image) -> None:
        super().__init__(position, size, color, image)
    