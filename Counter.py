import time

class Counter:
    _kill_count :int
    _timer :float
    
    def __init__(self, kill = 0, timer = 0.0):
        self._kill_count = kill
        self._timer
        
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