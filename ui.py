import pygame as pg
import __main__
from variables import *

# player = __main__.player

class Ui(pg.sprite.Sprite):
    """ UI parent class (pretty unnecessary at the moment) """
    def __init__(self):
        super().__init__()
        self.surf = pg.Surface((SCREEN_SIZE))
        self.surf.fill((0, 255, 0))
        self.surf.set_colorkey((0, 255, 0))

        all_sprites.add(self)
        ui_group.add(self)

class Ui_Bar(Ui):
    """ XP / Health bar on top of screen

    Variables value and value_max are methods, that are called to get the
    current and maximum values for the bar's length
    """
    def __init__(self, value = None, value_max = None):
        super().__init__()
        self.bar_height = HEIGHT//100
        self.bar_max_width = WIDTH//2
        self.surf = pg.Surface((self.bar_max_width, self.bar_height))
        self.rect = self.surf.get_rect()
        self.surf.fill((0, 255, 0))
        self.surf.set_colorkey((0, 255, 0))
        self.color = (0, 0, 0)
        self.value = value
        self.value_max = value_max

    def update(self):
        """ Draws value()/value_max() percent of self.color on the Surface """
        if not self.value_max:
            bar_width = 0
        else:
            bar_width = self.value()/self.value_max() * self.bar_max_width

        pg.draw.rect(self.surf, (0, 0, 0), (0, 0, self.bar_max_width, self.bar_height), 0, HEIGHT//300)
        pg.draw.rect(self.surf, self.color, (1, 1, bar_width-1, self.bar_height-1), 0, HEIGHT//300)

class Ui_Bar_XP(Ui_Bar):
    """ XP Bar on top of screen, purplish """
    def __init__(self, player):
        super().__init__(player.get_xp, player.get_xp_to_next_level)
        self.rect.topleft = (WIDTH//4, HEIGHT//19 + 7)
        self.color = (150, 50, 255)

class Ui_Bar_Health(Ui_Bar):
    """ Health Bar on top of screen, red """
    def __init__(self, player):
        super().__init__(player.get_hp, player.get_hp_max)
        self.rect.topleft = (WIDTH//4, HEIGHT//19 - 7)
        self.color = (255, 0, 0)