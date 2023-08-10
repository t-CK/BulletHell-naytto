from variables import *
import math, random

def get_closest_enemy(position: tuple or Sprite = None):
    """ Return enemy Sprite closest to passed point or Sprite (or player by default) """
    if len(enemies) == 0:
        return None
    target = (target_x, target_y) = (0,0)
    if not position:
        position = player
    origin = (origin_x, origin_y) = position if type(position) == tuple else position.rect.center
    for sprite in enemies:
        if get_distance(sprite, origin) < get_distance(target, origin):
            target = sprite
    if target == (0,0):
        return None
    return target

def get_random_enemy():
    """ Return a random enemy Sprite (or None) """
    if len(enemies) > 0:
        return enemies.sprites()[random.randrange(len(enemies))]
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
    
    
# Temporary functions still needed for testing:
def initialize_level():
    """ Initialize level. Just spawn a few random obstacles on screen for now. """
    global spawn_timer
    for _ in range(WIDTH // 150):
        size = (size_x, size_y) = (random.randint(20*SPRITE_SCALE, 100*SPRITE_SCALE),
                                   random.randint(20*SPRITE_SCALE, 100*SPRITE_SCALE))
        position = (pos_x, pos_y) = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        while abs(pos_x - player.rect.center[0]) < 50 + size_x or abs(pos_y - player.rect.center[1]) < 50 + size_y:
            position = (pos_x, pos_y) = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        World(*position, *size)
    spawn_timer = STARTING_SPAWN_TIME

def spawn_enemies():
    """ Spawns enemies at decreasing intervals, starting at STARTING_SPAWN_TIME ticks apart """
    global spawn_timer
    global ticks
    spawn_timer -= 1
    if spawn_timer == 0:
        # Randomize spawn direction (up, right, down, left) and set x and y to be a bit off-screen on that side
        spawn_side = random.randrange(4)
        if spawn_side == 0:   # Up
            x = random.randint(-WIDTH * 0.2, WIDTH * 1.2)
            y = -30
        elif spawn_side == 1: # Right
            x = WIDTH + 30
            y = random.randint(-HEIGHT * 0.3, HEIGHT * 1.3)
        elif spawn_side == 2: # Down
            x = random.randint(-WIDTH * 0.2, WIDTH * 1.2)
            y = HEIGHT + 30
        elif spawn_side == 3: # Left
            x = -30
            y = random.randint(-HEIGHT * 0.3, HEIGHT * 1.3)
        Enemy((x,y))

        # spawn_timer = STARTING_SPAWN_TIME

        # Testing, probably temporary:
        spawn_timer = STARTING_SPAWN_TIME - ticks//100 if STARTING_SPAWN_TIME - ticks//100 > 10 else 10

def check_collisions():
    """ Checks for non-movement related collision.

    Checks collision of bullets/enemies and enemies/player and deals damage for now.
    Movement related collision is in each sprite's update() function, and checking
    distance for pickups happens in the pickup's update().
    """
    for sprite in enemies:
        if pg.sprite.spritecollideany(sprite, bullets):
            sprite.damage()
        if pg.sprite.collide_rect_ratio(1.01)(sprite, player):
            player.damage(sprite.dmg)
            sprite.damage()

def player_death():
    """ Very much temporary, just playing around for now """
    player.surf = pg.transform.rotate(player.surf, 90)
    player.update = lambda *_: None