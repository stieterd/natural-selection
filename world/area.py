
from engine.mathfunctions import *
from entities.entity import Entity

from typing import TypedDict
import random
from dataclasses import dataclass

import math
import time



# this is because dict.setdefault does not work. 
def dict_setdefault(dictionary: dict, key: str, value: list) -> list or None:
    #D.setdefault(k[,d]) -&gt; D.get(k,d), also set D[k]=d if k not in D
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


    def key(self, entity: Entity) -> tuple:
        cell_size: float = self.cell_size
        return (
            int((math.floor(entity.position.x/cell_size))*cell_size),
            int((math.floor(entity.position.y/cell_size))*cell_size),
            #int((math.floor(point[2]/cell_size))*cell_size)
        )
    
    def remove_from_key(self, key, entity: Entity) -> None:
        """
        Remove entity from hashmap
        """
        
        #l1 = len(dict_setdefault( self.grid, key, []))
        
        dict_setdefault( self.grid, key, []).remove(entity)
        #l2 = len(dict_setdefault( self.grid, key, []))
        #print(l1 > l2)

    def insert(self, entity: Entity) -> None:
        """
        Insert entity into the hashmap.
        """
        #self.grid.setdefault(self.key(point), []).append(point)
        dict_setdefault( self.grid, self.key(entity), []).append(entity)
   
    def query(self, entity: Entity) -> list:
        """
        Return all objects in the cell specified by point.
        """
        #return self.grid.setdefault(self.key(point), [])
        return dict_setdefault( self.grid, self.key(entity), [])

def from_entities(cell_size: float, entities: list) -> HashMap:
    """
    Build a HashMap from a list of entities.
    """
    hashmap = HashMap(cell_size)
    #setdefault = hashmap.grid.setdefault
    #key = hashmap.key
    for ent in entities:
        #setdefault(key(point),[]).append(point)
        dict_setdefault(hashmap.grid, hashmap.key(ent),[]).append(ent)
    return hashmap

