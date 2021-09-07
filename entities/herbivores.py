import pygame

from engine.mathfunctions import *
from entities.entity import Entity


class Herbivore(Entity):

    def __init__(self, position: Vector, size: Vector, color: Color, image: pygame.image) -> None:
        super().__init__(position, size, color, image)
        
        self.energy = 100 # The energy of given entity

