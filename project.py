import sys, math, random, pygame as pg
from pygame.locals import *

pg.init()

SCREEN_SIZE = (WIDTH, HEIGHT) = 800, 600
SCREEN = pg.display.set_mode(SCREEN_SIZE)

FPS = 60
DEFAULT_SPEED = 5

SPAWN_TIME = 20

clock = pg.time.Clock()

all_sprites = pg.sprite.Group()
bullets = pg.sprite.Group()
enemies = pg.sprite.Group()
collideable = pg.sprite.Group()

ticks = 0
mouse_movement_enabled = False


class Player(pg.sprite.Sprite):
    def __init__(self, hp = 10):
        super().__init__()
        self.surf = pg.Surface([20, 20])
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.hp = hp
        self.speed = DEFAULT_SPEED
        self.invulnerable = 0 # Ticks of invulnerability

        all_sprites.add(self)

    def update(self):
        if self.invulnerable > 0:
            self.invulnerable -= 1
        # Keyboard input for player movement with arrows & WASD
        if not mouse_movement_enabled:
            keys = pg.key.get_pressed()
            if keys[K_UP] or keys[K_w]:
                self.rect.move_ip(0, -self.speed)
                while pg.sprite.spritecollideany(self, collideable):
                    self.rect.move_ip(0, 1)
            if keys[K_RIGHT] or keys[K_d]:
                self.rect.move_ip(self.speed, 0)
                while pg.sprite.spritecollideany(self, collideable):
                    self.rect.move_ip(-1, 0)
            if keys[K_DOWN] or keys[K_s]:
                self.rect.move_ip(0, self.speed)
                while pg.sprite.spritecollideany(self, collideable):
                    self.rect.move_ip(0, -1)
            if keys[K_LEFT] or keys[K_a]:
                self.rect.move_ip(-self.speed, 0)
                while pg.sprite.spritecollideany(self, collideable):
                    self.rect.move_ip(1, 0)

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

    def damage(self, amount = 1):
        if not self.invulnerable:
            self.hp -= amount
            self.invulnerable = 10

            if self.hp <= 0:
                player_death()

