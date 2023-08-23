import pygame as pg
import random, math
import pickups, misc
from variables import *

class Enemy(pg.sprite.Sprite):
    """ Rudimentary enemy sprite object (probably gonna move much of this to a child class)

    Variables: (in addition to pygame's Sprite stuff)
        hp, speed: Self-explanatory
        dmg: Damage the enemy deals when bumping into player
        solid: If False, can pass through world obstacles / other solid enemies
        invulnerable: Ticks of invulnerability (i-frames)

    Methods:
        update(): Pygame's Sprite-update. Decrease i-frames and move towards player. (+ collision)
        damage(): Decrease HP (if not invulnerable) and set i-frames. Call death() if needed.
        death(): Drop XP and kill sprite.
    """
    def __init__(self, game, position = misc.get_spawn, hp = 3, dmg = 1, solid = True):
        super().__init__()
        self.game = game
        try:
            self.player = game.player
        except AttributeError:
            self.player = game._player       
        self.surf = pg.Surface([19,25])
        self.color = (60,255,60)
        self.surf.fill(self.color)
        
        if not (SPRITE_SCALE == 1 or SPRITE_SCALE == 0):
            self.surf = pg.transform.scale_by(self.surf, SPRITE_SCALE)

        self.rect = self.surf.get_rect()
        if not callable(position):
            self.rect.center = position
        else:
            self.rect.center = position()

        self.hp = hp
        self.dmg = dmg
        self.solid = solid
        self.invulnerable = 0

        all_sprites.add(self)
        enemy_group.add(self)
        if self.solid:
            collideable.add(self)

    def update(self):
        """ Decrease i-frames """
        if self.invulnerable > 0:
            self.invulnerable -= 1

    def damage(self, amount = 1):
        """ Decrease HP (and Surface size) and set i-frames. """
        if self.invulnerable:
            return
        self.hp -= amount
        if self.hp <= 0:
            self.death()
        self.invulnerable = 5

        self.surf = pg.transform.scale_by(self.surf, 0.8)
        if self.color:  # If sprite's image is not loaded
            temp_color_r, temp_color_g, temp_color_b = self.color
            temp_color_g = max(temp_color_g-100, 0)
            temp_color_b = min(temp_color_b+100, 255)
            self.color = temp_color_r, temp_color_g, temp_color_b
            self.surf.fill(self.color)
        temp_center = self.rect.center
        self.rect = self.surf.get_rect()
        self.rect.center = temp_center

    def death(self):
        """ Drop XP and die """
        pickups.Xp(self.game, *self.rect.center, random.randrange(len(pickups.Xp._colors))+1)
        self.game._counters.kill_update()
        self.kill()

class Enemy_Follow(Enemy):
    """ Enemy moving in a straight line towards player """
    def __init__(self, game, position = misc.get_spawn, target: tuple or Sprite = None,
                 hp = 3, speed = 1, dmg = 1, solid = True):
        super().__init__(game, position, hp, dmg, solid)
        try:
            self.surf = pg.image.load("./images/enemy.png").convert()
            self.surf.set_colorkey((0,255,0))
            self.color = None
        except FileNotFoundError:
            pass
            
        if not (SPRITE_SCALE == 1 or SPRITE_SCALE == 0):
            self.surf = pg.transform.scale_by(self.surf, SPRITE_SCALE)
        self.rect = self.surf.get_rect(center = self.rect.center)
        self.speed = speed

        if target is None: # Default to player...
            self.target = self.player.rect.center
        elif type(target) is tuple: # ...but allow targeting coordinates...
            self.target = target
        else: #  ...as well as other Sprites
            self.target = target.rect.center

    def update(self) -> bool:
        """ Move towards player. Move back until there's no collision (if solid).

        If collision was detected, return True
        """
        super().update() # For i-frames
        collided = False
        collideable.remove(self)
        if self.target[0] > self.rect.center[0]:
            self.rect.move_ip(self.speed,0)
            while self.solid and pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(-1,0)
                collided = True
        elif self.target[0] < self.rect.center[0]:
            self.rect.move_ip(-self.speed,0)
            while self.solid and pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(1,0)
                collided = True
        if self.target[1] > self.rect.center[1]:
            self.rect.move_ip(0,self.speed)
            while self.solid and pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(0,-1)
                collided = True
        elif self.target[1] < self.rect.center[1]:
            self.rect.move_ip(0,-self.speed)
            while self.solid and pg.sprite.spritecollideany(self, collideable):
                self.rect.move_ip(0,1)
                collided = True
        if self.solid:
            collideable.add(self)
        return collided

