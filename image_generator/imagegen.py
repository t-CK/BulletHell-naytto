import pygame as pg
from os import listdir
from pathlib import Path
from pygame.locals import *

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
    if len(filelist) == 1:
        sequence = (0,)
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
    
def get_sprite_by_index(head, body, leg) -> (pg.image, list):
    """ Returns a tuple of (Sprite standing still, Generator for walk animation)
        from the parts' list indexes """
    return combine_sprite(heads[head], bodies[body], legs[leg])

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
    
### Väkinäinen, nopea SQL-tallennus ja lataus, koska tutkintovaatimus:
import sqlite3 as sql

def save_sql(head, body, leg):
    conn = sql.connect("sql.db")
    cursor = conn.cursor()
    parts = (heads[head_cursor].name, bodies[body_cursor].name, legs[leg_cursor].name)
    cursor.execute("UPDATE parts SET head = ?, body = ?, leg = ? WHERE id = 0", parts)
    conn.commit()
    conn.close()
    
def load_sql():
    conn = sql.connect("sql.db")
    cursor = conn.cursor()
    correct_parts = []
    parts = cursor.execute("SELECT head, body, leg FROM parts").fetchone()
    for n in zip((heads, bodies, legs), parts):
        for i in range(len(n[0])):
            if n[0][i].name == n[1]:
                correct_parts.append(i)
                break
    conn.close()
    return correct_parts
### SQL-touhu ohi


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
    """ Just a quick UI for demonstration purposes """
    SCREEN_SIZE = (WIDTH, HEIGHT) = 640, 480
    SCREEN = pg.display.set_mode(SCREEN_SIZE)
    sprite = pg.sprite.Sprite()
    sprite.image = None
    clock = pg.time.Clock()
    head_cursor, body_cursor, leg_cursor = (0, 0, 0)
    redraw_needed = True
    
    while True:
        SCREEN.fill((60,60,80))
        if redraw_needed:
            image_preview, animator = combine_sprite(heads[head_cursor], bodies[body_cursor], legs[leg_cursor])
            redraw_needed = False
        if not sprite.image:
            sprite.image = image_preview
        else:
            sprite.image = next(animator)
        sprite.image = pg.transform.scale_by(sprite.image, 4)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = (WIDTH//2, HEIGHT//2)
        
        SCREEN.blit(sprite.image, sprite.rect)
        
        text_surfs = []
        for _ in ("Q", "A", "Z"):
            text_surfs.append(pg.font.Font(None,50).render(_, False, (0,0,0)))
        for _ in range(len(text_surfs)):
            text_rect = text_surfs[_].get_rect()
            text_rect.center = (sprite.rect.left - 50, sprite.rect.top + _*80)
            SCREEN.blit(text_surfs[_], text_rect)
        
        text_surfs = []        
        for _ in ("E", "D", "C"):
            text_surfs.append(pg.font.Font(None,50).render(_, False, (0,0,0)))
        for _ in range(len(text_surfs)):
            text_rect = text_surfs[_].get_rect()
            text_rect.center = (sprite.rect.right + 50, sprite.rect.top + _*80)
            SCREEN.blit(text_surfs[_], text_rect)

        text_surfs = []
        partnames = (heads[head_cursor].name.title(), bodies[body_cursor].name.title(), legs[leg_cursor].name.title())
        for _ in partnames:
            text_surfs.append(pg.font.Font(None,30).render(_, False, (0,0,0)))
        for _ in range(len(text_surfs)):
            text_rect = text_surfs[_].get_rect()
            text_rect.center = (sprite.rect.x - 90 + (_*150), sprite.rect.bottom + 80)
            SCREEN.blit(text_surfs[_], text_rect)
                
        txt = pg.font.Font(None,25).render("F5: Save SQL", False, (0,0,0))
        text_rect = txt.get_rect(topleft = (30,30))
        SCREEN.blit(txt, text_rect)
        txt = pg.font.Font(None,25).render("F8: Load SQL", False, (0,0,0))
        text_rect = txt.get_rect(topright = (WIDTH-30,30))
        SCREEN.blit(txt, text_rect)
        
            
        pg.display.flip()
        clock.tick(7)
        
        for event in pg.event.get():
            if event.type == KEYDOWN:
                redraw_needed = True
                if event.key == K_ESCAPE:
                    pg.quit()
                elif event.key == K_q:
                    head_cursor = head_cursor - 1 if head_cursor > 0 else len(heads)-1
                elif event.key == K_e:
                    head_cursor = head_cursor + 1 if head_cursor < len(heads)-1 else 0
                elif event.key == K_a:
                    body_cursor = body_cursor - 1 if body_cursor > 0 else len(bodies)-1
                elif event.key == K_d:
                    body_cursor = body_cursor + 1 if body_cursor < len(bodies)-1 else 0
                elif event.key == K_z:
                    leg_cursor = leg_cursor - 1 if leg_cursor > 0 else len(legs)-1
                elif event.key == K_c:
                    leg_cursor = leg_cursor + 1 if leg_cursor < len(legs)-1 else 0
                    
                elif event.key == K_RETURN:
                    pg.image.save(image_preview, "sprite.png")
                    pg.quit()
                    
                elif event.key == K_F5:
                    save_sql(heads[head_cursor].name, bodies[body_cursor].name, legs[leg_cursor].name)
                elif event.key == K_F8:
                    head_cursor, body_cursor, leg_cursor = load_sql()