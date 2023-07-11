input:
    _p1         Referenssi pelaajaobjektiin
    _game       Referenssi peli -luokan objektiin
    
    __init__:
        Initialisoidaan input -objekti.
        Ottaa parametrina referenssin Game -objektiin ja referenssin pelaaja -objektiin.
        Tallentaa saadut parametrit self._p1 :Player ja self._game :Game -muuttujioin.
        
    get_input:
        Kuuntelee eventtejä ja eventin ollessa pygame.quit, sulkee ikkunan ja lopettaa pelin
        Kuuntelee näppäimistöä ja painettaessa esc -näppäintä, vaihtaa game._state:n Game_State.PAUSED ja Game_State.RUNNING välillä.
        Näppäimen ollessa UP, DOWN, LEFT tai RIGHT, kutsuu self._p1 objektin funktioita näppäimestä riippuen.