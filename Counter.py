import time

class Counter:
    _kill_count :int
    _timer_start :float
    
    def __init__(self, kill = 0, timer = 0.0):
        self._kill_count = kill
        if time > 0:
            self._timer_start = timer
        # Luodaan ajastin -objekti laskemaan kulunutta peliaikaa
        else: self._timer_start = time.time()
        
    def kill_update(self):
        """Kasvattaa kill counteria yhdellä\n
        Kutsutaan aina tapon yhteydessä"""
        self._kill_count +=1
    
    def timer_update(self):
        pass
    
    def get_kill_count(self):
        return self._kill_count
    
    def get_timer(self):
        """Palauttaa pelin alusta kuluneen ajan sekunneissa"""
        now = time.time()
        return time.time() - self._timer_start