class Bullet(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pg.Surface([5,5])
        self.surf.fill((200,0,0))
        self.rect = self.surf.get_rect()

        all_sprites.add(self)
        bullets.add(self)

class Bullet_Line(Bullet):
    """ Bullet flying in a straight line
    
    Takes two points as tuples or Sprites, spawns at [position] and follows a line going 
    through [target]. Flies at [speed] pixels per tick for [ttl] (time to live) ticks.
    
    NOTE: Will not register collision when passing through an enemy in a single tick.
    """
    def __init__(self, target: tuple or Sprite = None, position: tuple or Sprite = None, ttl = 50, speed = 5):
        super().__init__()
        self.ttl = ttl
        self.speed = speed
        if not position:
            self.position = player.rect.center
        elif type(position) is not tuple:
            self.position = position.rect.center
        self.rect.center = self.position
        if target:
            if type(target) is tuple:
                self.target = target
            else:
                self.target = target.rect.center
        else:
            try:
                self.target = get_closest_enemy(self.position).rect.center
            except AttributeError:  # Raised if there are no enemies
                self.kill()
                return
        
        distance = max(1, get_distance(self.target, self.position)) # To prevent division by zero
        self.step = (self.speed*(self.target[0] - self.position[0])/distance,
                     self.speed*(self.target[1] - self.position[1])/distance)

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
    def __init__(self, center_object: tuple or Sprite = (0,0), radius = 100, speed = 30):
        super().__init__()
        self.radius = radius
        self.speed = speed
        # If first attribute is a tuple, set it as the center, otherwise two variables are used
        if type(center_object) == tuple:
            self.center = (self.centerx, self.centery) = center_object
            self.center_object = None
        else:
            self.center_object = center_object

    def update(self):
        if self.center_object:
            self.center = (self.centerx, self.centery) = self.center_object.rect.center

        self.rect.center = (self.centerx + self.radius*math.sin(ticks/self.speed),
                            self.centery + self.radius*math.cos(ticks/self.speed))


class Enemy(pg.sprite.Sprite):
    def __init__(self, position = (0,0), hp = 3, speed = 1, dmg = 1):
        super().__init__()
        self.surf = pg.Surface([15, 15])
        self.color = (60,255,60)
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()
        self.rect.center = position
        self.hp = hp
        self.speed = speed
        self.dmg = dmg
        self.invulnerable = 0

        all_sprites.add(self)
        collideable.add(self)
        enemies.add(self)

    def update(self):
        if self.invulnerable > 0:
            self.invulnerable -= 1

        collideable.remove(self)
        if player.rect.center[0] > self.rect.center[0]:
            self.rect.move_ip(self.speed,0)
            while pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(-1,0)
        elif player.rect.center[0] < self.rect.center[0]:
            self.rect.move_ip(-self.speed,0)
            while pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(1,0)
        if player.rect.center[1] > self.rect.center[1]:
            self.rect.move_ip(0,self.speed)
            while pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(0,-1)
        elif player.rect.center[1] < self.rect.center[1]:
            self.rect.move_ip(0,-self.speed)
            while pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(0,1)
        collideable.add(self)

    def damage(self, amount = 1):
        if self.invulnerable:
            return
        self.hp -= amount
        
        self.surf = pg.transform.scale_by(self.surf, 0.8)
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
            self.kill()


class World(pg.sprite.Sprite):
    """ World object such as an obstacle or a special area of the level
    
    [pos_x] and [pos_y] are coordinates for the top left corner, sizes are the
    sides down and right from that point. If [solid] is True, will be impassable.
    """
    def __init__(self, pos_x, pos_y, size_x, size_y, solid = True):
        super().__init__()
        self.surf = pg.Surface([size_x, size_y])
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect()
        self.solid = solid

        self.rect.topleft = (pos_x, pos_y)

        all_sprites.add(self)
        if self.solid:
            collideable.add(self)


class Ui(pg.sprite.Sprite):
    """ Testailun jäänteitä; per-pixel alpha toimii, mutta ilmeisesti hidas,
        kannattanee oikeasti toteuttaa UI-layer pygame:n set_colorkey():llä
        kunhan sovitaan sille väri
    """
    def __init__(self):
        super().__init__()
        self.surf = pg.Surface((SCREEN_SIZE), pg.SRCALPHA)
        self.surf.fill((0,0,0,0))
        self.rect = self.surf.get_rect()


def main():
    """ Main loop """
    global ticks
    global player

    player = Player()
    player.rect.center = (WIDTH//2, HEIGHT//2)

    initialize_level()

    while True:
        process_event_queue()
        spawn_enemies()
        all_sprites.update()
        check_collisions()
        render_screen()
        clock.tick(FPS)
        ticks += 1


def initialize_level():
    global spawn_timer
    # Spawn a few random obstacles
    for _ in range(WIDTH//150):
        size = (size_x, size_y) = (random.randint(20,120), random.randint(20,120))
        position = (pos_x, pos_y) = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        while abs(pos_x - player.rect.center[0]) < 50 + size_x or abs(pos_y - player.rect.center[1]) < 50 + size_y:
            position = (pos_x, pos_y) = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        World(*position, *size)
    spawn_timer = SPAWN_TIME

def spawn_enemies():
    """ Spawn an enemy every SPAWN_TIME ticks """
    global spawn_timer
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
        spawn_timer = SPAWN_TIME

def process_event_queue():
    global mouse_movement_enabled
    for event in pg.event.get():

        # ESC / Close button
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pg.quit()
            sys.exit()
            raise SystemExit

        # M = Toggle mouse
        if event.type == KEYDOWN and event.key == K_m:
            mouse_movement_enabled = not mouse_movement_enabled

        # Omaa testailua / "Debug-napit"
        global prev
        if event.type == KEYDOWN:
            if event.key == K_1:
                player.speed -= 1
            elif event.key == K_2:
                player.speed += 1
            elif event.key == K_3:
                prev = Bullet_Orbit(player, random.randrange(20,200), random.randrange(10,50))
            elif event.key == K_4:
                try:
                    Bullet_Orbit(prev, random.randrange(5,30), random.randrange(1,50))
                except:
                    pass
            elif event.key == K_5:
                for sprite in bullets:
                    sprite.kill()
            elif event.key == K_6:
                Bullet_Line()
            elif event.key == K_9:
                Enemy()
            elif event.key == K_0:
                for sprite in enemies:
                    sprite.kill()

def check_collisions():
    for sprite in enemies:
        if pg.sprite.spritecollideany(sprite, bullets):
            sprite.damage()
        if pg.sprite.collide_rect_ratio(1.01)(sprite, player):
            player.damage(sprite.dmg)

def render_screen():
    SCREEN.fill((20,20,150))
    for sprite in all_sprites:
        SCREEN.blit(sprite.surf, sprite.rect)
    pg.display.flip()


def player_death():
    pass

def get_closest_enemy(position: tuple or Sprite = None):
    """ Return enemy Sprite closest to passed point or Sprite """
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
    """ Return a random enemy Sprite """
    return enemies.sprites()[random.randrange(len(enemies))]

def get_distance(point1, point2):
    """ Return distance between two tuples or Sprites """
    if type(point1) is not tuple:
        point1 = point1.rect.center
    if type(point2) is not tuple:
        point2 = point2.rect.center
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


if __name__ == "__main__":
    main()