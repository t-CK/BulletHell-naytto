import pygame as pg
import random, math, sys
import weapons, misc, enemies
from pygame.locals import *
from variables import *

def process_event_queue(game):
    """ Check event queue for non-movement related keypresses """
    global mouse_movement_enabled
    game = game
    player = game.player
    for event in pg.event.get():

        # ESC / Close button
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pg.quit()
            sys.exit()
            raise SystemExit

        # M = Toggle mouse
        if event.type == KEYDOWN and event.key == K_m:
            player.mouse_movement_enabled = not player.mouse_movement_enabled

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
                prev = weapons.Bullet_Orbit(game, player, random.randrange(20,200), random.randrange(10,50))
            elif event.key == K_4:
                try:
                    weapons.Bullet_Orbit(game, prev, random.randrange(5,30), random.randrange(1,50))
                except:
                    pass
            elif event.key == K_5:
                for sprite in bullet_group:
                    sprite.kill()
            elif event.key == K_9:
                enemies.Enemy(game)
            elif event.key == K_0:
                for sprite in enemy_group:
                    sprite.death()
        if pg.key.get_pressed()[K_6]:
            weapons.Bullet_Line(game)
        if pg.key.get_pressed()[K_7]:
            weapons.Bullet_Line(game, misc.get_random_enemy())