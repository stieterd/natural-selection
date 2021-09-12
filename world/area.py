from entities.entity import Entity
from world.hashmap import HashMap, dict_setdefault

class World(HashMap):
    
    def __init__(self, cell_size: float, entities: dict) -> HashMap:
        """
        Build a HashMap from a list of entities.
        Each type of Entity will get its own hashmap
        Key hashing is not hashing so keys are same for all hashmaps :slight_smile:
        """

        super().__init__(cell_size)

        for entType in entities:
            
            for ent in entities[entType]:
                
                dict_setdefault(dict_setdefault( self.grid, self.key(ent), {}), ent.entityType, []).append(ent)
   
                #dict_setdefault(self.grid, self.key(ent),[]).append(ent)
        

    def looping(self):
        """
            Looping through all the entities and applying their behaviour functions to them
        """
        for entity in self.hashmaps: # iterating through all the entitytypes in our world
            for gridCell in list(self.hashmaps[entity].grid): # iterating through all the cells on the grid
                for creature in self.hashmaps[entity].grid[gridCell]: # iterating through all 
                    pass