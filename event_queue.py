import pygame as pg
import random, math, sys
import weapons, misc, enemies, pickups
from pygame.locals import *
from variables import *

def process_event_queue(game):
    """ Check event queue for non-movement related keypresses """
    game = game
    player = game.player

    # Keyboard input for player movement with arrows & WASD
    if not player.mouse_movement_enabled and player.hp > 0:
        keys = pg.key.get_pressed()
        if keys[K_UP] or keys[K_w]:
            player.move_player(0, -player.speed)
            while pg.sprite.spritecollideany(player, collideable):
                player.move_player(0, 1)
        if keys[K_RIGHT] or keys[K_d]:
            player.move_player(player.speed, 0)
            while pg.sprite.spritecollideany(player, collideable):
                player.move_player(-1, 0)
        if keys[K_DOWN] or keys[K_s]:
            player.move_player(0, player.speed)
            while pg.sprite.spritecollideany(player, collideable):
                player.move_player(0, -1)
        if keys[K_LEFT] or keys[K_a]:
            player.move_player(-player.speed, 0)
            while pg.sprite.spritecollideany(player, collideable):
                player.move_player(1, 0)

    # Mouse movement
    elif player.mouse_movement_enabled and player.hp > 0:
        MIN_MOUSE_DISTANCE = 30
        mouse_x, mouse_y = pg.mouse.get_pos()
        distance_from_player = misc.get_distance((mouse_x, mouse_y), player.rect.center)
        speed_multiplier = min(1, (distance_from_player - MIN_MOUSE_DISTANCE)/game._wnd_size[1]*3.5)

        if distance_from_player > MIN_MOUSE_DISTANCE:
            if 3*abs(mouse_x - player.rect.center[0])/game._wnd_size[1] > abs(mouse_y - player.rect.center[1])/game._wnd_size[1]:
                if mouse_x > player.rect.center[0]:
                    player.move_player(player.speed * speed_multiplier, 0)
                    while pg.sprite.spritecollideany(player, collideable):
                        player.move_player(-1, 0)
                else:
                    player.move_player(-player.speed * speed_multiplier, 0)
                    while pg.sprite.spritecollideany(player, collideable):
                        player.move_player(1, 0)
            if abs(mouse_x - player.rect.center[0])/game._wnd_size[1] < 2*abs(mouse_y - player.rect.center[1])/game._wnd_size[0]:
                if mouse_y > player.rect.center[1]:
                    player.move_player(0, player.speed * speed_multiplier)
                    while pg.sprite.spritecollideany(player, collideable):
                        player.move_player(0, -1)
                else:
                    player.move_player(0, -player.speed * speed_multiplier)
                    while pg.sprite.spritecollideany(player, collideable):
                        player.move_player(0, 1)


    for event in pg.event.get():

        # ESC / Close button
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pg.quit()
            sys.exit()
            raise SystemExit

        # M = Toggle mouse
        if event.type == KEYDOWN and event.key == K_m:
            player.mouse_movement_enabled = not player.mouse_movement_enabled

# Temporary debug buttons for testing
        """ 1 = Spawn 3 orbiters
            2 = Spawn 9 orbiters
            3 = Spawn bullet orbiting player (with ugly random offset)
            4 = Spawn bullet orbiting previous bullet spawned with 3
            5 = Despawn bullets
            6 = Spawn bullet towards closest enemy
            7 = Spawn bullet towards random enemy
            8 = Spawn (WIP) sine bullet
            9 = Spawn (WIP) sine enemy
            0 = Kill enemies
            P = Spawn Enemy_Follow
            O = Spawn Worm (very WIP)
            I = Spawn a bomb pickup
            
            Z, X, C = Some patterns made with weapons.Orbiters()
        """
        global prev
        if event.type == KEYDOWN:
            if event.key == K_1:
                weapons.Orbiters(game, 3)
            elif event.key == K_2:
                weapons.Orbiters(game, 9)
            elif event.key == K_3:
                offset = (random.randrange(0,4), random.randrange(0,4), random.randrange(0,20), random.randrange(0,20))
                prev = weapons.Bullet_Orbit(game, player, random.randrange(20,150), random.randrange(10,50), -1, offset)
            elif event.key == K_4:
                try:
                    offset = (random.randrange(0,4), random.randrange(0,4), random.randrange(0,20), random.randrange(0,20))
                    weapons.Bullet_Orbit(game, prev, random.randrange(5,30), random.randrange(1,50), -1, offset)
                except:
                    pass
            elif event.key == K_5:
                for sprite in bullet_group:
                    sprite.kill()
            elif event.key == K_9:
                enemies.Enemy_Sine(game)
            elif event.key == K_0:
                for sprite in enemy_group:
                    sprite.death()
            elif event.key == K_p:
                enemies.Enemy_Follow(game)
            elif event.key == K_o:
                enemies.Enemy_Worm_Head(game)
            elif event.key == K_i:
                pickups.Item_Bombs(game, 100,100)
            elif event.key == K_z:
                weapons.Orbiters(game, 2, 50)
                weapons.Orbiters(game, 4, 70)
                weapons.Orbiters(game, 6, 90)
                weapons.Orbiters(game, 8, 110)
                weapons.Orbiters(game, 10, 130)
            elif event.key == K_x:
                weapons.Orbiters(game, 2, 50, -30)
                weapons.Orbiters(game, 4, 70)
                weapons.Orbiters(game, 6, 90, -30)
                weapons.Orbiters(game, 8, 110)
            elif event.key == K_c:
                weapons.Orbiters(game, 20, 50)
                weapons.Orbiters(game, 20, 70, -30)
                
        if pg.key.get_pressed()[K_6]:
            weapons.Bullet_Line(game)
        if pg.key.get_pressed()[K_7]:
            weapons.Bullet_Line(game, misc.get_random_enemy())
        if pg.key.get_pressed()[K_8]:
            weapons.Bullet_Sine(game)
