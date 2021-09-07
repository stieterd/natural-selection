
import pygame
from enum import Enum

# Enum for the drawtypes
class DrawTypes(Enum):

    RECT = 1 # Draw object as rectangle
    CIRCLE = 2 # Draw object as circle
    IMAGE = 3 # Draw object as image


# parent class for all objects that can draw
class Drawable:
    
    def draw_rect(self, screen: pygame.Surface, position: tuple, size: tuple, color: tuple) -> pygame.Rect:
        rect = pygame.draw.rect(screen, color, (position, size))

        return rect

    def draw_image(self, screen: pygame.Surface, img: pygame.image, position: tuple) -> pygame.Rect:

        screen.blit(img, position)