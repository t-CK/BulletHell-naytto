import sys, math, random, pygame as pg
from pygame.locals import *

pg.init()

SCREEN_SIZE = (WIDTH, HEIGHT) = 800, 600
SCREEN = pg.display.set_mode(SCREEN_SIZE)

FPS = 60
DEFAULT_SPEED = 5

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
        
        all_sprites.add(self)
        
    def update(self):
        # Keyboard input for player movement with arrows & WASD
        if not mouse_movement_enabled:
            keys = pg.key.get_pressed()
            if keys[K_UP] or keys[K_w]:
                self.rect.move_ip(0, -self.speed)
                while pg.sprite.spritecollide(player, collideable, False):
                    self.rect.move_ip(0, 1)
            if keys[K_RIGHT] or keys[K_d]:
                self.rect.move_ip(self.speed, 0)
                while pg.sprite.spritecollide(player, collideable, False):
                    self.rect.move_ip(-1, 0)
            if keys[K_DOWN] or keys[K_s]:
                self.rect.move_ip(0, self.speed)
                while pg.sprite.spritecollide(player, collideable, False):
                    self.rect.move_ip(0, -1)
            if keys[K_LEFT] or keys[K_a]:
                self.rect.move_ip(-self.speed, 0)
                while pg.sprite.spritecollide(player, collideable, False):
                    self.rect.move_ip(1, 0)
        
        # Mouse movement testing
        else:
            MIN_MOUSE_DISTANCE = 30
            mouse_x, mouse_y = pg.mouse.get_pos()
            distance_from_player = math.sqrt((mouse_x - player.rect.center[0])**2 + (mouse_y - player.rect.center[1])**2)
            speed_multiplier = min(1, (distance_from_player - MIN_MOUSE_DISTANCE)/WIDTH*3.5)
            print(speed_multiplier)
            
            if distance_from_player > MIN_MOUSE_DISTANCE:
                if 3*abs(mouse_x - player.rect.center[0])/WIDTH > abs(mouse_y - player.rect.center[1])/HEIGHT:
                    if mouse_x > player.rect.center[0]:
                        self.rect.move_ip(self.speed * speed_multiplier, 0)
                    else:
                        self.rect.move_ip(-self.speed * speed_multiplier, 0)
                if abs(mouse_x - player.rect.center[0])/WIDTH < 2*abs(mouse_y - player.rect.center[1])/HEIGHT:
                    if mouse_y > player.rect.center[1]:
                        self.rect.move_ip(0, self.speed * speed_multiplier)
                    else:
                        self.rect.move_ip(0, -self.speed * speed_multiplier)

        
    def damage(self, amount = 1):
        self.hp -= amount
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
        
    def update(self):
        pass

class Bullet_Circle(Bullet):
    """ Bullet object circling a constant point at (x,y) or a Sprite-object.
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
    def __init__(self, hp = 1, speed = 1):
        super().__init__()
        self.surf = pg.Surface([10, 10])
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.hp = hp
        self.speed = speed
        
        all_sprites.add(self)
        enemies.add(self)
        
    def update(self):
        if player.rect.center[0] > self.rect.center[0]:
            self.rect.move_ip(self.speed,0)
            while pg.sprite.spritecollide(self, collideable, False):
                self.rect.move_ip(-1,0)
        elif player.rect.center[0] < self.rect.center[0]:
            self.rect.move_ip(-self.speed,0)
            while pg.sprite.spritecollide(self, collideable, False):
                self.rect.move_ip(1,0) 
        if player.rect.center[1] > self.rect.center[1]:
            self.rect.move_ip(0,self.speed)
            while pg.sprite.spritecollide(self, collideable, False):
                self.rect.move_ip(0,-1)
        elif player.rect.center[1] < self.rect.center[1]:
            self.rect.move_ip(0,-self.speed)
            while pg.sprite.spritecollide(self, collideable, False):
                self.rect.move_ip(0,1)
        
    def damage(self, amount = 1):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()

class World(pg.sprite.Sprite):
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
        
    def update(self):
        pass

        
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
    """Main loop"""
    global ticks
    while True:
        process_event_queue()
        all_sprites.update()
        check_collisions()
        render_screen()
        clock.tick(FPS)
        ticks += 1
        
        print(clock.get_rawtime())


def process_event_queue():
    """Käy event queue läpi"""
    global mouse_movement_enabled
    for event in pg.event.get():
    
        # Jos ikkuna suljetaan tai painetaan ESCiä, suljetaan
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pg.quit()
            sys.exit()
            raise SystemExit
        
        # M = Toggle mouse
        if event.type == KEYDOWN and event.key == K_m:
            mouse_movement_enabled = not mouse_movement_enabled
            
        # Omaa testailua
        global prev
        if event.type == KEYDOWN:
            if event.key == K_1:
                player.speed -= 1
            elif event.key == K_2:
                player.speed += 1
            elif event.key == K_3:
                prev = Bullet_Circle(player, random.randrange(20,200), random.randrange(10,50))
            elif event.key == K_4:
                try:
                    Bullet_Circle(prev, random.randrange(5,30), random.randrange(1,50))
                except:
                    pass
            elif event.key == K_5:
                for sprite in bullets:
                    sprite.kill()
            elif event.key == K_9:
                Enemy()
            elif event.key == K_0:
                for sprite in enemies:
                    sprite.kill()

def check_collisions():
    for sprite in enemies:
        if pg.sprite.spritecollide(sprite, bullets, False):
            sprite.damage()
        if pg.sprite.spritecollide(player, enemies, False):
            player.damage()

def render_screen():
    """Päivitä näyttö"""
    SCREEN.fill((20,20,150))
    for sprite in all_sprites:
        SCREEN.blit(sprite.surf, sprite.rect)
    pg.display.flip()

    
def player_death():
    pass


if __name__ == "__main__":

    player = Player()
    player.rect.center = (WIDTH//2, HEIGHT//2)
    World(30,30,30,30); World(WIDTH-70, HEIGHT-140, 30,30)

    main()