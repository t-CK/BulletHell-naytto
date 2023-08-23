from pygame import display, surface

class Counter:
    _kill_count :int
    _timer :float
    
    def __init__(self, wnd :surface.Surface, kill = 0, timer = 0.0):
        """Counter luokan initialisointi.\n
        Parametrit:
        1. referenssi pygame -ikkunaan
        2. tappojen määrä (ladattaessa peli tallennuksesta), oletusarvona 0
        3. aikalaskuri (ladattaessa peli tallennuksesta), oletusarvona 0.0"""
        self._kill_count = kill
        self._timer = timer # Peliaika millisekunteina
        self._wnd = wnd
        
    def kill_update(self):
        """Kasvattaa kill counteria yhdellä\n
        Kutsutaan aina tapon yhteydessä"""
        self._kill_count +=1
        
    def timer_update(self, delta_time :float):
        self._timer += delta_time
    
    def get_kill_count(self):
        return self._kill_count
    
    def get_timer(self):
        """Palauttaa pelin alusta kuluneen ajan sekuntteina"""
        return self._timer
    
    def render_counter_ui(self):
        """Renderöi counter UI:t"""
        minutes = 0
        seconds = int(self._timer)
        if seconds >= 60:
            minutes = int(seconds/60)
            seconds %= 60
        print(f"MIN {minutes} : SEC {seconds}")