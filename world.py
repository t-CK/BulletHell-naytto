import pygame as pg
from misc import get_spawn
from variables import *

class World(pg.sprite.Sprite):
    """ World object such as an obstacle or a special area of the level

    [pos_x] and [pos_y] are coordinates for the top left corner, sizes are the
    sides down and right from that point. If [solid] is True, will be impassable.
    """
    def __init__(self, game, pos_x, pos_y, size_x, size_y, solid = True):
        super().__init__()
        self.game = game
        self.surf = pg.Surface([size_x, size_y])
        self.surf.fill((200,30,30))
        self.rect = self.surf.get_rect()
        self.solid = solid

        self.rect.topleft = (pos_x, pos_y)

        all_sprites.add(self)
        world_group.add(self)
        
        if self.solid:
            collideable.add(self)
            
    def update(self):
        """ If out of screen by 700 pixels, respawn somewhere on the other side of the screen
        
        Very crude and quick, more of a simulation of level generation than actual, meaningful level generation
        """
        # if not (-700 < self.rect.centerx < self.game._wnd_size[0]+700 or \
                # -700 < self.rect.centery < self.game._wnd_size[1]+700):
        side = None
        if self.rect.centery > self.game._wnd_size[1]+700:
            side = 0
        elif self.rect.centerx < -700:
            side = 1
        elif self.rect.centery < -700:
            side = 2
        elif self.rect.centerx > self.game._wnd_size[0]+700:
            side = 3

        if side is not None:
            World(self.game, *get_spawn(side, 500), *self.rect.size)
            self.kill()