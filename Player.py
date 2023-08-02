import sys, math, random, pygame as pg
from pygame.locals import *
import Game_World
from Log import *
from variables import *

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
    def __init__(self, wnd_size :tuple, hp = 20):
        super().__init__()
        try:
            self.surf = pg.image.load("player.png").convert()
            self.surf.set_colorkey((0,255,0))
        except FileNotFoundError:
            Log_Warning("Cannot load image into Player")
            self.surf = pg.Surface([15, 20])
            self.surf.fill((255,255,255))
        if not SPRITE_SCALE == 1:
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
        
        self._window_size = wnd_size
        
        # Asetetaan pelaajan X ja Y sijainnit kartalla
        # Pelaaja asetetaan aloittamaan keskeltä pelialuetta
        self._map_x = Game_World.MAP_WIDTH / 2
        self._map_y = Game_World.MAP_HEIGHT / 2
        
        self.rect.center = [self._window_size[0] / 2, self._window_size[1] / 2]

        all_sprites.add(self)

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
        self._map_x += value
        self.rect.center = [Game_World.MAP_WIDTH / 2, Game_World.MAP_HEIGHT / 2]
    
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
        self._map_y += value
        self.rect.center = [Game_World.MAP_WIDTH / 2, Game_World.MAP_HEIGHT / 2]

    def update(self):
        """ Decreases i-frames, also checks for movement input for now. """
        if self.invulnerable > 0:
            self.invulnerable -= 1
        # Keyboard input for player movement with arrows & WASD
        if not mouse_movement_enabled:
            pass
#            keys = pg.key.get_pressed()
#            if keys[K_UP] or keys[K_w]:
#                self.rect.move_ip(0, -self.speed)
#                while pg.sprite.spritecollideany(self, collideable):
#                    self.rect.move_ip(0, 1)
#            if keys[K_RIGHT] or keys[K_d]:
#                self.rect.move_ip(self.speed, 0)
#                while pg.sprite.spritecollideany(self, collideable):
#                    self.rect.move_ip(-1, 0)
#            if keys[K_DOWN] or keys[K_s]:
#                self.rect.move_ip(0, self.speed)
#                while pg.sprite.spritecollideany(self, collideable):
#                    self.rect.move_ip(0, -1)
#            if keys[K_LEFT] or keys[K_a]:
#                self.rect.move_ip(-self.speed, 0)
#                while pg.sprite.spritecollideany(self, collideable):
#                    self.rect.move_ip(1, 0)

        # Mouse movement testing
        else:
            MIN_MOUSE_DISTANCE = 30
            mouse_x, mouse_y = pg.mouse.get_pos()
            distance_from_player = get_distance((mouse_x, mouse_y), self.rect.center)
            speed_multiplier = min(1, (distance_from_player - MIN_MOUSE_DISTANCE)/WIDTH*3.5)

            if distance_from_player > MIN_MOUSE_DISTANCE:
                if 3*abs(mouse_x - player.rect.center[0])/WIDTH > abs(mouse_y - player.rect.center[1])/HEIGHT:
                    if mouse_x > player.rect.center[0]:
                        self.rect.move_ip(self.speed * speed_multiplier, 0)
                        while pg.sprite.spritecollideany(self, collideable):
                            self.rect.move_ip(-1, 0)
                    else:
                        self.rect.move_ip(-self.speed * speed_multiplier, 0)
                        while pg.sprite.spritecollideany(self, collideable):
                            self.rect.move_ip(1, 0)
                if abs(mouse_x - player.rect.center[0])/WIDTH < 2*abs(mouse_y - player.rect.center[1])/HEIGHT:
                    if mouse_y > player.rect.center[1]:
                        self.rect.move_ip(0, self.speed * speed_multiplier)
                        while pg.sprite.spritecollideany(self, collideable):
                            self.rect.move_ip(0, -1)
                    else:
                        self.rect.move_ip(0, -self.speed * speed_multiplier)
                        while pg.sprite.spritecollideany(self, collideable):
                            self.rect.move_ip(0, 1)

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
                player_death()
                
    def levelup(self):
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level *= 1.5
        self.lvl += 1
        
    def get_x(self):
        return self._map_x
    
    def get_y(self):
        return self._map_y
