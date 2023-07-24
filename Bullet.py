from pygame import sprite, surface
from Player import Player
from Game import Game
import math

class Bullet(sprite.Sprite):
    """ Parent class for bullets """
    def __init__(self, game :Game):
        super().__init__()
        self.surf = surface.Surface([5,5])
        self.surf.fill((200,0,0))
        self.rect = self.surf.get_rect()

        self._game = game

        # Lisätään Bullet pelin spriteihin
        game.add_sprite(self)
        
        bullets.add(self)

class Bullet_Line(Bullet):
    """ Bullet flying in a straight line

    Takes two points as tuples or Sprites, spawns at [origin] and follows a line going
    through [target]. Flies at [speed] pixels per tick for [ttl] (time to live) ticks.

    NOTE: Will not register collision when passing through an enemy in a single tick.
    """
    def __init__(self, player :Player, target: tuple or sprite.Sprite = None, origin: tuple or sprite.Sprite = None, ttl = 60, speed = 5):
        super().__init__()
        self._p1 = player
        self.ttl = ttl
        self.speed = speed
        if not origin:
            self.origin = self._p1.rect.center
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
                self.target = get_closest_enemy(self.origin).rect.center
            except AttributeError:  # Raised if there are no enemies
                self.kill()
                return
        self.step = get_step_toward(self.origin, self.target)

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
    def __init__(self, game :Game, center_object: tuple or sprite.Sprite = (0,0), radius = 100, speed = 30):
        super().__init__()
        self._game = game
        self.radius = radius
        self.speed = speed
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

        self.rect.center = (self.centerx + self.radius*math.sin(self._game.get_delta_time()/self.speed),
                            self.centery + self.radius*math.cos(self._game.get_delta_time()/self.speed))