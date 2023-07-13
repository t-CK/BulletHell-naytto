from pygame import key, event, locals
from input_main import *

class Input:
    _p1 :Player
    
    def __init__(self, player :Player, game :Game) -> None:
        self._p1 = player
        self._game = game
    
    def get_input(self):
        if event.peek():
            e = event.poll()
            keys = key.get_pressed()
            if keys[locals.K_ESCAPE]:
                self._game.is_running = False
            if keys[locals.K_RIGHT]:
                self._p1.move_right(1)
                self._game.update_game(-1, 0)
            elif keys[locals.K_LEFT]:
                self._p1.move_right(-1)
                self._game.update_game(1, 0)
            if keys[locals.K_DOWN]:
                self._p1.move_down(1)
                self._game.update_game(0, -1)
            elif keys[locals.K_UP]:
                self._p1.move_down(-1)
                self._game.update_game(0, 1)