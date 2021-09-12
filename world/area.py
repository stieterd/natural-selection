from world.hashmap import HashMap, dict_setdefault

class World(HashMap):
    
    def __init__(self, cell_size: float, entities: list) -> HashMap:
        """
        Build a HashMap from a list of entities.
        """
        super().__init__(cell_size)
        
        for ent in entities:
            
            dict_setdefault(self.grid, self.key(ent),[]).append(ent)
        