import math, random
import pygame as pg
import weapons, enemies, world, pickups, ui, event_queue, misc
from player import Player
from variables import *

pg.init()
SCREEN_SIZE = (WIDTH, HEIGHT) = (1000,800)
SCREEN = pg.display.set_mode(SCREEN_SIZE)

class App():
    def __init__(self):
        self.ticks = 0
        self.player = self._player = Player((0,0))
        self._wnd_size = SCREEN_SIZE
        self.initialize_game()
        self.spawn_timer = STARTING_SPAWN_TIME
        self.clock = pg.time.Clock()

    def initialize_game(self):
        """ Initialize player, Ui etc. """
        self.player.rect.center = (WIDTH//2, HEIGHT//2)
        ui.Ui_Bar_XP(self)
        ui.Ui_Bar_Health(self)
        self.initialize_level()
    
    def main(self):
        """ Main loop """
        while True:
            event_queue.process_event_queue(self)
            self.spawn_enemies()
            self.player.update()
            all_sprites.update()
            ui_group.update()
            self.check_collisions()
            self.render_screen()
            self.clock.tick(FPS)
            self.ticks += 1

    def initialize_level(self):
        """ Initialize level. Just spawn a few random obstacles on screen for now. """
        for _ in range(WIDTH // 150):
            size = (size_x, size_y) = (random.randint(20*SPRITE_SCALE, 100*SPRITE_SCALE),
                                       random.randint(20*SPRITE_SCALE, 100*SPRITE_SCALE))
            position = (pos_x, pos_y) = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
            while abs(pos_x - self.player.rect.centerx) < 50 + size_x and abs(pos_y - self.player.rect.centery) < 50 + size_y:
                position = (pos_x, pos_y) = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
            world.World(*position, *size)

    def spawn_enemies(self):
        """ Spawns enemies at decreasing intervals, starting at STARTING_SPAWN_TIME ticks apart """
        self.spawn_timer -= 1
        if self.spawn_timer == 0:
            enemies.Enemy_Follow(self, misc.get_spawn())
            self.spawn_timer = max(10, STARTING_SPAWN_TIME - self.ticks//100)

    def check_collisions(self):
        """ Checks for non-movement related collision.
    
        Checks collision of bullets/enemies and enemies/player and deals damage for now.
        Movement related collision is in each sprite's update() function, and checking
        distance for pickups happens in the pickup's update().
        """
        for sprite in enemy_group:
            if pg.sprite.spritecollideany(sprite, bullet_group):
                sprite.damage()
            if pg.sprite.collide_rect_ratio(1.01)(sprite, self.player) and self.player.hp > 0:
                self.player.damage(sprite.dmg)
                sprite.damage()
    
    def render_screen(self):
        """ Fill background, blit sprites and flip() the screen """
        SCREEN.fill((20,20,150))
        for group in (items_group, world_group, enemy_group, bullet_group):
            for sprite in group:
                SCREEN.blit(sprite.surf, sprite.rect)
        SCREEN.blit(self.player.surf, self.player.rect)
        for sprite in ui_group:
            SCREEN.blit(sprite.surf, sprite.rect)
        pg.display.flip()
        
    def add_ui(*args):
        pass
    
if __name__ == "__main__":
    App().main()