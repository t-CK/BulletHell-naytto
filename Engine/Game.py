from Log import *
import Window
import array
import time
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
    _game_objects :list
    _delta_time = 0.0
    _wnd :Window.Window


    def __init__(self) -> None:
        self._wnd = Window.Window()
        self._state = Game_State(2)
        self._is_Running = True

#    def add_game_object(self, object :Game_Object) -> None:
#        """Lisää uuden peliobjektin peliin"""
#        # Tarkastetaan funktioon sy�tetyn parametrin tyyppi ja tyypin ollessa Game_Object lis�t��n se listaan
#        # Muussa tapauksessa tulostetaan vir�heilmoitus
#        if type(object) == GameObject:
#            self._game_objects.append(Game_Object())
#            return
#        Log_Error("Game.add_game_object() syötettiin vääränlainen parametri")

    def game_loop(self):
        # Ajanoton k�ynnistys
        while self._is_Running:
            # Loopataan peliobjektien lista ja päivitetään objektit + komponentit
            for instance in self._game_objects:
                instance.update_components()
                instance.update(self._delta_time)
            # Ikkunan sisällön päivittäminen

        # Ajanoton pys�ytys ja _delta_time -muuttujan p�ivitys 

    def get_delta_time(self) -> float:
        return self._delta_time
    

if __name__ == "__main__":
    game=Game()
    game.game_loop()