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
            # Pelaajan liikutus
            if keys[locals.K_UP]:
                self._p1.move_y(-1)
                self._game.update_map(0, 1)
            elif keys[locals.K_DOWN]:
                self._p1.move_y(1)
                self._game.update_map(0, -1)
            if keys[locals.K_RIGHT]:
                self._p1.move_x(1)
                self._game.update_map(-1, 0)
            elif keys[locals.K_LEFT]:
                self._p1.move_x(-1)
                self._game.update_map(1, 0)