import pygame as pg

# SCREEN_SIZE = (WIDTH, HEIGHT) = pg.display.get_window_size()
# SCREEN = pg.display.set_mode(SCREEN_SIZE)

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
ui_group = pg.sprite.Group()

ticks = 0
mouse_movement_enabled = False