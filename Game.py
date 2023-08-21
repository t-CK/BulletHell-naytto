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
        
    def add_sprite(self, new_sprite) -> None:
        """Lisää spriten groupiin"""
        self._enemy_sprites.append(new_sprite)
        
    def add_ui(self, ui):
        """Lisää uuden UI -elementin peliin"""
        self._ui_list.append(ui) # Lisätään uusi UI -elementti UI-listaan
        self._ui_group.add(ui)   # Lisätään uusi UI -elementti pygamen sprite groupiin
    def update_map(self, x_val, y_val):
        """Päivittää pelin spritet vastaamaan pelaajan uutta sijaintia ikkunassa"""
        for ent in self._enemy_sprites:
            ent.rect.move_ip(x_val, y_val)
        self._camera = self._map.Update()

    def game_loop(self):
        self.add_sprite(enemies.Enemy_Follow(self)) #DEBUG
        while self._is_Running:         
            # Jos peli on käynnissä, ajetaan loopin ensimmäinen if lohko
            if self._state == Game_State.RUNNING:
                # Otetaan vastaan input
                self._input.get_input()
                
                # Päivitetään kamera
                self._camera = self._map.Update()
                
                # Käydään läpi spritet ja renderöidään ainoastaan näkyvissä olevat
                for obj in self._enemy_sprites:
                    # Tarkastetaan x-akseli
                    if self._sprite_group.has(obj):
                        if obj.get_x() < self._camera[0]-self._wnd_size[0]-self._wnd_size[0]/2 or obj.get_x() > self._camera[0] +self._wnd_size[0]:
                            self._sprite_group.remove(obj)
                    # Tarkastetaan y-akseli mikäli x-akselin tarkastus ei ole poistanut spriteä groupista
                    #if self._sprite_group.has(obj):
                    if obj.get_y() > self._camera[1] - self._wnd_size[1] / 2.5:
                        self._sprite_group.remove(obj)
                    else:
                        if obj.get_x() >= self._camera[0] +self._wnd_size[0]*1.35 and obj.get_x() <= self._camera[0]-self._wnd_size[0] and obj.get_y() >= self._camera[1] - self._wnd_size[1] / 2 or obj.get_y() <= self._camera[1] + self._wnd_size[1] / 2:
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
                
                # Päivitetään viholliset
                for enemy in self._enemy_sprites:
                    enemy.update()
                
                # Render ###################
                self._wnd.draw_background()                 # renderöidään taustaväri
                player_group = []                           # Luodaan Playerille oma group renderöintiä varten
                player_group.append(self._player)       
                self._wnd.draw_objects(player_group)        # Renderöidään pelaaja
                
                self._wnd.draw_objects(self._enemy_sprites) # Renderöidään viholliset
                self._wnd.draw_objects(self._ui_group)      # Renderöidään UI
                self._counters.render_counter_ui()          # Renderöidään counterit
                
                self._wnd.end_frame()                       # Vaihdetaan front ja back buferit
                ############################
 
                # Lasketaan delta time ja tallennetaan pygame.get_ticks() palauttama arvo prev_tick muuttujaan
                if self._prev_tick == 0.0:
                    self._delta_time = 0.0
                else:
                    self._delta_time = (time.get_ticks() - self._prev_tick) / 1000
                    
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