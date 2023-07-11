import pygame
from random import randint
from pygame.sprite import *

MAP_WIDTH = 1000
MAP_HEIGHT = 1000
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 800
MOVE_SPEED = 10

class Game_Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.surface.Surface([100, 100])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self._pos_x = randint(0, MAP_WIDTH)
        self._pos_y = randint(0, MAP_HEIGHT)
        self.rect.center = [self._pos_x, self._pos_y]
        print(f"X:{self._pos_x} : Y:{self._pos_y}")
        
    def Get_X(self) -> float:
        return self._pos_x
    
    def Get_Y(self):
        return self._pos_y
    
    def obj_update(self, x :int, y :int):
        self._pos_x -= x
        self._pos_y -= y
        temp = (self._pos_x, self._pos_y)
        self.rect.center = temp

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self._pos_x = 200
        self._pos_y = 200
        self.image = pygame.surface.Surface([100, 100])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
    
    def Get_X(self) -> float:
        return self._pos_x
    
    def Get_Y(self):
        return self._pos_y
    
    def move_right(self, value :float):
        if (self._pos_x + value * MOVE_SPEED) >= 0 and (self._pos_x + value * MOVE_SPEED) <= self._pos_x + SCREEN_WIDTH:
            self._pos_x += value
            self.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
            print(f"Player X:{self._pos_x} : Y:{self._pos_y}")
        
    def move_down(self, value :float):
        if (self._pos_y + value * MOVE_SPEED) >= 0 and (self._pos_y + value * MOVE_SPEED) <= self._pos_y + SCREEN_HEIGHT:
            self._pos_y += value
            self.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
#            print(f"Player X:{self._pos_x} : Y:{self._pos_y}")

class Map:
    # Kameran X ja Y sijainti
    _camera_x :int
    _camera_y :int
    # Referenssi pelaajaan
    _p1 :Player
    
    def __init__(self, player :Player) -> None:
        self._p1 = player
        self._camera_x = self._p1.Get_X()
        self._camera_y = self._p1.Get_Y()
       
    
    def Update(self) -> tuple:
        """Päivittää kameran sijainnin vastaamaan pelaajan sijaintia kartalla ja palauttaa sijainnin tuplena"""
        # Päivitetään kameran sijainti vastaamaan pelaajan sijaintia
        self._camera_x = self._p1.Get_X()
        self._camera_y = self._p1.Get_Y()
        # Palautetaan kameran sijainti tuplena
        return (self._camera_x, self._camera_y)

pygame.init()
flags =  pygame.DOUBLEBUF | pygame.HWACCEL | pygame.SHOWN
wnd = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=flags)
pygame.key.set_repeat(10, 0)

player = Player()
other = Game_Sprite()
other2 = Game_Sprite()
sprites = []
sprites.append(other) 
sprites.append(other2) 
map = Map(player)

timer = pygame.time.Clock()

sprite_group = pygame.sprite.Group()
sprite_group.add(player)
prev_tick = 0

is_running = True

while is_running:
    delta_time = 0.0
    if pygame.event.peek():
        e = pygame.event.poll()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            is_running = False
        if keys[pygame.K_RIGHT]:
            player.move_right(1)
            for o in sprites:
                o.obj_update(1, 0)
        elif keys[pygame.K_LEFT]:
            player.move_right(-1)
            for o in sprites:
                o.obj_update(-1, 0)
        if keys[pygame.K_DOWN]:
            player.move_down(1)
            for o in sprites:
                o.obj_update(0, 1)
        elif keys[pygame.K_UP]:
            player.move_down(-1)
            for o in sprites:
                o.obj_update(0, -1)
    camera = map.Update()
    wnd.fill((0, 0, 0))
    for o in sprites:
        if sprite_group.has(o):
            if o.Get_X() < camera[0] and o.Get_X() > camera[1] + SCREEN_WIDTH:
                sprite_group.remove(o)
        else:
            if o.Get_X() >= map._camera_x and o.Get_X() <= map._camera_x + SCREEN_WIDTH:
                sprite_group.add(o)
    sprite_group.draw(wnd)
    pygame.display.flip()
    delta_time = (pygame.time.get_ticks() - prev_tick) / 1000
    prev_tick = pygame.time.get_ticks()
    