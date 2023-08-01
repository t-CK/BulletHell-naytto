from pygame import sprite, Surface, display
import Player

class Ui(sprite.Sprite):
    """ UI parent class (pretty unnecessary at the moment) """
    def __init__(self, game):
        super().__init__()
        
        self._wnd_size = game._wnd._wnd.get_size() # Tallennetaan ikkunan kokotiedot luokan muuttujiin
        
        self.surf = Surface((Game._wnd._wnd.get_size()))
        self.surf.fill((0, 255, 0))
        self.surf.set_colorkey((0, 255, 0))

        game.add_ui(self) # Lisätään ui-elementti Game -luokan spriteihin

class Ui_Bar(Ui):
    """ XP / Health bar on top of screen 
    
    Variables value and value_max are methods, that are called to get the
    current and maximum values for the bar's length
    """
    def __init__(self, game, value = None, value_max = None):
        super().__init__()        
        self.bar_height = self._wnd_size[1]//100
        self.bar_max_width = self.wnd_size[0]//2
        self.surf = Surface.Surface((self.bar_max_width, self.bar_height))
        self.rect = self.surf.get_rect()
        self.surf.fill((0, 255, 0))
        self.surf.set_colorkey((0, 255, 0))
        self.color = (0, 0, 0)
        self.value = value
        self.value_max = value_max
                
    def update(self):
        if not self.value_max:
            bar_width = 0
        else:
            bar_width = self.value()/self.value_max() * self.bar_max_width
        
        display.draw.rect(self.surf, (0, 0, 0), (0, 0, self.bar_max_width, self.bar_height), 0, self._wnd_size[1]//300)
        display.draw.rect(self.surf, self.color, (0, 0, bar_width, self.bar_height), 0, self._wnd_size[1]//300)

class Ui_Bar_XP(Ui_Bar):
    """ XP Bar on top of screen, purplish """
    def __init__(self, player):
        super().__init__(player.get_xp, player.get_xp_to_next_level)
        self._player = player
        self.rect.topleft = (self._wnd_size[0]//4, self._wnd_size[1]//19 + 7)
        self.color = (150, 50, 255)

class Ui_Bar_Health(Ui_Bar):
    """ Health Bar on top of screen, red """
    def __init__(self):
        super().__init__(self._player.get_hp, self._player.get_hp_max)
        self.rect.topleft = (self._wnd_size[0]//4, self._wnd_size[1]//19 - 7)
        self.color = (255, 0, 0)