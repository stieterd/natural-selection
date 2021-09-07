import pygame
from engine.mathfunctions import *
from engine.drawable import Drawable, DrawTypes
from engine.window_settings import WindowSettings


class Entity(Drawable):

    # Constructor for entity -> sets position, size
    def __init__(self, position: Vector, size: Vector, color: Color, image: pygame.image) -> None:

        self.position: Vector = position
        self.size: Vector = size

        self.color: Color = color
        self.collisionBox: pygame.Rect = pygame.Rect(tuple(self.position), tuple(self.size))
        if image == None:
            self.image = None
        else:
            self.image: pygame.image =  pygame.transform.scale(image, tuple(size)) # dget imager ihiihi

    # Change the position 
    def move(self, translate: Vector, winsettings: WindowSettings ) -> None:

        self.position += translate
        
        if self.position.x < 0:
            self.position.x += abs(translate.x)
        elif self.position.x + self.size.x > winsettings.screen_width:
            self.position.x -= abs(translate.x)

        if self.position.y < 0:
            self.position.y += abs(translate.y)
        elif self.position.y + self.size.y > winsettings.screen_height:
            self.position.y -= abs(translate.y)

        #if 0 + self.size.y <= self.position.y + translate.y + self.size.y<= winsettings.screen_height - self.size.y:
        #    self.position.y += translate.y
        

    # virtual method, can be overwritten by parent class, draws entity to the screen
    def draw_entity(self, screen: pygame.Surface, drawmethod: int) -> None:

        if drawmethod == DrawTypes.RECT:
            super().draw_rect(screen, tuple(self.position), tuple(self.size), tuple(self.color))
        
        elif drawmethod == DrawTypes.IMAGE:
            super().draw_image(screen, self.image, tuple(self.position))


    def collision(self, entity):
        pass
        #if entity.x < self.x < entity.x + entity.size and 