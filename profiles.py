from Player import Player
from Game import Game
from Counter import Counter
import sqlite3

class Profiles:
    def __init__(self) -> None:
        pass
    
    def save_game(self, xp :int, lvl :int, k_count :int, t_count :float):
        pass
    
    def load_game(self, profile_num :int) -> tuple:
        """Lataa valitun profiilin tiedot tietokannasta\n
        Palauttaa tiedot tuplena"""
        pass
    
    def level_up(self):
        pass