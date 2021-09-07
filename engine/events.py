import pygame
from dataclasses import dataclass

@dataclass
class Event_Types(object): # Basically a struct with events lmao
    event_running: bool
    event_pause: bool

class Events:

    # Returns value to running method of Window class
    def check_events(event_type: int, events_struct: Event_Types) -> bool:
        
        # QUIT
        pressed = pygame.key.get_pressed()
        if event_type == pygame.QUIT:
            events_struct.event_running = not events_struct.event_running
        
        # PAUSE
        if pressed[pygame.K_ESCAPE]:
            events_struct.event_pause = not events_struct.event_pause
        
        return events_struct