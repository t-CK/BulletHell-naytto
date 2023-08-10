import pygame as pg
import random, math
import pickups, misc
from variables import *

class Enemy(pg.sprite.Sprite):
    """ Rudimentary enemy sprite object (probably gonna move much of this to a child class)

    Variables: (in addition to pygame's Sprite stuff)
        hp, speed: Self-explanatory
        dmg: Damage the enemy deals when bumping into player
        solid: If False, can pass through world obstacles
        invulnerable: Ticks of invulnerability (i-frames)

    Methods:
        update(): Pygame's Sprite-update. Decrease i-frames and move towards player. (+ collision)
        damage(): Decrease HP (if not invulnerable) and set i-frames. Call death() if needed.
        death(): Drop XP and kill sprite.
    """
    def __init__(self, game, position = (0,0), hp = 3, speed = 1, dmg = 1, solid = True):
        super().__init__()
        self.game = game
        try:
            self.player = game.player
        except AttributeError:
            self.player = game._player
        try:
            self.surf = pg.image.load("./images/enemy.png").convert()
            self.surf.set_colorkey((0,255,0))
            self.color = None
        except FileNotFoundError:
            self.surf = pg.Surface([12, 19])
            self.color = (60,255,60)
            self.surf.fill(self.color)
        if not (SPRITE_SCALE == 1 or SPRITE_SCALE == 0):
            self.surf = pg.transform.scale_by(self.surf, SPRITE_SCALE)

        self.rect = self.surf.get_rect()
        self.rect.center = position

        self.hp = hp
        self.speed = speed
        self.dmg = dmg
        self.solid = solid
        self.invulnerable = 0
        
        self._map_x, self._map_y = position

        all_sprites.add(self)
        enemy_group.add(self)
        if self.solid:
            collideable.add(self)

    def update(self):
        """ Decrease i-frames """
        if self.invulnerable > 0:
            self.invulnerable -= 1
            
    def get_x(self):
        return self._map_x
    
    def get_y(self):
        return self._map_y

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
        pickups.Xp(self.game, *self.rect.center, random.randrange(len(pickups.Xp._colors))+1)
        self.kill()
        
class Enemy_Follow(Enemy):
    """ Enemy moving in a straight line towards player """
    def __init__(self, game, position = (0,0), target: tuple or Sprite = None, hp = 3, speed = 1, dmg = 1, solid = True):
        super().__init__(game, position, hp, speed, dmg, solid)
        
        if target is None:
            self.target = game._player.rect.center
        elif type(target) is tuple:
            self.target = target
        else:
            self.target = target.rect.center
        
    def update(self):
        """ Move towards player. Move back until there's no collision (if corporeal). """
        super().update() # For i-frames
        collideable.remove(self)
        if self.target[0] > self.rect.center[0]:
            self.rect.move_ip(self.speed,0)
            while self.solid and pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(-1,0)
        elif self.target[0] < self.rect.center[0]:
            self.rect.move_ip(-self.speed,0)
            while self.solid and pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(1,0)
        if self.target[1] > self.rect.center[1]:
            self.rect.move_ip(0,self.speed)
            while self.solid and pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(0,-1)
        elif self.target[1] < self.rect.center[1]:
            self.rect.move_ip(0,-self.speed)
            while self.solid and pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(0,1)
        if self.solid:
            collideable.add(self)
    
class Enemy_Sine(Enemy_Follow):
    """ Enemy_Follow but with some added circling """
    def __init__(self, game, position = (0,0), target = None, hp = 3, speed = 1, dmg = 1, solid = False):
        super().__init__(game, position, target, hp, speed, dmg, solid)
        
    def update(self):
        super().update() # For i-frames and movement towards player
        
        # First (bad) attempt at moving in a wave while closing in
        step = misc.get_step_toward(self.rect.center, self.player.rect.center, self.speed)
        self.offset = (-step[1] * 10*math.sin(self.game.ticks/10), step[0] * 10*math.sin(self.game.ticks/10))
        self.rect.move_ip(self.offset)