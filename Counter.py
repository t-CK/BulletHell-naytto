from pygame import display, surface, font

class Counter:
    _kill_count :int
    _timer :float
    
    def __init__(self, wnd :surface.Surface, kill = 0, timer = 0.0):
        """Counter luokan initialisointi.\n
        Parametrit:
        1. referenssi pygame -ikkunaan
        2. tappojen määrä (ladattaessa peli tallennuksesta), oletusarvona 0
        3. aikalaskuri (ladattaessa peli tallennuksesta), oletusarvona 0.0"""
        self._kill_count = kill
        self._timer = timer # Peliaika millisekunteina
        self._wnd = wnd
        
        font.init()
        self._font = font.SysFont(None, 50, True)
        
    def kill_update(self):
        """Kasvattaa kill counteria yhdellä\n
        Kutsutaan aina tapon yhteydessä"""
        self._kill_count +=1
        
    def timer_update(self, delta_time :float):
        self._timer += delta_time
    
    def get_kill_count(self):
        return self._kill_count
    
    def get_timer(self):
        """Palauttaa pelin alusta kuluneen ajan sekuntteina"""
        return self._timer
    
    def render_counter_ui(self):
        """Renderöi counter UI:t"""
        # Luodaan muuttujat minuuteille ja sekunneille
        minutes = 0
        seconds = int(self._timer) # Annetaan sekunttimuuttujalle arvoksi timer int muodossa (timer käyttää millisekunteja, joten timer muunnettuna kokonaisluvuksi vastaa sekunteja)
        # Jos sekuntteja on yli 60, aikaa on kulunut yli minuutti
        if seconds >= 60:
            # Asetetaan minuuteille arvoksi sekuntit jaettuna 60 ja muunnetaan se kokonaisluvuksi
            minutes = int(seconds/60) 
            # Asetetaan sekunttien arvoksi sekunttien jakojäännös 60
            seconds %= 60
        
        # Asetetaan minutit olemaan aina 2 numeron luku laskurin selkeyttämiseksi
        if minutes < 10: minutes = "0" + str(minutes)
        if seconds < 10: seconds = str(0) + str(seconds)
        
        
        # Renderöidään timer
        timer_txt = self._font.render(f"Time: {minutes}:{seconds}", False, (50, 50, 0)) # Luodaan pygame surface, johon on tallennettu sekuntti ja minuutti muuttujat tekstimuodossa
        self._wnd.blit(timer_txt, (20, 20)) # Blitataan timer teksti ikkunaan, eli renderöidään kuva kuvan päälle
        
        # Renderöidään kill count
        kill_txt = self._font.render(f"Kills: {self._kill_count}", False, (50, 50, 0))
        self._wnd.blit(kill_txt, (20, 50))
        