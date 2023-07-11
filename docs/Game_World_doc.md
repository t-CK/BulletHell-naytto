Map (class):
    _camera_x   Kameran sijainti horisontaalisesti
    _camera_y   Kameran sijainti Pystysuunnassa
    _p1         Referenssi pelaajaobjektiin
    
    __init__:
        Initialisoi kartan. Ottaa parametrina Player -pelaajaobjektin.
        Tallentaa pelaajaobjektin _p1 -muuttujaan ja asettaa _camera_x ja _camera_y -muuttujien arvot vastaamaan pelaajan x ja y sijainteja kartalla
        
    Update:
        Päivittää kartan kutsuttaessa. Asettaa _camera_x ja _camera_y arvot vastaamaan pelaajan sijaintitietoja.
        Palauttaa kameran x ja y -arvot tuplena.