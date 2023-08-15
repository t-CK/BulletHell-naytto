import pygame as pg
import misc, math
from variables import *

class Bullet(pg.sprite.Sprite):
    """ Parent class for bullets """
    def __init__(self):
        super().__init__()
        self.surf = pg.Surface([5,5])
        self.surf.fill((200,0,0))
        self.rect = self.surf.get_rect()

        all_sprites.add(self)
        bullet_group.add(self)

    def update(self):
        if self.ttl >= 0:
            self.ttl -= 1
            if self.ttl == 0:
                self.kill()

class Bullet_Line(Bullet):
    """ Bullet flying in a straight line

    Takes two points as tuples or Sprites, spawns at [origin] and follows a line going
    through [target]. Flies at [speed] pixels per tick for [ttl] (time to live) ticks.
    A ttl of <= 0 makes the bullet not despawn.

    NOTE: Will not register collision when passing through an enemy in a single tick.
    """
    def __init__(self, game, target: tuple or Sprite = None, origin: tuple or Sprite = None, ttl = 60, speed = 5):
        super().__init__()
        self.ttl = ttl
        self.speed = speed
        self.game = game
        if not origin: # Default to player
            self.origin = game.player.rect.center
        elif type(origin) is not tuple:
            self.origin = origin.rect.center
        self.rect.center = self.origin
        if target:
            if type(target) is tuple: # If target is a point
                self.target = target
            else: # If target is not a tuple, assume a Sprite
                self.target = target.rect.center
        else: # If target is None, try to default to closest enemy
            try:
                self.target = misc.get_closest_enemy(self.origin).rect.center
            except AttributeError:  # Raised if there are no enemies
                self.kill()
                return
        self.step = misc.get_step(self.origin, self.target, self.speed)

    def update(self):
        super().update()
        self.rect.move_ip(self.step)

class Bullet_Orbit(Bullet):
    """ Bullet object circling a constant point at (x,y) or a Sprite.

    Speed-attribute (inversely) affects time to do a complete circle, thus the velocity of
    the projectile depends on [radius] as well as [speed]. Despawns after [ttl] ticks (unless ttl <= 0).
    Offset is a tuple of (x,y,X,Y), where x/y scale and X/Y skew the circle, allowing for ellipses.
    """
    def __init__(self, game, center_object: tuple or Sprite = (0,0), radius = 100, speed = 30, ttl = -1, offset = (1,1,0,0)):
        super().__init__()
        self.radius = radius
        self.speed = speed
        self.game = game
        self.ttl = ttl
        self.x_scale = offset[0]
        self.y_scale = offset[1]
        self.x_offset = offset[2]
        self.y_offset = offset[3]
        # If first attribute is a tuple, set it as the center, otherwise two variables are used
        if type(center_object) == tuple:
            self.center = (self.centerx, self.centery) = center_object
            self.center_object = None
        else:
            self.center_object = center_object

    def update(self):
        """ If the center is not a tuple, update center point, then calculate position. """
        super().update()
        if self.center_object:
            self.center = (self.centerx, self.centery) = self.center_object.rect.center
        # Adding (r*sin(i), r*cos(i)) to (x,y) follows a circle of radius r as i -> inf.
        self.rect.center = (self.centerx + self.x_scale*self.radius*math.sin((self.x_offset+self.game.ticks)/self.speed),
                            self.centery + self.y_scale*self.radius*math.cos((self.y_offset+self.game.ticks)/self.speed))

class Bullet_Sine(Bullet_Line):
    """ Bullet_Line but wavy """
    def __init__(self, game, target: tuple or Sprite = None, origin: tuple or Sprite = None, ttl = 60, speed = 10,
                 wave_scale = 1):
        super().__init__(game, target, origin, ttl, speed)
        self.wave_scale = wave_scale

    def update(self):
        super().update()
        self.offset = [coordinate * self.wave_scale * math.sin(self.game.ticks/10) for coordinate in
                       (-self.step[1], self.step[0])]
        self.rect.move_ip(self.offset)

class Explosion(pg.sprite.Sprite):
    def __init__(self, game, target: tuple or Sprite = None, dmg = 3, diameter = 100):
        super().__init__()
        self.surf = pg.Surface([diameter, diameter//2])
        self.rect = self.surf.get_rect()
        self.game = game
        if target is None: # By default, target a random enemy
            try:
                self.rect.center = misc.get_random_enemy().rect.center
            except AttributeError:
                pass
        elif type(target) is not tuple: # If target is a Sprite
            self.rect.center = target.rect.center
        else: # Assume a tuple of coordinates
            self.rect.center = target
        self.dmg = dmg
        self.diameter = diameter

        self.update() # Exploding instantly might be temporary, but Sprite groups are not needed for now

    def update(self):
        for sprite in pg.sprite.spritecollide(self, enemy_group, False, pg.sprite.collide_circle):
            sprite.damage(self.dmg)
            pg.draw.ellipse(self.game.screen, (255,255,255), self.rect)
        self.kill()


def spawn_orbiters(game, n = 2, radius = 100, speed = 30, ttl = 500):
    """ Spawns n equidistant Bullet_Orbits around player

    As math.sin() and .cos() use radians (and the formula in Bullet_Orbit divides by speed)
    adding (2/n*pi * speed) to both should make following bullets equally spaced.
    """
    offset = 2/n*math.pi*speed
    for i in range(n):
        Bullet_Orbit(game, game.player, radius, speed, ttl, (1,1,i*offset,i*offset))