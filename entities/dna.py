from dataclasses import dataclass

class Dna:

    def __init__(self, size: int, senserange: float, speed: int):
        
        self.size = size
        self.senserange = senserange
        self.speed = speed