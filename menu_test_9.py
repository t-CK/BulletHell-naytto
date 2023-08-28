import pygame # imports a pygame module
import main
from sys import exit # from system module import exit so we can succesfully exit pygame
import options_8 # importing options screen 
import random # import random module



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
                    start_game = main.App()
                    start_game.main()
##                    start_game = game_test_8.Game() # test file
##                    start_game.game_loop() # starting test file
                    
                if self.button.sprite2.rect.collidepoint(pos):
                    # navigate to external options file
                    print('Options button was clicked!')
                    options_menu = options_8.Button()
                    options_menu.button_loop()
                    
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
            

# Conditional statement that checks if the current script is being
# run as the main program.
if __name__ == "__main__":
    # Creating the object and running the loop
    menu = Menu()
    menu.menu_loop()









    
    
        
        
