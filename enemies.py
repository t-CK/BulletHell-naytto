import pygame as pg
import random
import pickup
from variables import *

class Enemy(pg.sprite.Sprite):
    """ Rudimentary enemy sprite object (probably gonna move much of this to a child class)

    Variables: (in addition to pygame's Sprite stuff)
        hp, speed: Self-explanatory
        dmg: Damage the enemy deals when bumping into player
        invulnerable: Ticks of invulnerability (i-frames)

    Methods:
        update(): Pygame's Sprite-update. Decrease i-frames and move towards player. (+ collision)
        damage(): Decrease HP (if not invulnerable) and set i-frames. Call death() if needed.
        death(): Drop XP and kill sprite. No death animations, at least not yet.
    """
    def __init__(self, game, position = (0,0), hp = 3, speed = 1, dmg = 1):
        super().__init__()
        self.game = game
        self.player = game.player
        try:
            self.surf = pg.image.load("enemy.png").convert()
            self.surf.set_colorkey((0,255,0))
            self.color = None
        except FileNotFoundError:
            self.surf = pg.Surface([12, 19])
            self.color = (60,255,60)
            self.surf.fill(self.color)
        if not SPRITE_SCALE == 1 or SPRITE_SCALE == 0:
            self.surf = pg.transform.scale_by(self.surf, SPRITE_SCALE)

        self.rect = self.surf.get_rect()
        self.rect.center = position

        self.hp = hp
        self.speed = speed
        self.dmg = dmg
        self.invulnerable = 0

        all_sprites.add(self)
        collideable.add(self)
        enemy_group.add(self)

    def update(self):
        """ Decrease i-frames and move towards player. Move back until there's no collision. """
        if self.invulnerable > 0:
            self.invulnerable -= 1

        collideable.remove(self)
        if self.player.rect.center[0] > self.rect.center[0]:
            self.rect.move_ip(self.speed,0)
            while pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(-1,0)
        elif self.player.rect.center[0] < self.rect.center[0]:
            self.rect.move_ip(-self.speed,0)
            while pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(1,0)
        if self.player.rect.center[1] > self.rect.center[1]:
            self.rect.move_ip(0,self.speed)
            while pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(0,-1)
        elif self.player.rect.center[1] < self.rect.center[1]:
            self.rect.move_ip(0,-self.speed)
            while pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(0,1)
        collideable.add(self)

    def damage(self, amount = 1):
        """ Decrease HP (and Surface size) and set i-frames. """
        if self.invulnerable:
            return
        self.hp -= amount

        self.surf = pg.transform.scale_by(self.surf, 0.8)
        if self.color:  # If sprite's image is not loaded
            temp_color_r, temp_color_g, temp_color_b = self.color
            temp_color_g = max(temp_color_g-100, 0)
            temp_color_b = min(temp_color_b+100, 255)
            self.color = temp_color_r, temp_color_g, temp_color_b
            self.surf.fill(self.color)
        temp_center = self.rect.center
        self.rect = self.surf.get_rect()
        self.rect.center = temp_center

        self.invulnerable = 5
        if self.hp <= 0:
            self.death()

    def death(self):
        """ Drop XP and die """
        pickup.Xp(self.game, *self.rect.center, random.randrange(len(pickup.Xp._colors))+1)
        self.kill()