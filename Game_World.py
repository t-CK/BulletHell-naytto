from Player import Player

# Kartan koko
MAP_WIDTH = 5000
MAP_HEIGHT = 5000

class Map:
    # Kameran X ja Y sijainti
    _camera_x :int
    _camera_y :int
    # Referenssi pelaajaan
    _p1 :Player
    
    def __init__(self, player :Player) -> None:
        # Tallennetaan referenssi pelaaja objektiin
        self._p1 = player
        # Asetetaan kameran sijainti vastaamaan pelaajan sijaintia kartalla
        self._camera_x = self._p1.get_x()
        self._camera_y = self._p1.get_y()
       
    
    def Update(self) -> tuple:
        """Päivittää kameran sijainnin vastaamaan pelaajan sijaintia kartalla ja palauttaa sijainnin tuplena"""
        # Päivitetään kameran sijainti vastaamaan pelaajan sijaintia
        self._camera_x = self._p1.get_x()
        self._camera_y = self._p1.get_y()
        # Palautetaan kameran sijainti tuplena
        return (self._camera_x, self._camera_y)