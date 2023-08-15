import pygame as pg
import misc
from image_generator.imagegen import get_sprite_by_names
from pygame.locals import *
from variables import *

import Game_World

class Player(pg.sprite.Sprite):
    """ Player sprite object with various attributes

    Variables: (in addition to pygame's Sprite stuff)
        hp, hp_max, speed, lvl, xp: Self-explanatory
        xp_to_next_level: XP points needed for next level. XP resets on leveling.
        invulnerable: Ticks of invulnerability (i-frames)
        pickup_distance: Distance from which XP and pickups are picked up

    Methods:
        update(): Pygame's Sprite-update. Decreases i-frames, also checks for movement input for now.
        get_hp(), get_hp_max(), get_xp(), get_xp_to_next_level(): Getters for variables
        damage(amount = 1): Decreases player's HP by [amount] and sets i-frames.
        levelup(): Trigger leveling up; increases [xp_to_next_level] and resets [xp].
            (levelup() is, at least for now, called by Xp.pickup() and not Player)
    """
    def __init__(self, wnd_size, hp = 20):
        super().__init__()
        try:
            self.surf = pg.image.load("./image_generator/sprite.png").convert()
        except:
            try:
                self.surf = pg.image.load("./images/player.png").convert()
            except FileNotFoundError:
                self.surf = pg.Surface([30, 40])
                self.surf.fill((255,255,255))
        # self.surf, self.animation = get_sprite_by_names("skull", "rogue", "skeleton")
        self.surf.set_colorkey((0,255,0))
        if not (SPRITE_SCALE == 1 or SPRITE_SCALE == 0):
            self.surf = pg.transform.scale_by(self.surf, SPRITE_SCALE)
        self.rect = self.surf.get_rect()
        self.hp = hp
        self.hp_max = hp
        self.speed = DEFAULT_SPEED
        self.lvl = 1
        self.xp = 0
        self.xp_to_next_level = 100
        self.invulnerable = 0
        self.pickup_distance = DEFAULT_PICKUP_DISTANCE * SPRITE_SCALE
        self.mouse_movement_enabled = False

        self._window_size = wnd_size

        # Asetetaan pelaajan X ja Y sijainnit kartalla
        # Pelaaja asetetaan aloittamaan keskeltä pelialuetta
        self._map_x = Game_World.MAP_WIDTH / 2
        self._map_y = Game_World.MAP_HEIGHT / 2
        self.rect.center = [self._window_size[0] / 2, self._window_size[1] / 2]

    def update(self):
        """ Decreases i-frames, also checks for movement input for now. """
        if self.invulnerable > 0:
            self.invulnerable -= 1

    def move_x(self, value):
        if value > 0:
            self.rect.move_ip(-self.speed * value, 0)
            while pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(1, 0)

        else:
            self.rect.move_ip(self.speed * value, 0)
            while pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(-1, 0)
        # Päivitetään pelaajan sijainti kartalla
        self._map_x += value * self.speed
        self.rect.center = [self._window_size[0] / 2, self._window_size[1] / 2]

    def move_y(self, value):
        if value < 0:
            self.rect.move_ip(0, -self.speed * value)
            while pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(0, 1)
        else:
            self.rect.move_ip(0, self.speed * value)
            while pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(0, -1)
        # Päivitetään pelaajan sijainti kartalla
        self._map_y += value * self.speed
        self.rect.center = [self._window_size[0] / 2, self._window_size[1] / 2]

    def get_x(self):
        return self._map_x

    def get_y(self):
        return self._map_y

    def get_hp(self):
        return self.hp

    def get_hp_max(self):
        return self.hp_max

    def get_xp(self):
        return self.xp

    def get_xp_to_next_level(self):
        return self.xp_to_next_level

    def damage(self, amount = 1):
        """ Decrease HP and set i-frames. """
        if not self.invulnerable:
            self.hp -= amount
            self.invulnerable = 10

            if self.hp <= 0:
                self.player_death()

    def levelup(self):
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level *= 1.5
        self.lvl += 1

    def player_death(self):
        """ Very much temporary, just playing around for now """
        self.surf = pg.transform.rotate(self.surf, 90)
        for sprite in bullet_group:
            sprite.kill()
        self.update = lambda *_: None

    def move_player(self, x, y):
        """ Move every non-player (and non-ui) sprite (-x,-y) pixels """
        for sprite in all_sprites:
            sprite.rect.move_ip(-x,-y)
            # if hasattr(sprite, "target") and type(sprite.target) is tuple:
                # sprite.target = (sprite.target[0]-x, sprite.target[1]-y)