import math

# Vector "Struct", contains float x,y 
class Vector:

    def __init__(self, x: float, y: float) -> None:

        self.x = x
        self.y = y

    def __iter__(self):
        for i in [self.x, self.y]:
            yield i

    def __add__(self, adder):

        self.x += adder.x
        self.y += adder.y

        return self
    
    
    def __str__(self):
        return f"Vector({self.x},{self.y})"
     

# Vector3 "Struct", contains float x,y,z
class Vector3:

    def __init__(self, x: float, y: float, z: float) -> None:

        self.x = x
        self.y = y
        self.z = z
    
    def __iter__(self):
        for i in [self.x, self.y, self.z]:
            yield i


# Color is basically a Vector3 class called Color lmao -> RGB
class Color(Vector3): 
    
    @classmethod
    def from_hex(cls, hex_value: str): # cls is passed from classmethod dunder
        assert len(hex_value) == 7 and hex_value[0] == "#", "Error: Wrong hex value given to initialize color!"
        hex_value = hex_value[1:] # strip the "#" from hex_value, we only need the hexadecimal DWORDS
        arguments = [int(hex_value[x*2:2+x*2], base=16) for x in range(len(hex_value)//2)] # list comprehension to find all the colorvalues

        return cls(*arguments) # return the class object that is created

# Some basic colors :)
class DefinedColors:

    black = Color(0,0,0)
    white = Color(255,255,255)

    red = Color(225, 30, 30)
    green = Color(30, 225, 30)
    blue = Color(30, 30, 225)

class simpleMath:

    def clamp(x: float, a: float, b: float) -> float: # Clamp the value(x) in between two values (a and b)
        return math.min(math.max(x,a),b)
    
    def sat(x: float) -> float: # clamp the value between 0 and 1
        return math.min(math.max(x, 0.0), 1.0)

    def lerp(x: float, a: float, b: float) -> float: # lineair interpolation lol
        return x * (b-a) + a