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

        self.hp = hp + game._ticks//4000
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
        """ Drop XP (and every once in a while, a Bombs-item) and die """
        pickups.Xp(self.game, *self.rect.center, random.randrange(len(pickups.Xp._colors))+1)
        if random.randrange(100) < 5:
            pickups.Item_Bombs(self.game, *self.rect.center)
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
    """ Worm type enemy head
    
    Variables not in Enemy:
        tail_length
            Length of Worm. 
        size
            Side of square pg.Surface. Passed to child as one smaller.
        turn_rate
            Divides ticks in movement's sin() for shaping wave.
        turn_speed
            Speed of sideways movement
        child
            "Attached" Enemy_Worm_Tail(). tail_length, size and dmg are passed to child as smaller.
    
    No idea what to do after collision yet, so solid probably shouldn't be set True.
    """
    def __init__(self, game, position = misc.get_spawn, tail_length = 30, size = 25, turn_rate = 7,
                turn_speed = 7, hp = 5, speed = 5, dmg = 1, solid = False):
        super().__init__(game, position, hp, dmg, solid)
        self._centerx, self._centery = game.player.rect.center # For targeting regardless of screen resolution
        self.surf = pg.Surface([size,size])
        self.surf.fill((0,255,0))
        self.surf.set_colorkey((0,255,0))
        self.color = (50, 150, 50)
        self.rect = self.surf.get_rect(center = (self.rect.center))
        pg.draw.circle(self.surf, self.color, (size//2, size//2), size//2)
        self.turn_rate = turn_rate
        self.turn_speed = turn_speed
        self.speed = speed
        self.last_position = self.rect.center # For checking if and where the tail should follow
        self.get_target() # To set self.step and self.sidestep for movement
        
        all_sprites.add(self)
        enemy_group.add(self)

        if tail_length > 0:
            self.child = Enemy_Worm_Tail(self, tail_length - 1, size - 1, hp - 0.25)
        else:
            self.child = None

    def update(self):
        super().update()
        spawn_side = None
        # If far enough outside the screen, take new target and spawn again from the same side
        if self.rect.centery < -1000:
            spawn_side = 0
        elif self.rect.centerx > self.game._wnd_size[0]+1000:
            spawn_side = 1
        elif self.rect.centery > self.game._wnd_size[1]+1000:
            spawn_side = 2
        elif self.rect.centerx < -1000:
            spawn_side = 3
        
        if spawn_side is not None:
            self.get_target()
            self.rect.center = misc.get_spawn(spawn_side)

        self.last_position = self.rect.center
        # Combine step forward to sideways move, apply sine for wave (with turn_rate for tweaking shape)
        x_move, y_move = (self.step[0] + self.sidestep[0] * math.sin(self.game._ticks/self.turn_rate),
                          self.step[1] + self.sidestep[1] * math.sin(self.game._ticks/self.turn_rate))
        self.rect.move_ip(x_move, y_move)
        if self.rect.center == self.last_position: # If movement was completely blocked, set to None
            self.last_position = None

    def get_target(self):
        """ Set target to a random point near player """
        target = (self._centerx + random.randint(-200, 200),
                  self._centery + random.randint(-200, 200))
        self.step = misc.get_step(self, target, self.speed)
        self.sidestep = misc.get_step_p(self.step, self.turn_speed)

    def damage(self, amount = 1):
        """ If the whole (attached) tail is dead, take damage.
        Else transfer the damage to the last part of remaining tail """ 
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
    """ Child object following Enemy_Worm_Head (and other Tails) """
    def __init__(self, parent, tail_length, size, hp):
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
        self.hp = max(hp, 1)
        self.size = max(size, 10)
        self.dmg = parent.dmg
        self.invulnerable = 0

        all_sprites.add(self)
        enemy_group.add(self)

        if tail_length > 0:
            self.child = Enemy_Worm_Tail(self, tail_length - 1, self.size - 0.5, self.hp - 0.25)
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
        if self.invulnerable:
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
        if self.parent:
            self.parent.child = None
            self.parent = None
        # self.child = None
        enemy_group.remove(self)