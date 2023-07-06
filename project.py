import sys, math, random, pygame as pg
from pygame.locals import *
import Game_World

pg.init()

SCREEN_SIZE = (WIDTH, HEIGHT) = 1000, 700
SCREEN = pg.display.set_mode(SCREEN_SIZE)

SPRITE_SCALE = 2

FPS = 60
DEFAULT_SPEED = 4
DEFAULT_PICKUP_DISTANCE = 30

STARTING_SPAWN_TIME = 200

clock = pg.time.Clock()

all_sprites = pg.sprite.Group()
bullets = pg.sprite.Group()
enemies = pg.sprite.Group()
collideable = pg.sprite.Group()
ui = pg.sprite.Group()

ticks = 0
mouse_movement_enabled = False

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
    def __init__(self, hp = 20):
        super().__init__()
        try:
            self.surf = pg.image.load("player.png").convert()
            self.surf.set_colorkey((0,255,0))
        except FileNotFoundError:
            self.surf = pg.Surface([15, 20])
            self.surf.fill((255,255,255))
        if (SPRITE_SCALE > 1):
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
        
        # Asetetaan pelaajan X ja Y sijainnit kartalla
        # Pelaaja asetetaan aloittamaan keskeltä pelialuetta
        self._map_x = Game_World.MAP_WIDTH / 2
        self._map_y = Game_World.MAP_HEIGHT / 2

        all_sprites.add(self)

    def update(self):
        """ Decreases i-frames, also checks for movement input for now. """
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


class Bullet(pg.sprite.Sprite):
    """ Parent class for bullets """
    def __init__(self):
        super().__init__()
        self.surf = pg.Surface([5,5])
        self.surf.fill((200,0,0))
        self.rect = self.surf.get_rect()

        all_sprites.add(self)
        bullets.add(self)

class Bullet_Line(Bullet):
    """ Bullet flying in a straight line

    Takes two points as tuples or Sprites, spawns at [origin] and follows a line going
    through [target]. Flies at [speed] pixels per tick for [ttl] (time to live) ticks.

    NOTE: Will not register collision when passing through an enemy in a single tick.
    """
    def __init__(self, target: tuple or Sprite = None, origin: tuple or Sprite = None, ttl = 60, speed = 5):
        super().__init__()
        self.ttl = ttl
        self.speed = speed
        if not origin:
            self.origin = player.rect.center
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
        """ If the center is not a tuple, update center point, then calculate position. """
        if self.center_object:
            self.center = (self.centerx, self.centery) = self.center_object.rect.center

        self.rect.center = (self.centerx + self.radius*math.sin(ticks/self.speed),
                            self.centery + self.radius*math.cos(ticks/self.speed))


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
    def __init__(self, position = (0,0), hp = 3, speed = 1, dmg = 1):
        super().__init__()
        try:
            self.surf = pg.image.load("enemy.png").convert()
            self.surf.set_colorkey((0,255,0))
            self.color = None
        except FileNotFoundError:
            self.surf = pg.Surface([12, 19])
            self.color = (60,255,60)
            self.surf.fill(self.color)
        if (SPRITE_SCALE > 1):
            self.surf = pg.transform.scale_by(self.surf, SPRITE_SCALE)

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
        """ Decrease i-frames and move towards player. Move back until there's no collision. """
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
        Xp(*self.rect.center, random.randrange(len(Xp._colors))+1)
        self.kill()


class World(pg.sprite.Sprite):
    """ World object such as an obstacle or a special area of the level

    [pos_x] and [pos_y] are coordinates for the top left corner, sizes are the
    sides down and right from that point. If [solid] is True, will be impassable.
    """
    def __init__(self, pos_x, pos_y, size_x, size_y, solid = True):
        super().__init__()
        self.surf = pg.Surface([size_x, size_y])
        self.surf.fill((200,30,30))
        self.rect = self.surf.get_rect()
        self.solid = solid

        self.rect.topleft = (pos_x, pos_y)

        all_sprites.add(self)
        if self.solid:
            collideable.add(self)

