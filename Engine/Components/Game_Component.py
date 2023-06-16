from Game_Component import Game_Component
from ..Log import *
from .. import Window
from pygame import image, locals, key, event
from pygame import surface, display

# Abstrakti luokka, josta periytetään muut pelikomponenttiluokat
class Game_Component:
    def __init__(self) -> None:
        pass
    
class Sprite_Component(Game_Component):
    """Sprite component renderöitävien kuvien/Spritejen käsittelyyn peliobjektissa"""
    _wnd :surface
    
    def __init__(self, wnd :Window.Window):
        self._imgs = []
        self._wnd = wnd._wnd

    def add_sprites(self, *imgs) -> None:
        """Lataa kuvatiedostot ja tallentaa listaan renderöintiä varten\n
        Ottaa parametrina kuvatiedoston tai -tiedostojen osoitteet/nimet"""
        try:
            for i in imgs:
                self._imgs.append(image.load(filename=i).convert())
        except Exception as e:
            Log_Error(f"Failed to load img into pygame: {e}")

    def render_sprite(self, index):
        """Renderöi kuvan, ottaa argumenttina renderöitävän kuvan indeksipaikan"""
        self._wnd.blit(self._imgs[index])
        
class Input_Component(Game_Component):
    _wnd :display # pygame.display, josta tarkastellaan inputtia
    def __init__(self, owner):
        key.set_repeat(0, 0)
        self._wnd = Window.Window._wnd
        # Tallennetaan Game_Object, johon komponentti kuuluu, jotta voidaan kutsua oikean objektin metodia
        self._owner = owner 
    
    def get_input() -> str:
        # Tarkastetaan input ja bindataan input event oikeaan funktioon
        for e in event.get():
            if e.type == locals.KEYDOWN:
                if e.key == locals.K_UP:
                    Log_Info("K_UP")
                if e.key == locals.K_DOWN:
                    Log_Info("K_DOWN")
                if e.key == locals.K_RIGHT:
                    Log_Info("K_RIGHT")
                if e.key == locals.K_LEFT:
                    Log_Info("K_LEFT")