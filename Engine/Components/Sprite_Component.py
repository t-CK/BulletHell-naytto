from Game_Component import Game_Component
from ..Log import *
from .. import Window
from pygame import image
from pygame import surface, display


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