import pygame

from entities.entity import *
from engine.events import Events, Event_Types
from engine.window_settings import WindowSettings

pygame.font.init()

# Window on top of which everything will be drawn
class Window:

    FONT = pygame.font.SysFont("Arial", 26) # 18 size font
    CLOCK = pygame.time.Clock()

    # Initializing the pygame Window 
    def __init__(self, width: int, height: int) -> None:


        self.events_struct = Event_Types(event_running=True, event_pause=False)
        self.config = WindowSettings(width, height)

        self.screen = pygame.display.set_mode((self.config.screen_width, self.config.screen_height), pygame.RESIZABLE) # surface on which we draw 

    # Look what events just processed and execute functions written in events.py
    def check_events(self) -> None:
        for event in pygame.event.get():
            self.events_struct = Events.check_events(event, event.type, self.events_struct)
    
    def update_fps(self):
        fps = str(int(self.CLOCK.get_fps())) + " FPS"
        fps_text = self.FONT.render(fps, 1, tuple(DefinedColors.blue))
        return fps_text

    # draw an Entity to the screen
    def draw_entity(self, ent: Entity) -> None:
        ent.draw_entity(self.screen)

    # draws the current settings window to the screen (NOT WORKING YET)
    def draw_settings(self) -> None:
        pass

    # pause function
    def paused(self) -> None:
        while self.events_struct.event_pause:
            self.check_events()

    # Change resolution (NOT WORKING YET)
    def change_resolution(self, new_width: int, new_height: int) -> None:

        self.config.screen_width = new_width
        self.config.screen_height = new_height

    # Toggling mode to fullscreen
    def toggle_fullscreen(self) -> None:

        display = (self.config.screen_width, self.config.screen_height)

        if pygame.display.get_driver()=='x11':
            pygame.display.toggle_fullscreen()
        else:
            acopy=self.screen.copy()                    
        
        if self.config.fullscreen:
            screen=pygame.display.set_mode(display)
        else:
            screen=pygame.display.set_mode(display, pygame.FULLSCREEN)
            self.config.fullscreen= not self.config.fullscreen
            screen.blit(acopy, (0,0))                    
            pygame.display.update()