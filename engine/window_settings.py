from dataclasses import dataclass
from dataclasses import asdict

# Fancy struct instance 
@dataclass
class WindowSettings(object):

    screen_width: int # the width of the window
    screen_height: int # the height of the window
    
    screen_fps: int = 60 # frames per second

    fullscreen: bool = False # toggle fullscreen

    # retrieve dictionary with all variables
    def get_as_dict(self) -> None:
        return asdict(self)
    
    # update all the variables from a dictionary
    def update_from_dict(self, new_settings: dict) -> None:
        for key in new_settings:
            setattr(WindowSettings, key, new_settings[key])

    # change a single variable from the struct
    def change_var(self, name: str, value: any) -> None:
        setattr(WindowSettings, name, value)
