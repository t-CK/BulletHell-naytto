import math, random
import pygame as pg
import weapons, enemies, world, pickup, ui, event_queue, misc
from player import Player
from variables import *

pg.init()

class Game():
    def __init__(self):
        self.ticks = 0
        self.player = Player()
        self.initialize_game()

    def initialize_game(self):
        """ Initialize player, Ui etc. """
        self.player.rect.center = (WIDTH//2, HEIGHT//2)
        ui.Ui_Bar_XP(self.player)
        ui.Ui_Bar_Health(self.player)
        initialize_level()
    
    def main(self):
        """ Main loop """
        while True:
            event_queue.process_event_queue(self)
            spawn_enemies()
            self.player.update()
            all_sprites.update()
            check_collisions()
            render_screen()
            clock.tick(FPS)
            self.ticks += 1

def initialize_level():
    """ Initialize level. Just spawn a few random obstacles on screen for now. """
    global spawn_timer
    for _ in range(WIDTH // 150):
        size = (size_x, size_y) = (random.randint(20*SPRITE_SCALE, 100*SPRITE_SCALE),
                                   random.randint(20*SPRITE_SCALE, 100*SPRITE_SCALE))
        position = (pos_x, pos_y) = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        while abs(pos_x - WIDTH) < 50 + size_x or abs(pos_y - HEIGHT) < 50 + size_y:
            position = (pos_x, pos_y) = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        world.World(*position, *size)
    spawn_timer = STARTING_SPAWN_TIME

def spawn_enemies():
    """ Spawns enemies at decreasing intervals, starting at STARTING_SPAWN_TIME ticks apart """
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
        enemies.Enemy(game, (x,y))
        spawn_timer = STARTING_SPAWN_TIME - game.ticks//100 if STARTING_SPAWN_TIME - game.ticks//100 > 10 else 10

def check_collisions():
    """ Checks for non-movement related collision.

    Checks collision of bullets/enemies and enemies/player and deals damage for now.
    Movement related collision is in each sprite's update() function, and checking
    distance for pickups happens in the pickup's update().
    """
    for sprite in enemy_group:
        if pg.sprite.spritecollideany(sprite, bullet_group):
            sprite.damage()
        if pg.sprite.collide_rect_ratio(1.01)(sprite, game.player):
            game.player.damage(sprite.dmg)
            sprite.damage()

def render_screen():
    """ Fill background, blit sprites and flip() the screen """
    SCREEN.fill((20,20,150))
    # for sprite in all_sprites:
        # SCREEN.blit(sprite.surf, sprite.rect)
    for group in (items_group, enemy_group, world_group, bullet_group):
        for sprite in group:
            SCREEN.blit(sprite.surf, sprite.rect)
    SCREEN.blit(game.player.surf, game.player.rect)
    for sprite in ui_group:
        SCREEN.blit(sprite.surf, sprite.rect)
    pg.display.flip()

if __name__ == "__main__":
    game = Game()
    game.main()
