import random, math
from variables import *

def get_closest_enemy(position: tuple or Sprite = None):
    """ Return enemy Sprite closest to passed point or Sprite (or player by default) """
    if len(enemy_group) == 0:
        return None
    target = (target_x, target_y) = (0,0)
    if not position:
        position = player
    origin = (origin_x, origin_y) = position if type(position) == tuple else position.rect.center
    for sprite in enemy_group:
        if get_distance(sprite, origin) < get_distance(target, origin):
            target = sprite
    if target == (0,0):
        return None
    return target

def get_random_enemy():
    """ Return a random enemy Sprite (or None) """
    if len(enemy_group) > 0:
        return enemy_group.sprites()[random.randrange(len(enemy_group))]
    else:
        return None

def get_distance(point1, point2):
    """ Return distance between two tuples or Sprites' centers """
    if type(point1) is not tuple:
        point1 = point1.rect.center
    if type(point2) is not tuple:
        point2 = point2.rect.center
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def get_step_toward(origin: tuple or Sprite, target: tuple or Sprite, speed = 5):
    """ Return a tuple for movement from [origin] to [target] at [speed] pixels per tick """
    if not type(origin) == tuple:
        origin = origin.rect.center
    if not type(target) == tuple:
        target = target.rect.center
    distance = max(1, get_distance(origin, target)) # To prevent division by zero
    return (speed*(target[0] - origin[0])/distance, speed*(target[1] - origin[1])/distance)