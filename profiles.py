from Player import Player
from Game import Game
import sqlite3

class Profiles:
    _table = "profiles"
    _conn :sqlite3.Connection
    _cursor :sqlite3.Cursor
    
    def __init__(self):
        self._conn = sqlite3.connect("player_profiles.db")
        self._cursor = self._conn.cursor()
        self._cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self._table}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level INTEGER,
            xp INTEGER,
            kills INTEGER,
            time REAL,
            pname TEXT
            );""")
#        self._cursor.execute("CREATE TABLE profiles (ID INTEGER, level INTEGER, xp INTEGER, kills INTEGER, time REAL, pname TEXT)")
        print(self._conn.total_changes)
        
    def new_profile(self, pName :str) -> None:
        """Luo uuden pelaajaprofiilin tietokantaan.\n
        Ottaa parametrina pelaajan nimen\n
        Asettaa profiilin kentät nollaan ja levelin 1"""
        self._cursor.execute(f"""INSERT INTO {self._table} VALUES(NULL, 1, 0, 0, 0.0, '{pName}')""")
        self._conn.commit()
        
    def on_level_up(self) -> None:
        pass
    
    def get_content(self, id :int) -> list:
        """Hakee profiilin tiedot tietokannasta ja palauttaa tiedot listana\n
        Ottaa parametrinä pelaajan profiili-id:n"""
        pass
        
    def delete_profile(self, id) -> None:
        """Poistaa tietokannasta pelaajaprofiilin\n
        Ottaa parametrina poistettavan profiilin ID:n"""
        pass
