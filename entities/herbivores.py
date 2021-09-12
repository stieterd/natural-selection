import pygame

from engine.mathfunctions import *
from entities.entity import Entity


class Herbivore(Entity):

    """
    Herbivores are one of the three Entities that will be tested in this experiment.
    Herbivores can only eat vegitibles, this means they wont form a threat to each other.
    """

    STARTING_ENERGY = 100 # The energy an entity starts with when entering the first day

    def __init__(self, position: Vector, size: Vector, senserange: float, color: Color, image: pygame.image) -> None:
        super().__init__(position, size, color, image)
        
        self.senserange = senserange # This is the range from where the entity will be able to see an apple and will go towards it

        self.energy = self.STARTING_ENERGY # The energy of given entity
        self.lifespan = 60 # Lifespan in seconds, lifespan expires -> entity dies

        self.dna = None # placeholder 

    def remove_energy(self):
        pass

    def pick_apple(self):
        pass
