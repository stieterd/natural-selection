import pygame
from dataclasses import dataclass

@dataclass
class Event_Types(object): # Basically a struct with events lmao
    event_running: bool
    event_pause: bool
    
    showdbg: bool = False 
    speedup: bool = False

class Events:

    # Returns value to running method of Window class
    def check_events(event:pygame.event, event_type: int, events_struct: Event_Types) -> bool:
        
        # QUIT
        if event_type == pygame.QUIT:
            events_struct.event_running = not events_struct.event_running

        elif event_type == pygame.KEYDOWN:

            # PAUSE
            if event.key == pygame.K_ESCAPE:
                events_struct.event_pause = not events_struct.event_pause

            # Debug On
            if event.key == pygame.K_p:
                events_struct.showdbg = not events_struct.showdbg

            # Speedup On
            if event.key == pygame.K_s:
                events_struct.speedup = not events_struct.speedup
            
        return events_struct