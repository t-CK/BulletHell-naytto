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

class Bullet_Line(Bullet):
    """ Bullet flying in a straight line

    Takes two points as tuples or Sprites, spawns at [origin] and follows a line going
    through [target]. Flies at [speed] pixels per tick for [ttl] (time to live) ticks.

    NOTE: Will not register collision when passing through an enemy in a single tick.
    """
    def __init__(self, game, target: tuple or Sprite = None, origin: tuple or Sprite = None, ttl = 60, speed = 5):
        super().__init__()
        self.ttl = ttl
        self.speed = speed
        self.game = game
        if not origin:
            self.origin = game.player.rect.center
        elif type(origin) is not tuple:
            self.origin = origin.rect.center
        self.rect.center = self.origin
        if target:
            if type(target) is tuple:
                self.target = target
            else:
                self.target = target.rect.center
        else:
            try:
                self.target = misc.get_closest_enemy(self.origin).rect.center
            except AttributeError:  # Raised if there are no enemies
                self.kill()
                return
        self.step = misc.get_step_toward(self.origin, self.target)

    def update(self):
        if self.ttl > 0:
            self.ttl -= 1
        else:
            self.kill()
        self.rect.move_ip(self.step)

class Bullet_Orbit(Bullet):
    """ Bullet object circling a constant point at (x,y) or a Sprite.

    Speed-attribute affects time to do a complete circle, thus the velocity of
    the projectile depends on radius as well as speed.
    """
    def __init__(self, game, center_object: tuple or Sprite = (0,0), radius = 100, speed = 30):
        super().__init__()
        self.radius = radius
        self.speed = speed
        self.game = game
        # If first attribute is a tuple, set it as the center, otherwise two variables are used
        if type(center_object) == tuple:
            self.center = (self.centerx, self.centery) = center_object
            self.center_object = None
        else:
            self.center_object = center_object

    def update(self):
        """ If the center is not a tuple, update center point, then calculate position. """
        if self.center_object:
            self.center = (self.centerx, self.centery) = self.center_object.rect.center
        self.rect.center = (self.centerx + self.radius*math.sin(self.game.ticks/self.speed),
                            self.centery + self.radius*math.cos(self.game.ticks/self.speed))