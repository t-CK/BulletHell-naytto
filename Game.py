import Log
import Window
import Game_World
import player
import input
from Counter import Counter

from pygame import event
from pygame import key
from pygame import time
from pygame import locals
from pygame import sprite
from pygame import display
from enum import Enum, IntEnum
import random

from variables import *

import misc
import enemies
import world
import ui


# Enum luokka pelin statuksen seuraamista varten
class Game_State(IntEnum):
    RUNNING = 0
    PAUSED = 1
    IN_MENU = 2

class Game:
    # Ainoastaan yksi instanssi pelist� sallitaan kerrallaan, joten Game -luokka voi olla staattinen (Luokan muuttujat tallennetaan suoraan class-variableina)
    _is_Running :bool
    _state :Game_State
    _game_objects = []
    _wnd :Window.Window
    _wnd_size :tuple
    # delta time
    _prev_tick = 0
    _delta_time = 0.0
    _ui_list = []
    _clock = time.Clock()

    def __init__(self) -> None:
        self._wnd = Window.Window()
        self.screen = self._wnd._wnd
        self._state = Game_State.RUNNING
        self._is_Running = True
        # Luodaan array, johon tallennetaan kaikki spritet paitsi pelaaja
        self._enemy_sprites = []
        # Luodaan pelaaja- ja karttaobjektit
        self._wnd_size = self._wnd.get_size()
        self._player = self.player = player.Player(self)
        # Aloitettaessa uusi peli, luodaan counter -objekti default parametreillä
        self._counters = Counter(self._wnd._wnd)
        # TODO: Counterin luonti ladattaessa peli tallennuksesta

        self._input = input.Input(self, self._player)
        self._map = Game_World.Map(self._player)
        # Luodaan camera(tuple) muuttuja, jolle annetaan arvoksi pelaajan X ja Y sijainnit
        self._camera = self._map.Update()
        # Luodaan sprite.Group spritejen renderöintiin
        self._sprite_group = sprite.Group()
        self._sprite_group.add(self._player)
        self._ui_group = sprite.Group()

        self._spawn_timer = STARTING_SPAWN_TIME
        self._ticks = 0
        self.initialize_level()
        ui.Ui_Bar_XP(self)
        ui.Ui_Bar_Health(self)

    def add_sprite(self, new_sprite) -> None:
        """Lisää spriten groupiin"""
        self._enemy_sprites.append(new_sprite)

    def add_ui(self, ui):
        """Lisää uuden UI -elementin peliin"""
        self._ui_list.append(ui) # Lisätään uusi UI -elementti UI-listaan
        self._ui_group.add(ui)   # Lisätään uusi UI -elementti pygamen sprite groupiin
    def update_map(self, x_val, y_val):
        """Päivittää pelin spritet vastaamaan pelaajan uutta sijaintia ikkunassa"""
        for ent in all_sprites:
            ent.rect.move_ip(x_val, y_val)
        self._camera = self._map.Update()

    def game_loop(self):
        while self._is_Running:
            self._clock.tick(60)
            # Jos peli on käynnissä, ajetaan loopin ensimmäinen if lohko
            if self._state == Game_State.RUNNING:
                self._ticks += 1
                # Otetaan vastaan input
                self._input.get_input()

                # Päivitetään kamera
                self._camera = self._map.Update()

                # Käydään läpi spritet ja renderöidään ainoastaan näkyvissä olevat
                for obj in all_sprites:
                # Tarkastetaan onko sprite ruudulla, ja poistetaan groupista jos ei...
                    if obj.rect.centerx < -obj.rect.width/2 or obj.rect.centerx > self._wnd_size[0] + obj.rect.width/2 or \
                       obj.rect.centery < -obj.rect.height/2 or obj.rect.centery > self._wnd_size[1] + obj.rect.height/2:
                        self._sprite_group.remove(obj)
                    else: # ...ja lisätään jos on.
                        self._sprite_group.add(obj)

            # Jos game_state on PAUSE, asetetaan prev_tick arvoksi 0, tarkastetaan onko escape näppäintä painettu pausen lopettamiseksi
            # ja hypätään loopin alkuun
            elif self._state == Game_State.PAUSED:
                self._delta_time = 0.0
                if event.peek():
                    keys = key.get_pressed()
                    e = event.poll()
                    if keys[locals.K_ESCAPE]:
                        self._state = Game_State.RUNNING
                Log.Log_Info("PAUSED")
            # Renderöidään menu tarvittaessa
            elif self._state == Game_State.IN_MENU:
                pass

            # Renderöidään peliobjektit/valikot
            if self._state == Game_State.RUNNING:

                # Spawnataan viholliset
                self.spawn_enemies()

                # Päivitetään spritet
                all_sprites.update()
                self._player.update()
                ui_group.update()
                
                # Damage vihollisille & pelaajalle
                self.check_collisions()

                # Render ###################

                for group in (items_group, world_group, enemy_group,
                             bullet_group, [self._player], self._ui_group):
                    self._wnd.draw_objects(group)


                # Lasketaan delta time ja tallennetaan pygame.get_ticks() palauttama arvo prev_tick muuttujaan
                if self._prev_tick == 0.0:
                    self._delta_time = 0.0
                else:
                    self._delta_time = (time.get_ticks() - self._prev_tick) / 1000
                    
                self._counters.timer_update(self._delta_time)
                self._counters.render_counter_ui()
                self._wnd.end_frame()                       # Vaihdetaan front ja back buferit
                self._wnd.draw_background()                 # renderöidään taustaväri

                ############################
            self._prev_tick = time.get_ticks()


    def toggle_state(self, state :Game_State):
        if self._state == state:
            if state == Game_State.PAUSED:
                self._state = Game_State.RUNNING
        else: self._state = state

    def get_state(self) -> Game_State:
        return self._state

    def get_delta_time(self) -> float:
        return self._delta_time

    def spawn_enemies(self):
        """ Spawns enemies at decreasing intervals, starting at STARTING_SPAWN_TIME ticks apart 
        Also spawn bigger waves of increasing size or major enemies every now and then """
        self._spawn_timer -= 1
        if self._spawn_timer == 0:
            _enemy_type = random.choices([enemies.Enemy_Follow, enemies.Enemy_Sine], (0.9, 0.1))
            _stats = (_hp, _speed, _damage) = (3+self._ticks//5000, 1+self._ticks//15000, 1+self._ticks//10000)
            _enemy_type[0](self, misc.get_spawn(), None, *_stats)
            self._spawn_timer = max(10, STARTING_SPAWN_TIME - self._ticks//100)

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

    def initialize_level(self):
        """ Initialize level. Just spawn a few random obstacles on screen for now. """
        for _ in range(self._wnd_size[0] // 10):
            size = (size_x, size_y) = (random.randint(20*SPRITE_SCALE, 100*SPRITE_SCALE),
                                       random.randint(20*SPRITE_SCALE, 100*SPRITE_SCALE))
            position = (pos_x, pos_y) = (random.randint(-600, self._wnd_size[0]+600), random.randint(-600, self._wnd_size[1]+600))
            while abs(pos_x - self._player.rect.centerx) < 50 + size_x and \
                  abs(pos_y - self._player.rect.centery) < 50 + size_y:
                position = (pos_x, pos_y) = (random.randint(-600, self._wnd_size[0]+600), random.randint(-600, self._wnd_size[1]+600))
            world.World(self, *position, *size)
            
    def check_collisions(self):
        """ Checks for non-movement related collision.
    
        Checks collision of bullets/enemies and enemies/player and deals damage for now.
        Movement related collision is in each sprite's update() function, and checking
        distance for pickups happens in the pickup's update().
        """
        for s in enemy_group:
            if sprite.spritecollideany(s, bullet_group):
                s.damage()
            if sprite.collide_rect_ratio(1.01)(s, self._player) and self._player.hp > 0:
                self._player.damage(s.dmg)
                s.damage()

if __name__ == "__main__":
    game=Game()
    game.game_loop()