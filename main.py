import math, random
import pygame as pg
import weapons, enemies, world, pickups, ui, event_queue, misc
from player import Player
from variables import *

from Counter import Counter

pg.init()
SCREEN_SIZE = (WIDTH, HEIGHT) = (1000,800)
SCREEN = pg.display.set_mode(SCREEN_SIZE)

class App():
    def __init__(self):
        self._ticks = 0
        self.screen = SCREEN
        self.spawn_timer = STARTING_SPAWN_TIME
        self.clock = pg.time.Clock()
        self._wnd_size = SCREEN_SIZE
        self.player = self._player = Player(self)
        self.initialize_game()
        self._counters = Counter(self.screen)

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
            self._ticks += 1

    def initialize_level(self):
        """ Initialize level. Just spawn a few random obstacles on screen for now. """
        for _ in range(WIDTH // 10):
            size = (size_x, size_y) = (random.randint(20*SPRITE_SCALE, 100*SPRITE_SCALE),
                                       random.randint(20*SPRITE_SCALE, 100*SPRITE_SCALE))
            position = (pos_x, pos_y) = (random.randint(-600, WIDTH+600), random.randint(-600, HEIGHT+600))
            while abs(pos_x - self.player.rect.centerx) < 50 + size_x and \
                  abs(pos_y - self.player.rect.centery) < 50 + size_y:
                position = (pos_x, pos_y) = (random.randint(-600, WIDTH+600), random.randint(-600, HEIGHT+600))
            world.World(self, *position, *size)

    def spawn_enemies(self):
        """ Spawns enemies at decreasing intervals, starting at STARTING_SPAWN_TIME ticks apart 
        Also spawn bigger waves of increasing size or major enemies every now and then """
        self.spawn_timer -= 1
        if self.spawn_timer == 0:
            _enemy_type = random.choices([enemies.Enemy_Follow, enemies.Enemy_Sine], (0.9, 0.1))
            _stats = (_hp, _speed, _damage) = (3+self._ticks//5000, 1+self._ticks//15000, 1+self._ticks//10000)
            _enemy_type[0](self, misc.get_spawn(), None, *_stats)
            self.spawn_timer = max(10, STARTING_SPAWN_TIME - self._ticks//100)
        
        # Spawn one of 4 "wave types"
        if self._ticks % 1500 == 0:
            _wave_type = random.randrange(4)            
            # Worms
            if _wave_type == 0:
                _wave_size = 1+self._ticks//7000
                for _ in range(_wave_size):
                    _distance_offset = random.randrange(100)
                    enemies.Enemy_Worm_Head(self, misc.get_spawn(None, 100 + _distance_offset))
            # A closely spawning group of Enemy_Follow
            elif _wave_type == 1:
                _wave_size = 1+self._ticks//1500
                _group_center = misc.get_spawn(None, 200)
                for _ in range(_wave_size):
                    _random_x_offset = random.randrange(150)
                    _random_y_offset = random.randrange(150)
                    _position = (_group_center[0] + _random_x_offset, _group_center[1] + _random_y_offset)
                    enemies.Enemy_Follow(self, _position)
            # A closely spawning group of Enemy_Sine
            elif _wave_type == 2:
                _wave_size = 1+self._ticks//2500
                _group_center = misc.get_spawn(None, 300)
                for _ in range(_wave_size):
                    _random_x_offset = random.randrange(250)
                    _random_y_offset = random.randrange(250)
                    _position = (_group_center[0] + _random_x_offset, _group_center[1] + _random_y_offset)
                    enemies.Enemy_Sine(self, _position)
            # Randomly placed Enemy_Sines
            elif _wave_type == 3:
                _wave_size = 1+self._ticks//1500
                for _ in range(_wave_size):
                    _distance_offset = random.randrange(150)
                    enemies.Enemy_Sine(self, misc.get_spawn(None, 150 + _distance_offset))

    def check_collisions(self):
        """ Checks for non-movement related collision.
    
        Checks collision of bullets/enemies and enemies/player and deals damage for now.
        Movement related collision is in each sprite's update() function, and checking
        distance for pickups happens in the pickup's update().
        """
        for sprite in enemy_group:
            if pg.sprite.spritecollideany(sprite, bullet_group):
                sprite.damage(self.player.bullet_damage)
            if pg.sprite.collide_rect_ratio(1.01)(sprite, self.player) and self.player.hp > 0:
                self.player.damage(sprite.dmg)
                sprite.damage()
    
    def render_screen(self):
        """ Fill background, blit sprites and flip() the screen """
        for group in (items_group, world_group, enemy_group, bullet_group):
            for sprite in group:
                SCREEN.blit(sprite.surf, sprite.rect)
        SCREEN.blit(self.player.surf, self.player.rect)
        for sprite in ui_group:
            SCREEN.blit(sprite.surf, sprite.rect)
        pg.display.flip()
        SCREEN.fill((20,20,150))
        
    def add_ui(*args):
        pass
    
if __name__ == "__main__":
    App().main()