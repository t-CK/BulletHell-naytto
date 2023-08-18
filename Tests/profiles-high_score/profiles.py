import sqlite3
from multipledispatch import dispatch
from os.path import exists

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

class High_Score:
    _table = "score"
    _conn :sqlite3.Connection
    _cursor :sqlite3.Cursor
    
    def __init__(self):
        self._conn = sqlite3.connect("score.db")
        try:
            self._cursor = self._conn.cursor()
            self._cursor.execute(f"""CREATE TABLE IF NOT EXISTS '{self._table}'(
                pname TEXT PRIMARY KEY,
                score INTEGER,
                kills INTEGER,
                time REAL
                );""")
        except sqlite3.Error as e:
            (f"sqlite3 error : {e}\n__init__")
    
    def get_scores(self):
        """Hakee tietokannasta kaikki pelaajatiedot ja pisteet"""
        try:
            data = self._cursor.execute(f"SELECT * FROM {self._table}")
        except sqlite3.Error as e:
            print(f"sqlite error : {e}")
            data = None
        return data.fetchall()
        
    def get_score(self, pName :str) -> list:
        """Hakee tietokannasta halutun pelaajan pisteet ja tiedot\n
        Ottaa parametrina halutun pelaajan nimimerkin"""
        try:
            data = self._cursor.execute(f"SELECT * FROM {self._table} WHERE pname = '{pName}'")
        except sqlite3.Error as e:
            print(f"sqlite error : {e}")
            data = None
        return data.fetchone()
        
    
    def add_score(self, pName :str, score :int, kills :int, time :float) -> None:
        """Lisää pelaajan pisteet tietokantaan
        Parametrit:
        pelaaja : str
        pisteet : int
        tapot   : int
        aika    : float"""
        for name in  self._cursor.execute(f"""SELECT pname FROM {self._table}"""):
            if name[0] == pName:
                self.update_score(pName, score, kills, time)
                return
        self._cursor.execute(f"""INSERT INTO {self._table} (pname, score, kills, time)
                             VALUES ('{pName}', {score}, {kills}, {time});""")
        self._conn.commit()
        
    def update_score(self, pName :str, score :int, kills :int, time :float):
        """Päivittää halutun pelaajan tulokset tietokantaan
        Parametrit:
        pelaaja : str
        pisteet : int
        tapot   : int
        aika    : float"""
        self._cursor.execute(f"""UPDATE {self._table} SET score = {score}, kills = {kills}, time = {time}
                             WHERE pname = '{pName}'""")
        self._conn.commit()