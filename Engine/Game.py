import Log
from pygame import event
from pygame import key
from pygame import time
from pygame import locals
from enum import Enum


# Enum luokka pelin statuksen seuraamista varten
class Game_State(Enum):
    RUNNING = 0
    PAUSED = 1
    IN_MENU = 2

class Game:
    # Ainoastaan yksi instanssi pelist� sallitaan kerrallaan, joten Game -luokka voi olla staattinen (Luokan muuttujat tallennetaan suoraan class-variableina)
    _is_Running :bool
    _state :Game_State
    _game_objects = []
#    _wnd :Window.Window
    # delta time
    _prev_tick = 0
    _delta_time = 0.0


    def __init__(self) -> None:
#        self._wnd = Window.Window()
        self._state = Game_State(2)
        self._is_Running = True


    def game_loop(self):
        while self._is_Running:
            # Jos game_state on PAUSE, asetetaan prev_tick arvoksi 0, tarkastetaan onko escape näppäintä painettu pausen lopettamiseksi
            # ja hypätään loopin alkuun
            if self._state == Game_State.PAUSED:
                self._prev_tick = 0.0
                if event.peek():
                    keys = key.get_pressed()
                    e = event.poll()
                    if keys[locals.K_ESCAPE]:
                        self._state = 0
                Log.Log_Info("PAUSED")
                continue
            if event.peek():
                e = event.poll()
                keys = key.get_pressed()
                if keys[locals.K_ESCAPE]:
                    self._state = Game_State.PAUSED
            Log.Log_Info(self._delta_time)
            # Lasketaan delta time ja tallennetaan pygame.get_ticks() palauttama arvo prev_tick muuttujaan
            if self._prev_tick == 0.0:
                self._prev_tick = time.get_ticks()
            else:
                self._delta_time = (time.get_ticks() - self._prev_tick) / 1000
            # Tyhjennetään ikkunan sisältö ja renderöidään taustaväri
#            self._wnd.draw_background()
            # Loopataan peliobjektien lista ja päivitetään objektit + komponentit
            for instance in self._game_objects:
                print(self._delta_time)
                # Päivitetään peliobjektit (peliobjekti päivittää komponenttinsa ja renderöi spritet)
#                instance.update(delta_time=self._delta_time)
            self.wnd.fill((1, 0, 1))
            display.flip()
            


    def get_delta_time(self) -> float:
        return self._delta_time
    

if __name__ == "__main__":
    game=Game()
    game.game_loop()