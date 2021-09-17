import pygame
from pygame.transform import average_color
from entities.dna import Dna
from dataclasses import dataclass

@dataclass
class Day: # Simple struct working as a datacontainer
    """
    Contains all the data(stats) this day - struct
    """
    frames_per_sec: int
    day_nmbr: int
    frames_passed: int = 0

    def get_passed_seconds(self) -> int:
        return self.frames_passed//self.frames_per_sec
    