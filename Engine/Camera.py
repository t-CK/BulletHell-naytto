from pygame import Camera

# Peliin tarvitaan vain yksi kamera, joten kamera -luokka on staattinen
class Camera(Camera):
    # Kameran x ja y sijainti, päivitetään pelaajan sijainnin perusteella
    _pos_x, pos_y :int
    # Seurattava pelaaja -objekti
    _player
    
    def __init__(self):
        pass
    