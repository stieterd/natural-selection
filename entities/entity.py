import pygame
from engine.mathfunctions import *
from engine.drawable import Drawable, DrawTypes
from engine.window_settings import WindowSettings


class Entity(Drawable):

    """
    Base Entity: Every interactable object on the screen inherits this class
    """
    
    # Constructor for entity -> sets position, size
    def __init__(self, entityType, position: Vector, size: Vector, color: Color, image: pygame.image) -> None:

        self.START_POSITION: Vector = position # CONSTANT, WONT EVER CHANGE

        self.entityType = entityType

        self.position: Vector = position
        
        self.size: Vector = size

        self.color: Color = color
        
        if image == None:
            self.image = None
        else:
            self.image: pygame.image =  pygame.transform.scale(image, tuple(size)) # dget imager ihiihi

    def get_center_pos(self) -> Vector:

        return self.position + self.size/2

    # Change the position 
    def move(self, translate: Vector, winsettings: WindowSettings) -> None:

        self.position += translate
        
        if self.position.x < 0:
            self.position.x += abs(translate.x)
        elif self.position.x + self.size.x > winsettings.screen_width:
            self.position.x -= abs(translate.x)

        if self.position.y < 0:
            self.position.y += abs(translate.y)
        elif self.position.y + self.size.y > winsettings.screen_height:
            self.position.y -= abs(translate.y)
        
    # virtual method, may be overwritten by parent class, draws entity to the screen
    def draw_entity(self, screen: pygame.Surface, drawmethod: int) -> None:

        if drawmethod == DrawTypes.RECT:
            super().draw_rect(screen, tuple(self.position), tuple(self.size), tuple(self.color))
        
        elif drawmethod == DrawTypes.IMAGE:
            super().draw_image(screen, self.image, tuple(self.position))

    # virtual method, may be overwritten by parent class, returns if entity collides with other entity
    def collides(self, entity: "Entity") -> bool: 
        if (self.position.x>=entity.position.x + entity.size.x) or (self.position.x + self.size.x<=entity.position.x) or (self.position.y + self.size.y<=entity.position.y) or (self.position.y>=entity.position.y + entity.size.y):
            return False
            
        return True
