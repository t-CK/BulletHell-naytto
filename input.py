from pygame import event
from pygame import key
from pygame import locals
import player
import Game
from Log import *
from sys import exit
from enum import Enum

class Input:
    _p1 :player.Player # Referenssi pelaajaobjektiin
    _game :Game.Game # Referenssi peliin
    
    def __init__(self, game :Game.Game, player :player.Player) -> None:
        self._p1 = player
        self._game = game
        key.set_repeat(10, 0)
    
    def get_input(self):
        # Tarkastetaan, onko eventtejä käsiteltävänä
        if event.peek():
            e = event.poll()
            keys = key.get_pressed()
            # Tarkastetaan onko ikkuna suljettu
            if e.type == locals.QUIT:
                exit()
            # Vaihdetaan Game_State PAUSED ja RUNNING välillä painettaessa esc -näppäintä
            if keys[locals.K_ESCAPE]:
                self._game.toggle_state(Game.Game_State.PAUSED)
                #if self._game.get_state() == Game.Game_State.RUNNING:
                #    self._game._state = Game.Game_State.PAUSED
                #elif self._game.get_state() == Game.Game_State.PAUSED:
                #    self._game._state = Game.Game_State.RUNNING
            # Pelaajan liikutus
            if keys[locals.K_UP]:
                Log_Info(f"Player move Y : {-1}")
                self._p1.move_y(-1)
                self._game.update_game(0, 1)
            elif keys[locals.K_DOWN]:
                Log_Info(f"Player move Y : {1}")
                self._p1.move_y(1)
                self._game.update_game(0, -1)
            if keys[locals.K_RIGHT]:
                Log_Info(f"Player move X : {1}")
                self._p1.move_x(1)
                self._game.update_game(-1, 0)
            elif keys[locals.K_LEFT]:
                Log_Info(f"Player move X : {-1}")
                self._p1.move_x(-1)
                self._game.update_game(1, 0)