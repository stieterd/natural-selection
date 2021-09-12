import pygame
from pygame.transform import average_color
from entities.dna import Dna

class Day: # Simple struct working as a datacontainer
    """
    Contains all the data(stats) this day 
    """
    day_nmbr: int
    avg_dna: Dna
    