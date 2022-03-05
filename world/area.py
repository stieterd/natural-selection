from entities.dna import Dna, Property
from engine.window import Window
from engine.mathfunctions import *

from entities.herbivores import Herbivore
from entities.entity import Entity
from entities.types import EntTypes
from entities.apple import Apple, generate_apples

from world.hashmap import HashMap, dict_setdefault
from world.days import Day

import random

class World(HashMap):
    
    current_day: Day # OH HAPPY DAAYYYYYYYYYYYYYYYYY
    n_herbivores: int # Amount of herbivores alive on the world
    average_dna_values: list # The average weights of each dna property of all the herbivores alive
    
    def __init__(self, cell_size: float, entities: dict, day: Day) -> HashMap:
        """
        Build a HashMap from a list of entities.
        Each type of Entity will get its own hashmap
        Key hashing is not hashing so keys are same for all hashmaps :slight_smile:
        """
        self.current_day = day
        self.n_herbivores = len(entities[EntTypes.herbivores])
        self.average_dna_values = self.get_avg_dna(list(entities.values())[0])

        # Setup statistics file
        self.update_stats(True)

        # Calling parent class
        super().__init__(cell_size) 

        # Set the entities onto the grid
        self.set_entities_on_grid(entities)

    def set_entities_on_grid(self, entities: dict):
        self.grid = {}
        for entType in entities:
            for ent in entities[entType]:
                dict_setdefault(dict_setdefault( self.grid, self.key(ent), {}), ent.entityType, []).append(ent)
                
                #dict_setdefault(self.grid, self.key(ent),[]).append(ent)
    
    def new_day(self, win: Window, config: dict, appleArguments:list) -> None:

        # Retarded way of initializing new day object and assigning it to current day lmao :(
        d_nmbr = self.current_day.day_nmbr + 1 # The number of the current day increased by one 
        self.current_day = Day(self.current_day.frames_per_sec, d_nmbr)

        # Update the new day variables for all herbivores
        
        self.update_entity_variables()

        # Birth of new entities and death of weak entities
        entities_alive = self.give_entities_birth(config) # Born
        survived_entities = self.get_surviving_entities() # Survived
        
        entities_alive.extend(survived_entities)

        # Retrieve the average dna :)
        self.average_dna_values = self.get_avg_dna(entities_alive)

        # Updating statistics file
        self.update_stats()

        # Setting the remaining entities onto the grid
        herbivore_amount = len(entities_alive)
        self.n_herbivores = herbivore_amount
        assert herbivore_amount > 0, "All the entities died!"
        
        # Fixing startposition of the remaining entities
        entityDistance = win.config.screen_height / herbivore_amount
        for idx, entity in enumerate(entities_alive):
            entity.position = Vector(config["creature_start_x"], (idx) * entityDistance)

        # Putting the apples onto the grid :yum:
        apples_list = generate_apples(*appleArguments)
        random.shuffle(entities_alive)
        all_entities = {EntTypes.herbivores: entities_alive, EntTypes.apples: apples_list}
        
        self.set_entities_on_grid(all_entities)       

    def update_stats(self, firstday=False):
        """Update statistics in a txt doc (can be converted to csv lmaoooo)"""
        #print(self.average_dna_values)
        my_average_dna = Dna(*self.average_dna_values)
        factor = 10**3
        data = f"{self.current_day.day_nmbr};{int(my_average_dna.size*factor/2)};{int(my_average_dna.speed*factor/2)};{int(my_average_dna.senserange*factor/2)};{self.n_herbivores}\n"
        if firstday:
            with open("stats.txt", "w") as fw:
                fw.write(f"day;avg_size;avg_speed;avg_senserange;n_creatures\n")
                fw.write(data)
        else:
            with open("stats.txt", "a") as fw:
                fw.write(data)
    def update_entity_variables(self) -> None:
        """Updates the entity methods each new day"""
        for gridCell in list(self.grid): # MIGHT REMOVE LIST CAST
            for entityType in list(self.grid[gridCell]):       
                for entity in self.grid[gridCell][entityType]:
                    if entity.entityType != EntTypes.herbivores: # String comparison takes a lot of processing power, ill probably switch to integers
                        continue
                    entity: Herbivore 

                    # Setting up variables for each herbivore
                    entity.days += 1
                    entity.position = entity.START_POSITION
                    entity.energy -= entity.energy_need

    def get_surviving_entities(self) -> list:
        """First call update_entity_variables before calling this function"""
        # Empty lists for assigning entities for next day 
        surviving_entities = []

        for gridCell in list(self.grid): # MIGHT REMOVE LIST CAST
            for entityType in list(self.grid[gridCell]):       
                for entity in self.grid[gridCell][entityType]:
                    if entity.entityType != EntTypes.herbivores: # String comparison takes a lot of processing power, ill probably switch to integers
                        continue
                    # Check if still alive
                    if entity.days > entity.lifespan or entity.energy < 0:
                        continue
            
                    # Survived
                    surviving_entities.append(entity)
        return surviving_entities

    def give_entities_birth(self, config) -> list:
        """First call update_entity_variables before calling this function"""
        # Empty lists for assigning entities for next day 
        entities_replicate: list[Herbivore] = []
        surviving_entities: list[Herbivore] = []
        for gridCell in list(self.grid): # MIGHT REMOVE LIST CAST
            for entityType in list(self.grid[gridCell]):       
                for entity in self.grid[gridCell][entityType]:
                    if entity.entityType != EntTypes.herbivores: # String comparison takes a lot of processing power, ill probably switch to integers
                        continue    
                    entity: Herbivore 
                    # Mating potential
                    if entity.energy > entity.MATING_ENERGY_COST:
                        entities_replicate.append(entity)
        random.shuffle(entities_replicate)
        # Birth of new entities
        for idx in range(len(entities_replicate)//2):
            surviving_entities.extend(entities_replicate[2*idx].giving_birth_to_multiple_creatures(entities_replicate[2*idx+1], config))
        return surviving_entities

    def looping(self):
        """
            Looping through all the entities and applying their behaviour functions to them
        """
        for entity in self.hashmaps: # iterating through all the entitytypes in our world
            for gridCell in list(self.hashmaps[entity].grid): # iterating through all the cells on the grid
                for creature in self.hashmaps[entity].grid[gridCell]: # iterating through all 
                    pass

    def get_avg_dna(self, entities:list) -> list:

        """
        Retrieving the average dna values
        """
        
        properties = []
        
        # DOING STUPID UNREADABLE FOR LOOP SO I DONT HAVE TO CHANGE IT EVERY TIME DNA ATTRIBUTES CHANGE
        ent: Herbivore
        n: int = 0
        #print(entities)
        if len(entities) < 1:
            raise TypeError("All entities are dead (RIP) :(")
        for idx,ent in enumerate(entities):
            n += 1
            property: Property
            for idx1,property in enumerate(ent.dna.get_properties()):
                
                if idx == 0:
                    properties.append(property.get_value())
                else:
                    properties[idx1] += property.get_value()

        result = []
        for property in properties:
            result.append(property/n)
        
        return result