class World(pg.sprite.Sprite):
    """ World object such as an obstacle or a special area of the level

    [pos_x] and [pos_y] are coordinates for the top left corner, sizes are the
    sides down and right from that point. If [solid] is True, will be impassable.
    """
    def __init__(self, pos_x, pos_y, size_x, size_y, solid = True):
        super().__init__()
        self.surf = pg.Surface([size_x, size_y])
        self.surf.fill((200,30,30))
        self.rect = self.surf.get_rect()
        self.solid = solid

        self.rect.topleft = (pos_x, pos_y)

        all_sprites.add(self)
        if self.solid:
            collideable.add(self)