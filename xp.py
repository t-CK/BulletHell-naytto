import pygame as pg

class Xp(pg.sprite.Sprite):
    """ XP globe dying enemies drop """
    # Testinä huvin vuoks lista väreistä xp-arvon mukaan:
    _colors = [(140, 70, 255), (200, 70, 230), (255, 180, 120), (180, 240, 0), (200, 200, 40), (255, 255, 100)]
    def __init__(self, pos_x, pos_y, xp_amount = 1):
        super().__init__()
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

    def update(self):
        """ Check distance to player and if close, call for pickup() """
        if get_distance(self, player) < player.pickup_distance:
            self.pickup()

    def pickup(self):
        """ Get picked up and increase player XP """
        self.kill()
        player.xp += self.xp_amount
        if player.xp >= player.xp_to_next_level:
            player.levelup()