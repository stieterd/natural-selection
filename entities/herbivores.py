from engine.window_settings import WindowSettings
from engine.mathfunctions import *
from engine.window import Window

from entities.types import EntTypes
from entities.entity import Entity
from entities.dna import Allel, Dna, Property
from entities.entity_factors import HerbivoreFactors, AppleFactors

import pygame
import random

def generate_herbivores(win: Window, config: dict, nEntities: int, image: pygame.image) -> list:

    entityDistance = win.config.screen_height/ nEntities
    
    herbivores = []

    for x in range(nEntities):   
        pos: Vector = Vector(config["creature_start_x"], (x) * entityDistance)
        color: Color = DefinedColors.yellow

        sizeD: Allel = Allel(config["creature_size"], True)
        senserangeD: Allel = Allel(config["creature_sense"], False)
        speedD: Allel = Allel(config["creature_speed"], True)

        sizeM: Allel = Allel(config["creature_size"], False)
        senserangeM: Allel = Allel(config["creature_sense"], True)
        speedM: Allel = Allel(config["creature_speed"], False)

        dna: Dna = Dna(Property(sizeD, sizeM), Property(speedD, speedM), Property(senserangeD, senserangeM))

        ent: Herbivore = Herbivore(EntTypes.herbivores, pos, dna, config["creature_life_length_d"], color, image)

        herbivores.append(ent)

    return herbivores

class Herbivore(Entity):

    """
    Herbivores are one of the three Entities that will be tested in this experiment.
    Herbivores can only eat vegitibles, this means they wont form a threat to each other.
    """

    

    def __init__(self, entityType: int, position: Vector, dna: Dna, lifespan: int, color: Color, image: pygame.image) -> None:
        super().__init__(entityType, position, Vector(int(dna.size.get_value()*HerbivoreFactors.SIZE), int(dna.size.get_value()*HerbivoreFactors.SIZE)), color, image)
        
        # Entity Properties
        self.dna: Dna = dna # DNA of the entity 
        self.max_energy: int = int(self.dna.size.get_value() * HerbivoreFactors.SIZE * AppleFactors.MAX_APPLES_FACTOR)
        
        self.STARTING_ENERGY: float = 0.5 * dna.size.get_value() * dna.speed.get_value()**2 + 0.25 * dna.senserange.get_value() # The energy an entity starts with when entering the first day
        self.MATING_ENERGY_COST = self.STARTING_ENERGY/2 
        
        ## Variables controlling if entity is alive
        self.energy_need: float = self.STARTING_ENERGY # Need to write formula for it :) size^3 * speed^2 + sense
        
        self.days: int = 0 # Survived days
        self.energy: int = self.STARTING_ENERGY # The current energy of given entity
        self.lifespan: int = lifespan # Lifespan in days, days > lifespan -> entity dies

        
        ## Walking algorithm
        self.endposition: Vector = None


    def move_towards(self, point: Vector, winsettings: WindowSettings) -> None:

        # get the distance between the position and the point to move towards :)
        x = point.x - self.position.x 
        y = point.y - self.position.y

        # Set up translation of the position
        transl_x = is_positive(x) * self.dna.speed.get_value() * HerbivoreFactors.SPEED if abs(x) > abs(self.dna.speed.get_value() * HerbivoreFactors.SPEED) else x
        transl_y = is_positive(y) * self.dna.speed.get_value() * HerbivoreFactors.SPEED if abs(y) > abs(self.dna.speed.get_value() * HerbivoreFactors.SPEED) else y

        # Movement
        self.move(Vector(transl_x,transl_y), winsettings)

    def walk_path(self, winsettings: WindowSettings):
        
        # Check if endposition is hit, if so generate a new one
        if self.endposition == None or abs(self.position.x - self.endposition.x) < self.msize.x*HerbivoreFactors.SIZE and abs(self.position.y - self.endposition.y) < self.msize.y*HerbivoreFactors.SIZE:
            self.endposition = Vector(random.randint(0, winsettings.screen_width - self.msize.x*HerbivoreFactors.SIZE), random.randint(0, winsettings.screen_height - self.msize.y*HerbivoreFactors.SIZE))
        # Move towards new endposition
        self.move_towards(self.endposition, winsettings)

    def giving_birth_to_multiple_creatures(self, otherParent: "Herbivore", config: dict):

        children = []
        # Subtracts energy for every new child that gets born until out of energy
        while self.energy - self.MATING_ENERGY_COST > 0 and otherParent.energy - otherParent.MATING_ENERGY_COST > 0:
            children.append(self.give_birth(otherParent, config))
        return children

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
        for arg in new_dna_args:
            print(arg.get_value())
        print()
        return Herbivore(otherParent.entityType, otherParent.position, Dna(*new_dna_args), config["creature_life_length_d"], otherParent.color, otherParent.image)
    
    def mutate(self, value:float, mutation_rate:float) -> float:

        mutate_fac: float = (random.random() * 2 - 1) * mutation_rate  # Random float between -1 and 1 multiplied by the mutation rate
        return float(value + mutate_fac) 

    def remove_energy(self):
        pass

    def pick_apple(self):
        pass
