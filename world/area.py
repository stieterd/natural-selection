from engine.window import Window
from entities.herbivores import Herbivore
from entities.entity import Entity
from entities.types import EntTypes
from entities.apple import Apple, generate_apples

from world.hashmap import HashMap, dict_setdefault
from world.days import Day

class World(HashMap):
    
    def __init__(self, cell_size: float, entities: dict, day: Day) -> HashMap:
        """
        Build a HashMap from a list of entities.
        Each type of Entity will get its own hashmap
        Key hashing is not hashing so keys are same for all hashmaps :slight_smile:
        """
        self.current_day = day

        super().__init__(cell_size)

        self.set_entities_on_grid(entities)

    def set_entities_on_grid(self, entities: dict):
        self.grid = {}
        for entType in entities:
            for ent in entities[entType]:
                dict_setdefault(dict_setdefault( self.grid, self.key(ent), {}), ent.entityType, []).append(ent)
                #dict_setdefault(self.grid, self.key(ent),[]).append(ent)
    
    def new_day(self, appleArguments:list) -> None:

        d_nmbr = self.current_day.day_nmbr + 1
        self.current_day = Day(self.current_day.frames_per_sec, d_nmbr)

        entities_replicate = []
        surviving_entities = []

        for gridCell in list(self.grid): # MIGHT REMOVE LIST CAST
            for entityType in list(self.grid[gridCell]):       
                for entity in self.grid[gridCell][entityType]:
                    if entity.entityType == EntTypes.herbivores: # String comparison takes a lot of processing power, ill probably switch to integers
                        entity: Herbivore 

                        # Setting up variables for each herbivore
                        entity.days += 1
                        entity.position = entity.START_POSITION
                        entity.energy -= entity.energy_need

                        # Check if still alive
                        if entity.days > entity.lifespan or entity.energy < 0:
                            continue
                        
                        # Mating potential
                        if entity.energy > entity.MATING_ENERGY_COST:
                            entities_replicate.append(entity)

                        # Survived
                        surviving_entities.append(entity)

        apples_list = generate_apples(*appleArguments)
        all_entities = {EntTypes.herbivores: surviving_entities, EntTypes.apples: apples_list}
        self.set_entities_on_grid(all_entities)

    def looping(self):
        """
            Looping through all the entities and applying their behaviour functions to them
        """
        for entity in self.hashmaps: # iterating through all the entitytypes in our world
            for gridCell in list(self.hashmaps[entity].grid): # iterating through all the cells on the grid
                for creature in self.hashmaps[entity].grid[gridCell]: # iterating through all 
                    pass