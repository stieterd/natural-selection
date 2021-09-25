from engine.window import Window
import pygame
from pygame.transform import average_color
from entities.dna import Dna
from dataclasses import dataclass
from engine.mathfunctions import DefinedColors

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
    
    '''
    def show_passed_seconds(self, win: Window):

        passed_sec = str(int(self.get_passed_seconds()))
        passed_sec_txt = win.FONT.render(passed_sec, 1, tuple(DefinedColors.red))
        win.screen.blit(passed_sec_txt, (10,30))
    '''