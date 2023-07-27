

class Counter:
    _kill_count :int
    _timer :float
    
    def __init__(self, kill = 0, time = 0.0):
        self._kill_count = kill
        self._timer = time
        
    def kill_update(self):
        """Kasvattaa kill counteria yhdellä\n
        Kutsutaan aina tapon yhteydessä"""
        self._kill_count +=1
    
    def get_kill_count(self):
        return self._kill_count