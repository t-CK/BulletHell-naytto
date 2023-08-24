from pygame import event
from pygame import key
from pygame import locals
from pygame import sprite
from pygame import mouse
import random
import misc
import weapons
import enemies
import pickups
from Log import *
from sys import exit
from pygame import quit
from enum import Enum

from variables import *

class Input:
    # _p1 :Player, Referenssi pelaajaobjektiin
    # _game :Game, Referenssi peliin

    def __init__(self, game, player) -> None:
        self._p1 = player
        self._game = game

    def get_input(self):
        
        keys = key.get_pressed()

        # Pelaajan liikutus
        if self._p1.hp > 0:
            if not self._p1.mouse_movement_enabled:
                if keys[locals.K_UP]:
                    self._p1.move_y(-1)
                    self._game.update_map(0, 1)
                    while sprite.spritecollideany(self._p1, collideable):
                        self._p1.move_y(1)
                        self._game.update_map(0, -1)
                elif keys[locals.K_DOWN]:
                    self._p1.move_y(1)
                    self._game.update_map(0, -1)
                    while sprite.spritecollideany(self._p1, collideable):
                        self._p1.move_y(-1)
                        self._game.update_map(0, 1)
                if keys[locals.K_RIGHT]:
                    self._p1.move_x(1)
                    self._game.update_map(-1, 0)
                    while sprite.spritecollideany(self._p1, collideable):
                        self._p1.move_x(-1)
                        self._game.update_map(1, 0)
                elif keys[locals.K_LEFT]:
                    self._p1.move_x(-1)
                    self._game.update_map(1, 0)
                    while sprite.spritecollideany(self._p1, collideable):
                        self._p1.move_x(1)
                        self._game.update_map(-1, 0)
                    
            else:
                MIN_MOUSE_DISTANCE = 150
                mouse_x, mouse_y = mouse.get_pos()
                distance_from_player = misc.get_distance((mouse_x, mouse_y), self._p1.rect.center)
        
                if distance_from_player > MIN_MOUSE_DISTANCE:
                    if 2*abs(mouse_x - self._p1.rect.center[0])/self._game._wnd_size[1] > abs(mouse_y - self._p1.rect.center[1])/self._game._wnd_size[1]:
                        if mouse_x > self._p1.rect.center[0]:
                            self._p1.move_x(1)
                            self._game.update_map(-1, 0)
                            while sprite.spritecollideany(self._p1, collideable):
                                self._p1.move_x(-1)
                                self._game.update_map(1, 0)
                        else:
                            self._p1.move_x(-1)
                            self._game.update_map(1, 0)
                            while sprite.spritecollideany(self._p1, collideable):
                                self._p1.move_x(1)
                                self._game.update_map(-1, 0)
                    if abs(mouse_x - self._p1.rect.center[0])/self._game._wnd_size[1] < 3*abs(mouse_y - self._p1.rect.center[1])/self._game._wnd_size[0]:
                        if mouse_y > self._p1.rect.center[1]:
                            self._p1.move_y(1)
                            self._game.update_map(0, -1)
                            while sprite.spritecollideany(self._p1, collideable):
                                self._p1.move_y(-1)
                                self._game.update_map(0, 1)
                        else:
                            self._p1.move_y(-1)
                            self._game.update_map(0, 1)
                            while sprite.spritecollideany(self._p1, collideable):
                                self._p1.move_y(1)
                                self._game.update_map(0, -1)

        # Käsitellään jonossa olevat eventit
        for e in event.get():

            # Close button tai F10
            if e.type == locals.QUIT or (e.type == locals.KEYDOWN and e.key == locals.K_F10):
                quit()
                exit()
                raise SystemExit
            # Vaihdetaan Game_State PAUSED ja RUNNING välillä painettaessa esc -näppäintä
            if e.type == locals.KEYDOWN and e.key == locals.K_ESCAPE:
                state_temp = self._game.get_state()
                if state_temp == 0:
                    self._game.toggle_state(1)
                else:
                    self._game.toggle_state(0)
                    
            # M = Toggle mouse
            if e.type == locals.KEYDOWN and e.key == locals.K_m:
                self._p1.mouse_movement_enabled = not self._p1.mouse_movement_enabled
                    
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
            if e.type == locals.KEYDOWN:
                if e.key == locals.K_1:
                    weapons.Orbiters(self._game, 3)
                elif e.key == locals.K_2:
                    weapons.Orbiters(self._game, 9)
                elif e.key == locals.K_3:
                    offset = (random.randrange(0,4), random.randrange(0,4), random.randrange(0,20), random.randrange(0,20))
                    prev = weapons.Bullet_Orbit(self._game, self._p1, random.randrange(20,150), random.randrange(10,50), -1, offset)
                elif e.key == locals.K_4:
                    try:
                        offset = (random.randrange(0,4), random.randrange(0,4), random.randrange(0,20), random.randrange(0,20))
                        weapons.Bullet_Orbit(self._game, prev, random.randrange(5,30), random.randrange(1,50), -1, offset)
                    except:
                        pass
                elif e.key == locals.K_5:
                    for s in bullet_group:
                        s.kill()
                elif e.key == locals.K_9:
                    enemies.Enemy_Sine(self._game)
                elif e.key == locals.K_0:
                    for s in enemy_group:
                        s.death()
                elif e.key == locals.K_p:
                    enemies.Enemy_Follow(self._game)
                elif e.key == locals.K_o:
                    enemies.Enemy_Worm_Head(self._game)
                elif e.key == locals.K_i:
                    pickups.Item_Bombs(self._game, 100,100)
                elif e.key == locals.K_z:
                    weapons.Orbiters(self._game, 2, 50)
                    weapons.Orbiters(self._game, 4, 70)
                    weapons.Orbiters(self._game, 6, 90)
                    weapons.Orbiters(self._game, 8, 110)
                    weapons.Orbiters(self._game, 10, 130)
                elif e.key == locals.K_x:
                    weapons.Orbiters(self._game, 2, 50, -30)
                    weapons.Orbiters(self._game, 4, 70)
                    weapons.Orbiters(self._game, 6, 90, -30)
                    weapons.Orbiters(self._game, 8, 110)
                elif e.key == locals.K_c:
                    weapons.Orbiters(self._game, 20, 50)
                    weapons.Orbiters(self._game, 20, 70, -30)
                    
            if keys[locals.K_6]:
                weapons.Bullet_Line(self._game)
            if keys[locals.K_7]:
                weapons.Bullet_Line(self._game, misc.get_random_enemy())
            if keys[locals.K_8]:
                weapons.Bullet_Sine(self._game)