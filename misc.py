import random, math
from pygame import display
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

def get_distance(point1, point2 = (0,0)):
    """ Return distance between two tuples or Sprites' centers.
    
    Point2 defaults to (0,0), so passing only one point returns length of the single vector """
    if type(point1) is not tuple:
        point1 = point1.rect.center
    if type(point2) is not tuple:
        point2 = point2.rect.center
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def get_step(origin: tuple or Sprite, target: tuple or Sprite, speed = 1):
    """ Return a tuple for movement from [origin] to [target] at [speed] pixels per tick """
    if not type(origin) == tuple:
        origin = origin.rect.center
    if not type(target) == tuple:
        target = target.rect.center
    distance = max(1, get_distance(origin, target)) # To prevent division by zero
    return (speed*(target[0] - origin[0])/distance, speed*(target[1] - origin[1])/distance)

def get_step_p(vector: tuple, speed = 1, inverse = False):
    """ Take a vector and return a perpendicular vector of length speed.

    In other words, turns the vector 90 degrees clockwise (with inaccuracies related to speed,
    as positions (for now at least) directly use pygame's Rects, which convert coordinates to ints).

    If inverse is truthy, turns anti-clockwise instead. """
    x, y = vector
    speed_factor = speed / get_distance((0,0), vector)    
    
    if inverse:
        return (-y * speed_factor, x * speed_factor)
    else:
        return (y * speed_factor, -x * speed_factor)
        
def get_spawn(side = None):
    """ Returns a tuple of a random point a bit off-screen.
    
    Parameter side excepts an int of 0, 1, 2 or 3, 
    representing the upper, right-hand, lower and left-hand sides 
    of the screen, respectively. If side == None, will be randomized.
    """
    WIDTH, HEIGHT = display.get_window_size()
    if not side:
        side = random.randrange(4)
    if side == 0:   # Up
        x = random.randint(-WIDTH * 0.2, WIDTH * 1.2)
        y = -30
    elif side == 1: # Right
        x = WIDTH + 30
        y = random.randint(-HEIGHT * 0.3, HEIGHT * 1.3)
    elif side == 2: # Down
        x = random.randint(-WIDTH * 0.2, WIDTH * 1.2)
        y = HEIGHT + 30
    elif side == 3: # Left
        x = -30
        y = random.randint(-HEIGHT * 0.3, HEIGHT * 1.3)
    else:
        print("Invalid spawn side")
    return (x, y)