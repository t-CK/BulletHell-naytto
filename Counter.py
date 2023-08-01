import time
from Window import Window
from pygame import surface, font

class Counter:
    _kill_count :int
    _timer :float
    
    def __init__(self, wnd :Window, kill = 0, timer = 0.0):
        self._kill_count = kill
        self._timer
        self._font = font.SysFont(size=20)
        self._wnd = wnd
        
    def kill_update(self):
        """Kasvattaa kill counteria yhdellä\n
        Kutsutaan aina tapon yhteydessä"""
        self._kill_count +=1
    
    def timer_update(self, delta_time :float):
        # Päivittää self._timer muuttujan
        # Ottaa parametrina delta_timen (float)
        self._timer += delta_time
    
    def get_kill_count(self):
        return self._kill_count
    
    def get_timer(self):
        """Palauttaa pelin alusta kuluneen ajan sekunneissa"""
        return self._timer
    
    def render_counters(self) -> None:
        """Render counters on screen"""

        # Render counters as text
        render_surf = font.Font.render(text=f"KILLS: {self._kill_count}\nTIME: {self._timer}", color=(255, 10, 25, 1), background=None)
        self._wnd._wnd.blit(render_surf, (20, 50))
