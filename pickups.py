import pygame as pg
import misc, weapons
from variables import *

class Xp(pg.sprite.Sprite):
    """ XP globe dying enemies drop """
    # A list of colors according to XP value:
    _colors = [(140, 70, 255), (200, 70, 230), (255, 180, 120), (180, 240, 0), (200, 200, 40), (255, 255, 100)]
    def __init__(self, game, pos_x, pos_y, xp_amount = 1):
        super().__init__()
        self.player = game._player
        self.size = 5 + 3*xp_amount
        self.surf = pg.Surface([self.size, self.size])
        self.xp_amount = xp_amount
        if xp_amount <= len(self._colors):
            self.surf.fill(self._colors[xp_amount-1])
        else:
            self.surf.fill(self._colors[-1])
        self.rect = self.surf.get_rect()
        self.rect.center = (pos_x, pos_y)

        all_sprites.add(self)
        items_group.add(self)

    def update(self):
        """ Check distance to player and if close, call for pickup() """
        if misc.get_distance(self, self.player) < self.player.pickup_distance:
            self.pickup()

    def pickup(self):
        """ Get picked up and increase player XP """
        self.kill()
        self.player.xp += self.xp_amount**2
        if self.player.xp >= self.player.xp_to_next_level:
            self.player.levelup()

class Item(pg.sprite.Sprite):
    """ Parent class for powerups (incomplete) """
    def __init__(self, game, pos_x, pos_y):
        super().__init__()
        self.game = game
        self.surf = pg.Surface([0,0]) # 0,0 for testing for now
        self.rect = self.surf.get_rect()
        self.color = None
        self.rect.center = pos_x, pos_y

        all_sprites.add(self)
        items_group.add(self)

    def update(self):
        """ Draw item, check distance to player, and if close, call for pickup() """
        # TODO: Draw & blit
        if misc.get_distance(self, self.game._player) < self.game._player.pickup_distance:
            self.pickup()

class Item_Decoy(Item):
    """ Decoy item that makes following enemies target itself for [ttl] ticks (incomplete) """
    def __init__(self, game, pos_x, pos_y, ttl = 500, hp = 10):
        super().__init__(game, pos_x, pos_y)
        self.ttl = ttl
        self.hp = hp
        self.invulnerable = 0
        self.active = False

        self.color = (0,0,0) # TODO: Pick a color

    def update(self):
        if not self.active:
            super().update() # To draw & blit powerup, if not yet picked up
        else:
            # TODO: Drawing and blitting something for an active decoy
            if self.ttl >= 0:
                self.ttl -= 1
            if self.ttl == 0:
                # TODO: Set enemy targets back to player
                self.kill()

    def pickup(self):
        """ Set enemy targets to own position """
        pass

class Item_Bombs(Item):
    """ Powerup item that spawns [amount] of explosions on random enemies doing [dmg] damage each """
    def __init__(self, game, pos_x, pos_y, amount = 3, dmg = 2):
        super().__init__(game, pos_x, pos_y)
        self.amount = amount
        self.dmg = dmg

        self.color = (0,0,0) # TODO: Pick a color
        
        # Placeholder "graphics"
        self.surf = pg.Surface([10,10])
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center = (pos_x, pos_y))

    def pickup(self):
        for _ in range(self.amount):
            weapons.Explosion(self.game)
        self.kill()