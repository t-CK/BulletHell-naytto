import sys
from pygame import display
from pygame import surface
from pygame import locals
from Log import *

# Peliin tarvitaan vain yksi ikkuna kerrallaan, joten Window luokka voi olla staattinen (luokan muuttujat takllennetaan class variableina)
class Window:
    _wnd :surface.Surface

    def __init__(self) -> None:
        display.init()
        # Tarkistetaan pygame.display initialisoinnin onnistuminen ja virheen sattuessa tulostetaan virheilmoitus
        # käyttämällä Log.Log_Fatal toimintoa ja lopetetaan ohjelma
        if not display.get_init():
            Log_Fatal("Failed to initialize pygame.display")
            sys.exit()
        # Jos pygame.display on initialisoitu onnistuneesti, tulostetaan debug ilmoitus konsoliin
        Log_Info("Initialized pygame.display")

        # Set window flags and create window object
        flags_ = locals.FULLSCREEN | locals.DOUBLEBUF | locals.HWACCEL | locals.OPENGL | locals.SHOWN
        self._wnd = display.set_mode((0, 0), flags=flags_, display=0, vsync=1)
    
    def draw_frame(self, *args):
        for entity in args:
            pass

        display.flip()

