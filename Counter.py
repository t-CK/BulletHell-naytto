import time
from pygame import display, surface

class Counter:
    _kill_count :int
    _timer_start :float
    
    def __init__(self, wnd :surface.Surface, kill = 0, timer = 0.0):
        """Counter luokan initialisointi.\n
        Parametrit:
        1. referenssi pygame -ikkunaan
        2. tappojen määrä (ladattaessa peli tallennuksesta), oletusarvona 0
        3. aikalaskuri (ladattaessa peli tallennuksesta), oletusarvona 0.0"""
        self._kill_count = kill
        if time > 0:
            self._timer_start = timer
        # Luodaan ajastin -objekti laskemaan kulunutta peliaikaa
        else: self._timer_start = time.time()
        self._wnd = wnd
        
    def kill_update(self):
        """Kasvattaa kill counteria yhdellä\n
        Kutsutaan aina tapon yhteydessä"""
        self._kill_count +=1
    
    def get_kill_count(self):
        return self._kill_count
    
    def get_timer(self):
        """Palauttaa pelin alusta kuluneen ajan sekuntteina"""
        now = time.time()
        return time.time() - self._timer_start
    
    def render_counter_ui(self):
        """Renderöi counter UI:t"""
        pass