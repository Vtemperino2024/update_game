# content from kids can code: http://kidscancode.org/blog/
#content from geeksforgeeks: https://www.geeksforgeeks.org/how-to-use-images-as-backgrounds-in-tkinter/
# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
import math
from tkinter import *
import time
from time import *
import tkinter as tk



vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Game:
    
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self): 
        # create a group for all sprites
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_rockets = pg.sprite.Group()
        self.player = Player(self)
        # instantiate classes
        
        # add instances to groups  
        self.all_sprites.add(self.player)
        self.ground = Platform(*GROUND)
        self.all_sprites.add(self.ground)

        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)
        # create mobs...
        for m in range(0,8):
            m = Mob(randint(0, WIDTH), randint(0, math.floor(HEIGHT)), 20, 20, "normal")
            self.all_sprites.add(m)
            self.all_mobs.add(m)
        
       
        for i in range(0,10):
            rockt =Rocket(randint(0,WIDTH), randint(0,math.floor(HEIGHT)), 5, 5, "moving")
            self.all_rockets.add(rockt)
            self.all_sprites.add(rockt)
        self.run()

    def createRocket(self):
        newrockt =Rocket(randint(0,WIDTH), randint(0,math.floor(HEIGHT)), 5, 5, "moving")
        self.all_rockets.add(newrockt)
        self.all_sprites.add(newrockt)

    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
         # this prevents the player from jumping up through a platform
        hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
        ghits = pg.sprite.collide_rect(self.player, self.ground)
        if hits or ghits:
            if self.player.vel.y < 0:
                self.player.vel.y = -self.player.vel.y
            # this is what prevents the player from falling through the platform when falling down...
            elif self.player.vel.y > 0:
                if hits:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
                    self.player.score += 2
                    self.player.vel.x = hits[0].speed*1.5
                if ghits:
                    self.player.pos.y = self.ground.rect.top
                    self.player.vel.y = 0

    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    

    
    



# BACKGROUND (image bg script came from geeksforgeeks.org)

    def draw(self):
        ############ Draw ################
        # draw the background screen
        background_img = os.path.join(img_folder, 'backgroundimg.jpg')
       
        bg = pg.image.load(background_img)
        bg.convert()
        self.screen.blit(bg, (0, 0))
        self.all_sprites.draw(self.screen)
        self.draw_text("Hitpoints: " + str(self.player.hitpoints), 22, WHITE, WIDTH/2, HEIGHT/10)
        self.draw_text("Score: " + str(self.player.score),20, WHITE, WIDTH/2, HEIGHT*0.9)
        # buffer - after drawing everything, flip display
        pg.display.flip()


        

    
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass




g = Game()
while g.running:
    g.new()


pg.quit()


