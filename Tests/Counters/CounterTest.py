import time
from random import randint
from pygame import surface, font, display, time

class Counter:
    _kill_count :int
    _timer :float
    
    def __init__(self, wnd :surface.Surface, kill = 0, timer = 0.0):
        self._kill_count = kill
        self._timer = timer
        font.init()
        self._font = font.SysFont(name=None, size=20)
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
        render_surf = font.Font.render(, text=f"KILLS: {self._kill_count}\nTIME: {self._timer}", color=(255, 10, 25, 1), background=None)
        self._wnd._wnd.blit(render_surf, (20, 50))
        display.flip() # DEBUG

    def draw_background(self):
        self._wnd.fill(color=(50,255,20))

display.init()
wnd = display.set_mode((0, 0))
counter_obj = Counter(wnd)
delta_time = 0.0
prev_tick = 0
while True:
    counter_obj.timer_update(delta_time) # Update time count
    if randint(0, 1):
        counter_obj.kill_update() # Update kill count

    counter_obj.draw_background() # Clear screen with color
    counter_obj.render_counters() # Render counters

    delta_time = time.get_ticks() - prev_tick / 1000 # Update delta time
    prev_tick = time.get_ticks() # Update prev_tick