
from entities.types import EntTypes
from engine.mathfunctions import *
from entities.entity import Entity

import random
import math
import time

# this is because dict.setdefault does not work. 
def dict_setdefault(dictionary: dict, key: str, value: list) -> list or None:
    """
    If dictionary key exists, return corresponding value
    If dictionary key does not exist apply value to new key 
    """
    r = dictionary.get(key,value)
    if key not in dictionary:
        dictionary[key] = value
    return r


class HashMap(object):
    """
    Hashmap is a a spatial index which can be used for a broad-phase
    collision detection strategy.
    """
    def __init__(self, cell_size: float) -> None:
        self.cell_size: float = cell_size
        self.grid: dict = {}
    
    def get_entity_amount(self, entType:int):
        n = 0
        for cell in self.grid.values():
            if entType in cell:
                n += len(cell[entType])
        return n

    def key(self, entity: Entity) -> tuple:
        cell_size: float = self.cell_size
        return (
            int((math.floor(entity.position.x/cell_size))*cell_size),
            int((math.floor(entity.position.y/cell_size))*cell_size),
            
        )
    
    def key_pos(self, position: Vector) -> tuple:
        cell_size: float = self.cell_size

        return (
            int((math.floor(position.x/cell_size))*cell_size),
            int((math.floor(position.y/cell_size))*cell_size),
        )
    
    def remove_from_key(self, key, entity: Entity) -> None:
        """
        Remove entity from hashmap
        """
        
        dict_setdefault(dict_setdefault( self.grid, key, {}), entity.entityType, []).remove(entity)
        

    def insert(self, entity: Entity) -> None:
        """
        Insert entity into the hashmap.
        """
        
        dict_setdefault(dict_setdefault( self.grid, self.key(entity), {}), entity.entityType, []).append(entity)
   
    def query(self, entity: Entity, entType:int) -> list:
        """
        Return all objects in the cell specified by entity.
        """
        
        return dict_setdefault(dict_setdefault( self.grid, self.key(entity), {}), entType, [])


    def query_from_pos(self, pos: Vector, entType: int):
        """
        Return all objects in the cell specified by point.
        """

        return dict_setdefault(dict_setdefault( self.grid, self.key_pos(pos), {}), entType, [])
