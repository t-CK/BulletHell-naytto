import Log
import Window
import Game_World
import Player
import input
from Counter import Counter

from pygame import event
from pygame import key
from pygame import time
from pygame import locals
from pygame import sprite
from pygame import display
from enum import Enum, IntEnum

from variables import *

import enemies


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


    def __init__(self) -> None:
        self._wnd = Window.Window()
        self._state = Game_State.RUNNING
        self._is_Running = True
        # Luodaan array, johon tallennetaan kaikki spritet paitsi pelaaja
        self._non_player_sprites = []
        # Luodaan pelaaja- ja karttaobjektit
        self._wnd_size = self._wnd.get_size()
        self._player = Player.Player(self._wnd_size)
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
        
    def add_sprite(self, new_sprite) -> None:
        """Lisää spriten groupiin"""
        self._non_player_sprites.append(new_sprite)
        
    def add_ui(self, ui):
        """Lisää uuden UI -elementin peliin"""
        self._ui_list.append(ui) # Lisätään uusi UI -elementti UI-listaan
        self._ui_group.add(ui)   # Lisätään uusi UI -elementti pygamen sprite groupiin
    def update_game(self, x_val, y_val):
        """Päivittää pelin spritet vastaamaan pelaajan uutta sijaintia ikkunassa"""
        for ent in self._non_player_sprites:
            ent.obj_update(x_val, y_val)
        self._camera = self._map.Update()

    def game_loop(self):
        self.add_sprite(enemies.Enemy(self,(100,100))) #DEBUG
        while self._is_Running:         
            # Jos peli on käynnissä, ajetaan loopin ensimmäinen if lohko
            if self._state == Game_State.RUNNING:
                # Otetaan vastaan input
                self._input.get_input()
                
                # Päivitetään kamera
                self._camera = self._map.Update()
                
                # Käydään läpi spritet ja renderöidään ainoastaan näkyvissä olevat
                for obj in self._non_player_sprites:
                    if self._sprite_group.has(obj):
                        if obj.get_x() < self._camera[0]-self._wnd_size[0]-self._wnd_size[0]/2 or obj.get_x() > self._camera[0] +self._wnd_size[0]:
                            self._sprite_group.remove(obj)
                    else:
                        if obj.get_x() >= self._camera[0] -self._wnd_size[0]*1.35 and obj.get_x() <= self._camera[0]+self._wnd_size[0]:
                            self._sprite_group.add(obj)
                            
                # Päivitetään peliobjektit
                

            # Jos game_state on PAUSE, asetetaan prev_tick arvoksi 0, tarkastetaan onko escape näppäintä painettu pausen lopettamiseksi
            # ja hypätään loopin alkuun
            elif self._state == Game_State.PAUSED:
                if event.peek():
                    keys = key.get_pressed()
                    e = event.poll()
                    if keys[locals.K_ESCAPE]:
                        self._state = Game_State.RUNNING
                Log.Log_Info("PAUSED")
            # Renderöidään menu tarvittaessa
            elif self._state == Game_State.IN_MENU:
                pass
            # Tyhjennetään ikkunan sisältö ja renderöidään taustaväri
            self._wnd.draw_background()
            # Renderöidään peliobjektit/valikot
            if self._state == Game_State.RUNNING:
                for sprite in self._sprite_group:

                    # DEBUG
                    try:
                        sprite.debug_print()
                        # DEBUG
                        Log.Log_Error(f"Camera {self._camera}")
                        Log.Log_Warning(f"Enemy {sprite.get_x()} : {sprite.get_y()}")
                    except:
                        pass

                    self._wnd._wnd.blit(sprite.surf, sprite.rect)
                for sprite in self._ui_group:
                    self._wnd._wnd.blit(sprite.surf, sprite.rect)
                display.flip()
                
 #               self._wnd.draw_objects(self._sprite_group)
                # Lasketaan delta time ja tallennetaan pygame.get_ticks() palauttama arvo prev_tick muuttujaan
                if self._prev_tick == 0.0:
                    self._prev_tick = time.get_ticks()
                else:
                    self._delta_time = (time.get_ticks() - self._prev_tick) / 1000
                    self._prev_tick = time.get_ticks()
            elif self._state == Game_State.PAUSED:
                # Valikon renderöinti
                # Tarkastetaan käyttäjän syöte
                self._input.get_input()
                # Asetetaan delta_time arvoksi 0 ja päivitetään self._prev_tick
                self._delta_time = 0.0
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
    


if __name__ == "__main__":
    game=Game()
    game.game_loop()