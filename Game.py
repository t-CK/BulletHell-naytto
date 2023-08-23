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
        self._state = Game_State.RUNNING
        self._is_Running = True
        # Luodaan array, johon tallennetaan kaikki spritet paitsi pelaaja
        self._enemy_sprites = []
        # Luodaan pelaaja- ja karttaobjektit
        self._wnd_size = self._wnd.get_size()
        self._player = player.Player(self._wnd_size)
        # Aloitettaessa uusi peli, luodaan counter -objekti default parametreillä
        self._counters = Counter(self._wnd)
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
        self.add_sprite(enemies.Enemy_Follow(self)) #DEBUG
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

                # Render ###################

                for group in (items_group, world_group, self._enemy_sprites,
                             bullet_group, [self._player], self._ui_group):
                    self._wnd.draw_objects(group)

                self._wnd.end_frame()                       # Vaihdetaan front ja back buferit
                self._wnd.draw_background()                 # renderöidään taustaväri
                ############################

                # Lasketaan delta time ja tallennetaan pygame.get_ticks() palauttama arvo prev_tick muuttujaan
                if self._prev_tick == 0.0:
                    self._delta_time = 0.0
                else:
                    self._delta_time = (time.get_ticks() - self._prev_tick) / 1000
                self._counters.timer_update(self._delta_time)
                self._counters.render_counter_ui()

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
        """ Spawns enemies at decreasing intervals, starting at STARTING_SPAWN_TIME ticks apart """
        self._spawn_timer -= 1
        if self._spawn_timer == 0:
            enemies.Enemy_Follow(self)
            self._spawn_timer = max(10, STARTING_SPAWN_TIME - self._ticks//100)

    def initialize_level(self):
        """ Initialize level. Just spawn a few random obstacles on screen for now. """
        for _ in range(self._wnd_size[0] // 150):
            size = (size_x, size_y) = (random.randint(20*SPRITE_SCALE, 100*SPRITE_SCALE),
                                       random.randint(20*SPRITE_SCALE, 100*SPRITE_SCALE))
            position = (pos_x, pos_y) = (random.randint(0, self._wnd_size[0]), random.randint(0, self._wnd_size[1]))
            while abs(pos_x - self._player.rect.centerx) < 50 + size_x and abs(pos_y - self._player.rect.centery) < 50 + size_y:
                position = (pos_x, pos_y) = (random.randint(0, self._wnd_size[0]), random.randint(0, self._wnd_size[1]))
            world.World(*position, *size)

if __name__ == "__main__":
    game=Game()
    game.game_loop()