class Xp(pg.sprite.Sprite):
    """ XP globe dying enemies drop """
    # Testinä huvin vuoks lista väreistä xp-arvon mukaan:
    _colors = [(140, 70, 255), (200, 70, 230), (255, 180, 120), (180, 240, 0), (200, 200, 40), (255, 255, 100)]
    def __init__(self, pos_x, pos_y, xp_amount = 1):
        super().__init__()
        self.size = 5 + 3*xp_amount
        self.surf = pg.Surface([self.size, self.size])
        self.xp_amount = xp_amount
        if xp_amount <= len(self._colors):
            self.surf.fill(self._colors[xp_amount-1])
        else:
            self.surf.fill(self._colors[-1])
        self.rect = self.surf.get_rect()
        self.rect.center = (pos_x, pos_y)

        all_sprites.add(self)

    def update(self):
        """ Check distance to player and if close, call for pickup() """
        if get_distance(self, player) < player.pickup_distance:
            self.pickup()

    def pickup(self):
        """ Get picked up and increase player XP """
        self.kill()
        player.xp += self.xp_amount
        if player.xp >= player.xp_to_next_level:
            player.levelup()


class Ui(pg.sprite.Sprite):
    """ UI parent class (pretty unnecessary at the moment) """
    def __init__(self):
        super().__init__()
        self.surf = pg.Surface((SCREEN_SIZE))
        self.surf.fill((0, 255, 0))
        self.surf.set_colorkey((0, 255, 0))

        all_sprites.add(self)
        ui.add(self)

class Ui_Bar(Ui):
    """ XP / Health bar on top of screen 
    
    Variables value and value_max are methods, that are called to get the
    current and maximum values for the bar's length
    """
    def __init__(self, value = None, value_max = None):
        super().__init__()
        self.bar_height = HEIGHT//100
        self.bar_max_width = WIDTH//2
        self.surf = pg.Surface((self.bar_max_width, self.bar_height))
        self.rect = self.surf.get_rect()
        self.surf.fill((0, 255, 0))
        self.surf.set_colorkey((0, 255, 0))
        self.color = (0, 0, 0)
        self.value = value
        self.value_max = value_max
                
    def update(self):
        if not self.value_max:
            bar_width = 0
        else:
            bar_width = self.value()/self.value_max() * self.bar_max_width
        
        pg.draw.rect(self.surf, (0, 0, 0), (0, 0, self.bar_max_width, self.bar_height), 0, HEIGHT//300)
        pg.draw.rect(self.surf, self.color, (0, 0, bar_width, self.bar_height), 0, HEIGHT//300)

class Ui_Bar_XP(Ui_Bar):
    """ XP Bar on top of screen, purplish """
    def __init__(self):
        super().__init__(player.get_xp, player.get_xp_to_next_level)
        self.rect.topleft = (WIDTH//4, HEIGHT//19 + 7)
        self.color = (150, 50, 255)

class Ui_Bar_Health(Ui_Bar):
    """ Health Bar on top of screen, red """
    def __init__(self):
        super().__init__(player.get_hp, player.get_hp_max)
        self.rect.topleft = (WIDTH//4, HEIGHT//19 - 7)
        self.color = (255, 0, 0)

def main():
    """ Initialization and main loop """
    global ticks
    global player

    player = Player()
    player.rect.center = (WIDTH//2, HEIGHT//2)
    Ui_Bar_XP()
    Ui_Bar_Health()

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


def process_event_queue():
    """ Check event queue for non-movement related keypresses """
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

        # Omaa testailua / Väliaikaiset "Debug-napit"
        """ 1 = Player speed down
            2 = Player speed up
            3 = Spawn bullet orbiting player
            4 = Spawn bullet orbiting previous bullet spawned with 3
            5 = Despawn bullets
            6 = Spawn bullet towards closest enemy
            7 = Spawn bullet towards random enemy
            9 = Spawn enemy
            0 = Kill enemies
        """
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
            elif event.key == K_9:
                Enemy()
            elif event.key == K_0:
                for sprite in enemies:
                    sprite.death()
        if pg.key.get_pressed()[K_6]:
            Bullet_Line()
        if pg.key.get_pressed()[K_7]:
            Bullet_Line(get_random_enemy())

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

def render_screen():
    """ Fill background, blit sprites and flip() the screen """
    SCREEN.fill((20,20,150))
    for sprite in all_sprites:
        SCREEN.blit(sprite.surf, sprite.rect)
    # Tiedän että ui piirretään näin kahdesti, koska on myös all_spritesissa,
    # mutta jostain syystä ei piirry, jos ei ole siinäkin.
    # Toistetaan se anyway, jotta ui on päällimmäisenä.
    for sprite in ui:
        SCREEN.blit(sprite.surf, sprite.rect)
    pg.display.flip()


def player_death():
    """ Very much temporary, just playing around for now """
    player.surf = pg.transform.rotate(player.surf, 90)
    player.update = lambda *_: None

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


if __name__ == "__main__":
    main()