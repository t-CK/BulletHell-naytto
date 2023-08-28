import Log
import Window
import Game_World
import player
import input
from Counter import Counter

import pygame
from sys import exit

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




'''
The whole purpose of this file is to create an athmospheric and inviting user
experience before starting to play the game.

To enhance this experience, graphics and audio have been made just to keep in mind
the game design.

The user has to choose between three different buttons:
- play
- options
- quit

The Play button will take the user to the test game enviroment.
The Options button will take the user to the Options menu. The Options menu is an external file
where there is more info about its usability.
The Quit button will exit the main menu while loop, quit pygame module and system exit. When all of these
are called, the program is succesfully closed.
'''

'''MAIN MENU BELOW '''

class Menu:
    #-----------------------------
    '''Main class where events and loop are managed. '''
    #-----------------------------
    def __init__(self):
        pygame.init() # initialize pygame
        self.screen_width = 640 # define size of screen width
        self.screen_height = 480 # # define size of screen height
        self.screen = pygame.display.set_mode((self.screen_width,
                                               self.screen_height)) # define window and its values
        pygame.display.set_caption('Menu') # set title name for window
        self.clock = pygame.time.Clock() # initialize pygame clock. It manages FPS(frames per second)
        self.running = True # boolean value for main game loop
        self.font = pygame.font.SysFont(None, 36) # font object for rendering text. Using default system font
        # create an instance of class and assigning attributes
        self.audio = Audio(self.screen)
        self.button = Button(self.screen, self.screen_width, self.screen_height)
        self.rainMain = RainMain(self.screen,self.screen_width, self.screen_height)
        # define colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)


    def handle_events(self):
        '''manage events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                # if press 'x' on window or ESCAPE button it will quit while loop,
                # quit pygame module, and system exit
                self.running = False
                pygame.quit()
                exit()
                # - In menu: When button is clicked...
                # play the game, options or quit the game
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                
                if self.button.sprite1.rect.collidepoint(pos):
                    print('Play button was clicked!')
                    pygame.mixer.music.stop() # stop menu music when pressing play button
                    start_game = Game()
                    start_game.game_loop()
                    
                if self.button.sprite2.rect.collidepoint(pos):
                    # navigate to external options file
                    print('Options button was clicked!')
                    choose_options = OptionsButton()
                    choose_options.button_loop()
                    
                if self.button.sprite3.rect.collidepoint(pos):
                    # stop while loop, quit pygame and system exit
                    print('Quit button was clicked!')   
                    self.running = False
                    pygame.quit()
                    exit()

                    
 
    def menu_loop(self):
        ''' main loop '''
        self.audio.play_audio() # plays audio in menu
        # before there is pause, stopping or other
        # functionalies audio can stay ouside while loop
        
        while self.running:
            
            self.screen.fill(self.BLACK) # fills entire screen with spesific color
            self.handle_events() # managing events 
            self.rainMain.draw_raindrop() # calling 'rainmaker' class
            self.button.draw_buttons() # drawing all menu buttons and title
            self.clock.tick(60) # limit frame rate to given number per second
            pygame.display.update() # updates screen

        pygame.quit()
        exit()


class InheritSprite(pygame.sprite.Sprite):
    #-----------------------------
    '''inheriting & initializing pygame sprite'''
    #-----------------------------
    def __init__(self, image, x, y, button_text):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.button_text = button_text


class Button:
    #-----------------------------
    '''Creating buttons and menu title'''
    #-----------------------------
    def __init__(self, screen, screen_width, screen_height):

        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        
        # colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # images
        self.image1 = pygame.image.load("./ui_images/main_menu_img/button_200x50_play.png")
        self.image2 = pygame.image.load("./ui_images/main_menu_img/button_200x50_options.png")
        self.image3 = pygame.image.load("./ui_images/main_menu_img/button_200x50_quit.png")
        self.image4 = pygame.image.load("./ui_images/main_menu_img/menu_title_400x100.png")



        # sprite instances
        self.x_width = self.screen_width // 3
        self.y_height = self.screen_height // 3
        self.sprite1 = InheritSprite(self.image1,self.x_width , self.y_height, "Clicked play button!")
        self.sprite2 = InheritSprite(self.image2, self.x_width, self.y_height + 75, "Clicked options button!")
        self.sprite3 = InheritSprite(self.image3, self.x_width, self.y_height + 150, "Clicked quit button!")
        self.sprite4 = InheritSprite(self.image4, self.screen_width//7, self.screen_height // 25, "Clicked title!")

        
        # sprite group variable 
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.sprite1, self.sprite2, self.sprite3, self.sprite4)



    def draw_buttons(self):
        
        self.all_sprites.draw(self.screen)


class RainMain:
    #-----------------------------
    '''Access and draw rain effect'''
    #-----------------------------
    def __init__(self,screen,screen_width, screen_height):

        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clock = pygame.time.Clock()

        
        # define colors
        self.BLACK = (0,0,0)
        self.WHITE = (255, 255, 255)


        
        # sprite group
        self.all_sprites = pygame.sprite.Group()# assigning sprites container to a variable
        for _ in range(100):
            self.raindrop = Raindrop(self.screen_width, self.screen_height) # create variable out Raindrop class
            self.all_sprites.add(self.raindrop) # adds all individual sprites to a group
            # this will make easier to manage multiple sprites simultaneously

                
    def draw_raindrop(self):
        
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            
            

class Raindrop(pygame.sprite.Sprite): # inherit sprite class from pygame library
    #-----------------------------
    '''Creates a rain effect'''
    #-----------------------------
    def __init__(self, screen_width, screen_height):
        super().__init__() # initializing sprite stuff so it is usable
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # define color
        self.WHITE = (255, 255, 255)
        self.BLACK = (0 ,0, 0)
        self.BLUE = (0, 0, 255)
        
        # raindrop image
        self.image = pygame.Surface((1,10)) # change raindrop size from here
        self.image.fill(self.WHITE) # change color of raindrop
        
        # rect
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.screen_width)
        self.rect.y = random.randint(-self.screen_height, 0)

        
        # speed
        self.speed = random.randint(5,10) # falling down momentum speed


    def update(self):
        self.rect.y += self.speed
        # keep it raining after the rain goes out of the screen
        if self.rect.y > self.screen_height:
            self.rect.x = random.randint(0, self.screen_width)
            self.rect.y = random.randint(-self.screen_height, 0)

        

class Audio:
    #-----------------------------
    '''Play menu background music'''
    #-----------------------------
    def __init__(self, screen):
        self.screen = screen


    def play_audio(self):
        try:
            pygame.mixer.init() 
            pygame.mixer.music.load("./music_and_audio/menu_music/rain_mix_3_edit.mp3")
            pygame.mixer.music.play(-1) # -1 gives infinite loop
        except:
            print("Failed to load audio file.")




"""
The size of the options screen is approximately half the size of the
main menu screen. As a game design perspective in pygame's world, it is a
good way to caught the users' attention.

The resolution options button, the toggle auto attack button,
and the toggle mouse movementare ready but their usability is
under construction.We wanted to focus on the more
important parts of the game and prioritize those first.

The auto attack button has a toggle on and off, where the user can switch between
auto attack on / auto attack off. By default, the auto attack is toggled
off, indicated by a red color. If the user wants to toggle it on,
they slide it to the right and the color changes to green.
If it is turned on, the character will automatically
attack with its weapons. In other words: the player only has to move and aim
but the weapons are continuously shooting.

The mouse movement has a toggle on and off, where the user can switch between
mouse movement on / mouse movement off. By default, the mouse movement is toggled
off, indicated by a red color. If the user wants to toggle it on,
they slide it to the right and the color changes to green.
If it is turned on, the character will move
with the mouse instead of using the keyboard directions.
Therefore the use of the keyboard for movement does not work.
"""


''' OPTIONS BUTTON BELOW '''


class InheritSprite(pygame.sprite.Sprite):
    #-----------------------------
    '''inheriting & initializing pygame sprite'''
    #-----------------------------
    def __init__(self, image, x, y, button_text):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.button_text = button_text

class OnOffButton:
    def __init__(self, screen, x, y, width, height, text):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (150, 150, 150)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.TRANSPARENT = (0,0,0,0)
        self.REDISH= (181,3,3)
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.is_on = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.ellipse_rect = pygame.Rect(x + 10, y + 10, self.width -20,
                                        self.height - 20)
        self.circle_rect = pygame.Rect(x + 10, y + 10, self.height -20,
                                       self.height - 20)



    
    def on_off_event(self):
        # toggle on/off
        self.is_on = not self.is_on

    def draw(self, screen):
        ''''''
        self.color = self.GREEN if self.is_on else self.RED # toggle ellipse color
        pygame.draw.rect(self.screen, self.REDISH, self.rect, width=1)# ellipse toggle button is surrounded by rectangle
        pygame.draw.ellipse(self.screen, self.color, self.ellipse_rect, width=0)
        if self.is_on:
            self.circle_rect.x = self.rect.right - self.ellipse_rect.height - 8 # circle object is placed on right side of ellipse
        else:
            self.circle_rect.x = self.rect.left + 10 # adjusting slightly the position of circle
        pygame.draw.circle(self.screen, self.WHITE, self.circle_rect.center,
                            self.circle_rect.width // 2)
        


class OptionsButton:
    def __init__(self):
        pygame.init()

        self.screen_width, self.screen_height = 640 // 2, 480 // 1.5
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.x_width = self.screen_width // 5
        self.y_height = self.screen_height // 5
        self.toggle_button = OnOffButton(self.screen, self.x_width+120, self.y_height + 63,
                                         75, 35, "ON/OFF") 
        self.toggle_button2 = OnOffButton(self.screen, self.x_width+120, self.y_height + 123,
                                         75, 35, "ON/OFF")
        self.toggle_button.is_on # access boolean value to use in manage_event
        self.toggle_button2.is_on
        self.x_width = self.screen_width // 5 # sprite values
        self.y_height = self.screen_height // 5 # sprite values



        
        # colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (150, 150, 150)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        '''The image and the sprite variables don't have good description because we want them to be easily editable.
        For example mouse_movement and auto_attack position can be easily switched between.'''

        # images
        self.image1 = pygame.image.load("./ui_images/options_img/button_200x50_resolution.png")
        self.image2 = pygame.image.load("./ui_images/options_img/button_200x50_auto_attack.png")
        self.image3 = pygame.image.load("./ui_images/options_img/button_200x50_mouse_movement.png")
        self.image4 = pygame.image.load("./ui_images/options_img/button_200x50_return.png")

        # sprite instances

        self.sprite1 = InheritSprite(self.image1,self.x_width , self.y_height, "Clicked resolution button!")
        self.sprite2 = InheritSprite(self.image2, self.x_width, self.y_height + 60, "")
        self.sprite3 = InheritSprite(self.image3, self.x_width, self.y_height + 120, "")
        self.sprite4 = InheritSprite(self.image4, self.x_width, self.y_height + 180, "Clicked return game!")

        
        # sprite group variable 
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.sprite1, self.sprite2, self.sprite3, self.sprite4)


    def manage_event(self):
        # handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # left mouse button 
                    pos = pygame.mouse.get_pos()
                    if self.sprite1.rect.collidepoint(pos):
                        print(self.sprite1.button_text) # resolution 
                    if self.sprite4.rect.collidepoint(pos):
                        print(self.sprite4.button_text) # return menu
                        return_menu = Menu()
                        return_menu.menu_loop()    
                    if self.toggle_button.rect.collidepoint(pos):
                        self.toggle_button.on_off_event() # toggle button on/off
                        print("Auto attack on/off")
                    if self.toggle_button2.rect.collidepoint(pos):
                        self.toggle_button2.on_off_event()
                        print("Mouse movement on/off")

                        

    def draw_button(self):
        
        self.screen.fill(self.BLACK)
        self.all_sprites.draw(self.screen)
        self.toggle_button.draw(self.screen) # auto attack toggle button
        self.toggle_button2.draw(self.screen) # mouse movement toggle button
        pygame.display.flip()
        self.clock.tick(60)
            


    def button_loop(self):

        while self.running:
            
            self.manage_event()
            self.draw_button()
            

            
        pygame.quit()
        exit()




if __name__ == "__main__":
    # Creating the object and running the loop
    menu = Menu()
    menu.menu_loop()
