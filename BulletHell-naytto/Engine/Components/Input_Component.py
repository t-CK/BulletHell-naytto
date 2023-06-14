from pygame import locals
from pygame import key
from pygame import event
import Game_Component
from pygame import display
from .. import Log

class Input_Component(Game_Component):
    _wnd :display # pygame.display, josta tarkastellaan inputtia
    def __init__(self):
        key.set_repeat(0, 0)
    
    def get_input() -> str:
        # Tarkastetaan input ja bindataan input event oikeaan funktioon
        for e in event.get():
            if e.type == locals.KEYDOWN:
                if e.key == locals.K_UP:
                    Log.Log_Info("K_UP")
                if e.key == locals.K_DOWN:
                    Log.Log_Info("K_DOWN")
                if e.key == locals.K_RIGHT:
                    Log.Log_Info("K_RIGHT")
                if e.key == locals.K_LEFT:
                    Log.Log_Info("K_LEFT")
                