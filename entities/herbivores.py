from engine.window_settings import WindowSettings
from entities.dna import Dna
import pygame

from engine.mathfunctions import *
from entities.entity import Entity


class Herbivore(Entity):

    """
    Herbivores are one of the three Entities that will be tested in this experiment.
    Herbivores can only eat vegitibles, this means they wont form a threat to each other.
    """

    STARTING_ENERGY = 100 # The energy an entity starts with when entering the first day

    def __init__(self, entityType: int, position: Vector, dna: Dna, color: Color, image: pygame.image) -> None:
        super().__init__(entityType, position, dna.size, color, image)
        
        #self.senserange = dna.senserange # This is the range from where the entity will be able to see an apple and will go towards it
        #self.speed = dna.speed # Speed of entity

        self.energy = self.STARTING_ENERGY # The energy of given entity
        self.lifespan = 60 # Lifespan in seconds, lifespan expires -> entity dies

        self.dna = dna # placeholder 

    def move_towards(self, point: Vector, winsettings: WindowSettings) -> None:

        x = point.x - self.position.x 
        y = point.y - self.position.y

        transl_x = is_positive(x) * self.dna.speed if abs(x) > abs(self.dna.speed) else x
        transl_y = is_positive(y) * self.dna.speed if abs(y) > abs(self.dna.speed) else y

        self.move(Vector(transl_x,transl_y), winsettings)


    def remove_energy(self):
        pass

    def pick_apple(self):
        pass
