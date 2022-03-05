from dataclasses import dataclass
from dataclasses import asdict


class Allel:
    def __init__(self, value:float, dominant:bool) -> None:
        self.value: float = value
        self.dominant: bool = dominant

class Property:

    def __init__(self, pAllel: Allel, mAllel: Allel) -> None:
        self.pAllel: Allel = pAllel
        self.mAllel: Allel = mAllel
    
    def get_value(self):
        return self.pAllel.value + self.mAllel.value

@dataclass
class Dna(object):

    size: Property
    speed: Property
    senserange: Property

    def __init__(self, size: Property, speed: Property, senserange: Property):
        
        self.size = size
        self.speed = speed
        self.senserange = senserange

    def get_properties(self) -> list:
        return list(asdict(self).values())

    def get_dict(self) -> dict:
        return asdict(self)

    def __iter__(self):
        for i in [self.size, self.senserange, self.speed]:
            yield i
