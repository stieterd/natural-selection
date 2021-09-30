from engine.window_settings import WindowSettings
from engine.mathfunctions import *
from engine.window import Window

from entities.types import EntTypes
from entities.entity import Entity
from entities.dna import Allel, Dna, Property

import pygame
import random

def generate_herbivores(win: Window, config: dict, nEntities: int, image: pygame.image) -> list:

    entityDistance = win.config.screen_height/ nEntities
    
    herbivores = []

    for x in range(nEntities):   
        pos: Vector = Vector(config["creature_start_x"], (x) * entityDistance)
        color: Color = DefinedColors.yellow

        sizeD: Allel = Allel(config["creature_size"], True)
        senserangeD: Allel = Allel(config["creature_sense"], True)
        speedD: Allel = Allel(config["creature_speed"], True)

        sizeM: Allel = Allel(config["creature_size"], True)
        senserangeM: Allel = Allel(config["creature_sense"], True)
        speedM: Allel = Allel(config["creature_speed"], True)

        dna: Dna = Dna(Property(sizeD, sizeM), Property(senserangeD, senserangeM), Property(speedD, speedM))

        ent: Herbivore = Herbivore(EntTypes.herbivores, pos, dna, config["creature_life_length_d"], color, image)

        herbivores.append(ent)

    return herbivores

class Herbivore(Entity):

    """
    Herbivores are one of the three Entities that will be tested in this experiment.
    Herbivores can only eat vegitibles, this means they wont form a threat to each other.
    """

    STARTING_ENERGY = 5000 # The energy an entity starts with when entering the first day
    MATING_ENERGY_COST = STARTING_ENERGY/2 

    def __init__(self, entityType: int, position: Vector, dna: Dna, lifespan: int, color: Color, image: pygame.image) -> None:
        super().__init__(entityType, position, Vector(int(dna.size.get_value()), int(dna.size.get_value())), color, image)
        
        ## Variables controlling if entity is alive
        self.energy_need: float = dna.size.get_value()**3 * dna.speed.get_value()**2 + dna.senserange.get_value() # Need to write formula for it :) size^3 * speed^2 + sense
        
        self.days: int = 0 # Survived days
        self.energy: int = self.STARTING_ENERGY # The current energy of given entity
        self.lifespan: int = lifespan # Lifespan in days, days > lifespan -> entity dies

        # Entity Properties
        self.dna: Dna = dna # DNA of the entity 
        
        ## Walking algorithm
        self.endposition: Vector = Vector(0,0)

    def move_towards(self, point: Vector, winsettings: WindowSettings) -> None:

        # get the distance between the position and the point to move towards :)
        x = point.x - self.position.x 
        y = point.y - self.position.y

        # Set up translation of the position
        transl_x = is_positive(x) * self.dna.speed.get_value() if abs(x) > abs(self.dna.speed.get_value()) else x
        transl_y = is_positive(y) * self.dna.speed.get_value() if abs(y) > abs(self.dna.speed.get_value()) else y

        # Movement
        self.move(Vector(transl_x,transl_y), winsettings)

    def walk_path(self, WIDTH: int, HEIGHT: int):
        pass

    def give_birth(self, otherParent: "Herbivore", config: dict) -> "Herbivore":

        # The new dna properties for the child
        new_dna_args = []
        # Putting the dna properties in an array
        my_values = self.dna.get_properties()
        other_values = otherParent.dna.get_properties()
        
        # Setting the new dna properties for our child
        for idx in range(len(my_values)):

            myPassingAllel: Allel = my_values[idx].pAllel if random.randint(0,1) == 1 else my_values[idx].mAllel # Fancy inline if statement :hot_face_emoji:
            othersPassingAllel: Allel = other_values[idx].pAllel if random.randint(0,1) == 1 else other_values[idx].mAllel

            childProperty: Property = Property(Allel(self.mutate(myPassingAllel.value, config["creature_mutation_rate"]), myPassingAllel.dominant), Allel(self.mutate(othersPassingAllel.value, config["creature_mutation_rate"]), othersPassingAllel.dominant))
            new_dna_args.append(childProperty)
        
        # Subtracting the energy cost of making a child
        otherParent.energy -= otherParent.MATING_ENERGY_COST
        self.energy -= self.MATING_ENERGY_COST
        
        return Herbivore(otherParent.entityType, otherParent.position, Dna(*new_dna_args), config["creature_life_length_d"], otherParent.color, otherParent.image)
    
    def mutate(self, value:float, mutation_rate:float) -> float:
        mutate_fac: float = (random.random()*2 - 1) * mutation_rate * value # Random float between -1 and 1 multiplied by the mutation rate
        return float(value + mutate_fac) 

    def remove_energy(self):
        pass

    def pick_apple(self):
        pass
