# this file was created by Rahul Padhi 
# sprite classes for game 
import pygame as pg
from pygame.sprite import Sprite
import random 
from settings import* 

class Player(Sprite):
# creates the first player   
    def __init__(self):
        # defines dimensions of player one box 
        Sprite.__init__(self)
        self.image = pg.Surface((30,40))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height /2)
        self.vx = 0
        self.vy = 0
    def update(self):
        # updates player one when keys are pressed 
        self.vx = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vx = -5
        if keys[pg.K_RIGHT]:
            self.vx = 5
    def gravity(self):
        # brings player down after jump 
        if self.rect.y < height - 40:
            self.falling = True 
            print("Gravity is happening! " + str(self.rect.y))
            print("Falling " + str(self.falling))
    def jump(self):
        # runs when player jumps
        self.vy = -75 
        print("Jump called")
        

class Enemy(Sprite):
    # creates a second player or enemy
    def __init__(self):
        # dimensions of the enemy box 
        Sprite.__init__(self)
        self.image = pg.Surface((30,40))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.center = (width/ 2,height/2)
        self.vx = 0
        self.vy = 0
    def update(self):
        # updates enemy when key are pressed for it to move
        self.vx = 0
        keys = pg.key.get_pressed()
        # player moves left 
        if keys[pg.K_a]:
            self.vx = -5
        # player moves right
        if keys[pg.K_d]:
            self.vx = 5
        # makes player jump
        if keys[pg.K_UP] and self.falling == False:
            self.jump()            
        
        self.rect.x += self.vx
        self.rect.y += self.vy
    
class Platform(Sprite):
    #creates a platform for box to land on 
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((400,20))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height /2)