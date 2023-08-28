import pygame
from sys import exit
import menu_test_9


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
        


class Button:
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
                        main_menu = menu_test_9.Menu()
                        main_menu.menu_loop()
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

        







# Conditional statement that checks if the current script is being
# run as the main program.
if __name__ == "__main__":
    # Creating the object and running the loop
    button = Button()
    button.button_loop()

