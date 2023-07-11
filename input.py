from pygame import event
from pygame import key
from pygame import locals
from project import Player
import Game
from sys import exit

class Input:
    _p1 :Player # Referenssi pelaajaobjektiin
    _game :Game.Game # Referenssi peliin
    
    def __init__(self, game :Game.Game, player :Player) -> None:
        self._p1 = player
        self._game = game
        key.set_repeat(10, 0)
    
    def get_input(self):
        if event.peek():
            e = event.poll()
            keys = key.get_pressed()
            if e.type == locals.QUIT:
                exit()
            # Vaihdetaan Game_State PAUSED ja RUNNING välillä painettaessa esc -näppäintä
            if keys[locals.K_ESCAPE]:
                if self._game._state == Game.Game_State.RUNNING:
                    self._game._state = Game.Game_State.PAUSED
                elif self._game._state == Game.Game_State.PAUSED:
                    self._game._state = Game.Game_State.RUNNING
            # Pelaajan liikutus
            if keys[locals.K_UP]:
                pass
            if keys[locals.K_DOWN]:
                pass
            if keys[locals.K_LEFT]:
                pass
            if keys[locals.K_RIGHT]:
                pass