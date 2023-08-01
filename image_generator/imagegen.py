import pygame as pg
from os import listdir
from pathlib import Path

heads = []
bodies = []
legs = []

pg.init()

working_directory = Path().absolute() if not __name__ == "__main__" else Path().absolute().parent

class Head():
    """ Class for heads, self.image : pygame.Surface, self.name : str = filename (w/o extension) """
    def __init__(self, image_filepath):
        self.image = pg.image.load(f"{working_directory}\\{image_filepath}")#.convert()
        self.image.set_colorkey((0,255,0))
        self.name = image_filepath.split("\\")[-1].split(".")[0]
        heads.append(self)
        
class Body():
    """ Class for bodies, self.image : pygame.Surface, self.name : str = filename (w/o extension) """
    def __init__(self, image_filepath):
        self.image = pg.image.load(f"{working_directory}\\{image_filepath}")#.convert()
        self.image.set_colorkey((0,255,0))
        self.name = image_filepath.split("\\")[-1].split(".")[0]
        bodies.append(self)

class Leg():
    """ Class for legs, with walking animation
    
    Attributes:
        image : pygame.Surface
            Image for the sprite standing still
        name : str
            Name of the directory of frames
        animation : Generator
            Indefinitely looping generator so that next(self.animation) returns next frame
        animation_length : int
            Number of frames in walk animation
    """
    def __init__(self, image_filedir, sequence = None):
        """ Sequence is an iterable of file indexes from which to form walk animation """
        files = listdir(f"{working_directory}{image_filedir}")
        self.image = pg.image.load(f"{working_directory}\\{image_filedir}\\{files[0]}")#.convert()
        self.image.set_colorkey((0,255,0))
        self.animation_length = len(sequence) if sequence else len(files)-1
        if self.animation_length == 0:
            self.animation = None
        else:
            self.animation = get_anim_generator(image_filedir, files, sequence)
        self.name = image_filedir.split("\\")[-1]
        legs.append(self)


def get_anim_generator(path: str, filelist: list, sequence = None):
    """ Returns a looping Generator of animation frames 
    
    The filelist parameter can be an iterable of filenames in path or an iterable 
    of Pygame Surfaces. In the latter case, path doesn't matter.
    
    Sequence is an iterable of file indexes for the order of frames from which to form animation.
    If sequence is omitted, images from index 1 forward are used (as index 0 is presumed 
    to be the non-walking Sprite image)
    """
    animation_frames = []
    if not sequence:
        sequence = tuple(range(1, len(filelist)))
    for f in filelist:
        if type(f) == str:
            frame = pg.image.load(f"{working_directory}\\{path}\\{f}")#.convert()
        else:
            frame = f
        frame.set_colorkey((0, 255, 0))
        animation_frames.append(frame)
    while True:
        for n in sequence:
            yield animation_frames[n]
            
def get_sprite_by_names(head, body, leg) -> (pg.image, list):
    """ Returns a tuple of (Sprite standing still, Generator for walk animation)
        from the parts' name attributes """
    correct_head: Head
    correct_body: Body
    correct_leg: Leg
    for h in heads:
        if h.name == head:
            correct_head = h
    for b in bodies:
        if b.name == body:
            correct_body = b
    for l in legs:
        if l.name == leg:
            correct_leg = l
    return combine_sprite(correct_head, correct_body, correct_leg)

def combine_sprite(head, body, leg) -> (pg.image, list):
    """ Returns a tuple of (Sprite standing still, Generator for walk animation) """
    animation = []
    still_image = pg.Surface.copy(body.image)
    still_image.blit(head.image, (0, 0))
    still_image.blit(leg.image, (0, still_image.get_height() - leg.image.get_height()))
    animation.append(still_image)
    for n in range(leg.animation_length):
        image = pg.Surface.copy(body.image)
        image.blit(head.image, (0, 0))
        image.blit(next(leg.animation), (0, image.get_height() - leg.image.get_height()))
        animation.append(image)
    return (still_image, get_anim_generator(None, animation))



for image in listdir(f"{working_directory}\image_generator\heads"):
    try:
        Head(f"\image_generator\heads\{image}")
    except Exception as e:
        print(e)

for image in listdir(f"{working_directory}\image_generator\\bodies"):
    try:
        Body(f".\image_generator\\bodies\{image}")
    except Exception as e:
        print(e)
        
for dir in listdir(f"{working_directory}\image_generator\legs"):
    try:
        Leg(f"\image_generator\legs\{dir}", (1,0,2,0))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    SCREEN_SIZE = (WIDTH, HEIGHT) = 1000, 700
    SCREEN = pg.display.set_mode(SCREEN_SIZE)
    SCREEN.fill((60,60,80))
    sprite = get_sprite_by_names("test2", "test2", "test1")
    sprite2 = get_sprite_by_names("test2", "test1", "test1")
    sprite3 = get_sprite_by_names("test1", "test1", "test2")
    for n in range(10):
        SCREEN.blit(next(sprite[1]), (0,n*50))
    for n in range(10):
        SCREEN.blit(next(sprite2[1]), (50,n*50))
    for n in range(10):
        SCREEN.blit(next(sprite3[1]), (100,n*50))
    pg.display.flip()
    input()