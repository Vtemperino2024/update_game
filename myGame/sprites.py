import pygame as pg
from pygame.sprite import Sprite

from pygame.math import Vector2 as vec
import os
from settings import *

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # self.image = pg.Surface((50, 50))
        # self.image.fill(GREEN)
        # use an image for player sprite...
        plr = self
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'theBigBell.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.score = 0
        self.hitpoints = 100
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_SPACE]:
            self.jump()
    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        ghits = pg.sprite.collide_rect(self, self.game.ground)
        hitsrocket = pg.sprite.spritecollide(self, self.game.all_rockets, False)

        if hitsrocket:
            print("hit")
            self.hitpoints -= 5

        if hits or ghits:
            print("i can jump")
            self.vel.y = -PLAYER_JUMP
        
    def update(self):
        # CHECKING FOR COLLISION WITH MOBS HERE>>>>>
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        self.rect.center = self.pos
        # if friction - apply here
        self.acc.x += self.vel.x * -PLAYER_FRIC
        # self.acc.y += self.vel.y * -0.3
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

# platforms



class Platform(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        if self.category == "moving":
            self.speed = 5
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed

class Mob(Sprite):
    def __init__(self, x, y, w, h, kind):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = (WIDTH, HEIGHT)

    def update(self):
        pass


class Rocket(Sprite):
    def __init__(self, x, y, w, h, kind):
        Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, "rocket_img.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = x
        self.kind = kind
        if self.kind == "moving":
            self.speed = 4
            self.upspeed = 2

        
            
    def update(self):
        
        if self.kind == "moving":
            self.rect.x += self.speed
            self.rect.y += self.upspeed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed
            if self.rect.y + self.rect.h > HEIGHT or self.rect.y < 0:
                self.upspeed = -self.upspeed
            
    






    