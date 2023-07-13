import pygame
from random import randint
from pygame.sprite import *
import input

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


class Game:
    def __init__(self) -> None:
        pygame.init()
        flags =  pygame.DOUBLEBUF | pygame.HWACCEL | pygame.SHOWN
        self.wnd = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=flags)
        pygame.key.set_repeat(10, 0)

        self.player = Player()
        other = Game_Sprite()
        other2 = Game_Sprite()
        self.sprites = []
        self.sprites.append(other) 
        self.sprites.append(other2) 
        self.map = Map(self.player)
        self._input = input.Input(self.player, self)

        self.timer = pygame.time.Clock()

        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(self.player)
        self.prev_tick = 0
        
        self.camera = self.map.Update()

        self.is_running = True
        
    def update_game(self, x :float, y :float):
        """Päivittää pelin spritet map scrollingia varten"""
        if x != 0:
            for s in self.sprites:
                s.obj_update(x * -1, 0)
        if y != 0:
            for s in self.sprites:
                s.obj_update(0, y * -1)

    def Game_Loop(self):
        while self.is_running:
            self._input.get_input()
            self.camera = self.map.Update()
            self.wnd.fill((0, 0, 0))
            for o in self.sprites:
                if self.sprite_group.has(o):
                    if o.Get_X() < self.camera[0] and o.Get_X() > self.camera[1] + SCREEN_WIDTH:
                        self.sprite_group.remove(o)
                else:
                    if o.Get_X() >= self.map._camera_x and o.Get_X() <= self.map._camera_x + SCREEN_WIDTH:
                        self.sprite_group.add(o)
            self.sprite_group.draw(self.wnd)
            pygame.display.flip()
            self.delta_time = (pygame.time.get_ticks() - self.prev_tick) / 1000
            self.prev_tick = pygame.time.get_ticks()

if __name__ == "__main__":
    game = Game()
    game.Game_Loop()