from engine.window_settings import WindowSettings
from engine.mathfunctions import *
from engine.window import Window

from entities.types import EntTypes
from entities.entity import Entity
from entities.dna import Dna

import pygame

def generate_herbivores(win: Window, config: dict, nEntities: int, image: pygame.image) -> list:

    entityDistance = win.config.screen_height// nEntities

    herbivores = []

    for x in range(nEntities):   
        pos: Vector = Vector(20, x * entityDistance)
        color: Color = DefinedColors.black

        size: Vector = Vector(config["creature_size"], config["creature_size"])
        senserange: float = config["creature_sense"]
        speed: int = config["creature_speed"]

        dna: Dna = Dna(size, senserange, speed)

        ent: Herbivore = Herbivore(EntTypes.herbivores, pos, dna, config["creature_life_length_d"], color, image)

        herbivores.append(ent)

    return herbivores

class Herbivore(Entity):

    """
    Herbivores are one of the three Entities that will be tested in this experiment.
    Herbivores can only eat vegitibles, this means they wont form a threat to each other.
    """

    STARTING_ENERGY = 100 # The energy an entity starts with when entering the first day
    MATING_ENERGY_COST = 200 

    def __init__(self, entityType: int, position: Vector, dna: Dna, lifespan: int, color: Color, image: pygame.image) -> None:
        super().__init__(entityType, position, dna.size, color, image)
        
        #self.senserange = dna.senserange # This is the range from where the entity will be able to see an apple and will go towards it
        #self.speed = dna.speed # Speed of entity

        self.days = 0

        self.energy_need = dna.size.x**3 * dna.speed**2 + dna.senserange # Need to write formula for it :) size^3 * speed^2 + sense
        self.energy = self.STARTING_ENERGY # The energy of given entity
        self.lifespan = lifespan # Lifespan in days, lifespan expires -> entity dies

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