class Enemy_Sine(Enemy_Follow):
    """ Enemy_Follow but with some added circling """
    def __init__(self, game, position = misc.get_spawn, target = None, hp = 3, speed = 1, dmg = 1, solid = False):
        super().__init__(game, position, target, hp, speed, dmg, solid)

    def update(self):
        collided = super().update() # For i-frames and movement towards player

        # First (bad) attempt at moving in a wave while closing in
        step = misc.get_step(self.rect.center, self.target, self.speed)
        self.offset = (-step[1] * 10*math.sin(self.game._ticks/10), step[0] * 10*math.sin(self.game._ticks/10))
        self.rect.move_ip(self.offset)

class Enemy_Worm_Head(Enemy):
    """ Worm type enemy head (incomplete) """
    def __init__(self, game, position = misc.get_spawn, tail_length = 20, size = 20, turn_rate = 7,
                turn_speed = 7, hp = 3, speed = 5, dmg = 1, solid = False):
        super().__init__(game, position, hp, dmg, solid)
        self.surf = pg.Surface([size,size])
        self.surf.fill((0,255,0))
        self.surf.set_colorkey((0,255,0))
        self.rect = self.surf.get_rect(center = (self.rect.center))
        pg.draw.circle(self.surf, (50,250,50), self.rect.center, size/2)
        self.turn_rate = turn_rate
        self.turn_speed = turn_speed
        self.speed = speed
        self.last_position = self.rect.center # For checking if and where the tail should follow

        # Ottaa targetin jostain pelaajan läheltä spawnautuessaan, kulkee sen läpi kiemurrellen
        # kunnes despawnautuu ja vaihtaa suuntaa lähtien takaisin ruudun samasta sivusta?
        target = (game._player.rect.centerx + random.randint(-200, 200),
                  game._player.rect.centery + random.randint(-200, 200))
        self.step = misc.get_step(self, target, self.speed)
        self.sidestep = misc.get_step_p(self.step, self.turn_speed)
        
        all_sprites.add(self)
        enemy_group.add(self)

        if tail_length > 0:
            self.child = Enemy_Worm_Tail(self, tail_length - 1, size - 2)
        else:
            self.child = None

    def update(self):
        super().update()
        self.last_position = self.rect.center
        # Combine step forward to sideways move, apply sine for wave (with turn_rate for tweaking shape)
        x_move, y_move = (self.step[0] + self.sidestep[0] * math.sin(self.game._ticks/self.turn_rate),
                          self.step[1] + self.sidestep[1] * math.sin(self.game._ticks/self.turn_rate))
        self.rect.move_ip(x_move, y_move)
        if self.rect.center == self.last_position: # If movement was completely blocked, set to None
            self.last_position = None
            
    def damage(self, amount = 1):
        """ If the whole (attached) tail is dead, take damage. Else transfer the damage to the last part of remaining tail """ 
        if self.invulnerable:
            return
        if self.child:
            self.child.pass_damage(amount)
        else:
            self.hp -= amount
            if self.hp <= 0:
                self.death()
        self.invulnerable = 5

class Enemy_Worm_Tail(pg.sprite.Sprite):
    """ Child object following Enemy_Worm_Head (and other Tails)  (incomplete) """
    def __init__(self, parent, tail_length, size):
        super().__init__()
        self.surf = pg.Surface([size,size])
        self.rect = self.surf.get_rect()
        self.surf.fill((0,255,0))
        self.surf.set_colorkey((0,255,0))
        self.color = (50, 150, 50)
        pg.draw.circle(self.surf, self.color, self.rect.center, size/2)
        self.parent = parent

        self.rect.center = self.parent.last_position
        self.last_position = self.parent.last_position
        self.hp = parent.hp
        self.dmg = parent.dmg
        self.invulnerable = 0
        if size < 5:
            size = 5
        self.size = size

        all_sprites.add(self)
        enemy_group.add(self)
        # tail_group.add(self)
        self.dead = False

        if tail_length > 0:
            self.child = Enemy_Worm_Tail(self, tail_length - 1, size - 1)
        else:
            self.child = None

    def update(self):
        """ Decrease i-frames, follow the parent to their last position and set own """
        if self.invulnerable > 0:
            self.invulnerable -= 1
        self.last_position = self.rect.center
        if self.parent and self.parent.last_position: # Move only if parent moved (last_position != None)
            self.rect.center = self.parent.last_position
        else:
            self.last_position = None

    def damage(self, amount = 1):
        """ Decrease HP and set i-frames. """
        if self.invulnerable or self.dead:
            return
        self.hp -= amount
        self.color = pg.Color(self.color).lerp((70,0,0), 0.5)
        self.rect = self.surf.get_rect()
        pg.draw.circle(self.surf, self.color, self.rect.center, self.size/2)
        if self.hp <= 0:
            self.death()
        self.invulnerable = 5
        
    def pass_damage(self, amount):
        """ Pass damage from head on to last child. """
        if self.child:
            self.child.pass_damage(amount)
        else:
            self.damage(amount)
    
    def death(self):
        """ TODO: everything """
        self.dead = True
        if self.parent:
            self.parent.child = None
            self.parent = None
        self.child = None
        enemy_group.remove(self)
        # self.kill()