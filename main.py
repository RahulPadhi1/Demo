# this file was created by Rahul Padhi 
# sources: goo.gl/2KMivS
# dkfjkmdf
import pygame as pg
import random 
from settings import* 
from sprites import* 

class Game:
    def __init__(self):
        #init game window
        # init pygame and create window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption("jumpy")
        self.clock = pg.time.Clock()
        self.running = True 
    def new(self):
        # adds the sprites to this group 
        self.all_sprites = pg.sprite.Group()
        # adds player 1 
        self.player = Player()
        self.all_sprites.add(self.player)
        # add player 2 
        self.enemy = Enemy()
        self.all_sprites.add(self.enemy)
        # calls the run method
        self.run()
    def run(self):
        # set boolean playing to true
        self.playing = True
        while self.playing:
            # defines what happens while function runs 
            self.clock.tick(Fps)
            self.events()
            self.update()
            self.draw()
    def update(self):
        # updates the sprite 
        self.all_sprites.update()    
    def events(self):
        # functions for when game ends 
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    def draw(self):
        # draws on the screen 
        self.screen.fill(reddish)
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

g = Game()

g.show_go_screen()

while g.running:
    g.new()
    g.show_go_screen()