from pygame import sprite

SCREEN_SIZE = (WIDTH, HEIGHT) = 640, 480

SPRITE_SCALE = 1

FPS = 60
DEFAULT_SPEED = 3
DEFAULT_PICKUP_DISTANCE = 40

STARTING_SPAWN_TIME = 200

all_sprites = sprite.Group() # not including player or UI
bullet_group = sprite.Group()
enemy_group = sprite.Group()
items_group = sprite.Group()
world_group = sprite.Group()
collideable = sprite.Group()
ui_group = sprite.Group()