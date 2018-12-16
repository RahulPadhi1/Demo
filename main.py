# this file was created by Rahul Padhi 
# Sources: goo.gl/2KMivS 
# now available in github

'''
Curious, Creative, Tenacious Game Idea 

**********Gameplay ideas:
Adding a second player making this a multiplayer game
Adding a coin to boost the score by 100 points 
Making the cactus shoot the player downwards

**********Bugs
Fixing some glitches with the platforms where your character doesnt land on the platform and dies 
Fixing the glitch where you hit the cactus and you do not get show downward 
Showing the endscreen when the player hits the mob 

**********Gameplay fixes
Adding an end screen after someone dies
Making sure the platforms are less random so that they are never right mext to each other 
Pausing screen when you hit the monsters so you know how you hit it 

**********Features
Character coin boosts 
Cactus downward boost 
Sound effects for cactus and coins 
End Screen After death and death sound 

'''

import pygame as pg
import random
from settings import *
from sprites import *
from os import path
import sys
import time

class Game:
    def __init__(self):
        # initializing the pygame game window 
        pg.init()
        # initializing the game sounds
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("jumpy")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
    def load_data(self):
        print("load data is called...")
        # sets up directory name for images
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        # opens file with write options
        try:
            # imports the highscore of the game into my code 
            with open(path.join(self.dir, "highscore.txt"), 'r') as f:
                self.highscore = int(f.read())
                print(self.highscore)
        except:
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                self.highscore = 0
                print("exception")
        # loading the sprites for the game images 
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET)) 
        # loading the random clouds for the background image of the game 
        self.cloud_images = []
        for i in range(1,4):
            self.cloud_images.append(pg.image.load(path.join(img_dir, 'cloud{}.png'.format(i))).convert())
        # loading in the game sounds 
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = [pg.mixer.Sound(path.join(self.snd_dir, 'Jump18.wav')),
                            pg.mixer.Sound(path.join(self.snd_dir, 'Jump24.wav'))]
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump29.wav'))
        self.coin_sound = pg.mixer.Sound(path.join(self.snd_dir, 'smw_coin.wav'))
        self.head_jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump39.wav'))
        self.death_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Sad_Trombone.wav'))
    def new(self):
        self.score = 0
        self.paused = False
        # loading in all the sprites 
        self.all_sprites = pg.sprite.LayeredUpdates()
        # create platforms group
        self.platforms = pg.sprite.Group()
        # create clouds group
        self.clouds = pg.sprite.Group()
        # add powerups group 
        self.powerups = pg.sprite.Group()
        # add coin powerup // no longer needed; inputted as a powerup 
        # self.pointboost = pg.sprite.Group()
        # add cacti group 
        self.cacti = pg.sprite.Group()
        # initializing mob timer for the random mob spawns       
        self.mob_timer = 0
        # adds a player 1 to the group
        self.player = Player(self)
        # add mobs group 
        self.mobs = pg.sprite.Group()
        for plat in PLATFORM_LIST:
            # initializes list of platforms 
            Platform(self, *plat)
        for i in range(8):
            c = Cloud(self)
            c.rect.y += 500
        # loads the game music
        pg.mixer.music.load(path.join(self.snd_dir, 'happy.ogg'))
        # calls the games run method
        self.run()
    def run(self):
        # play music
        pg.mixer.music.play(loops=-1)
        # sets the game playing to true; starts the game 
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(1000)
    # adding a end screen after the game ends 
    def end_screen(self):
        # stops game music
        pg.mixer.music.stop()
        self.screen.fill(PURPLE)
        self.draw_text(ENDGAME, 48, BLACK, WIDTH/2, HEIGHT/4)
        self.draw_text("You died", 36, BLACK, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key if you want to play again...", 22, BLACK, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("Your score " + str(self.score), 22, BLACK, WIDTH / 2, 15)
        self.draw_text("Click off if you do not want to play again", 22, BLACK, WIDTH / 2, HEIGHT * 6/7)
        # plays music for death 
        self.death_sound.play()
        pg.display.flip()
        self.wait_for_key()
    def update(self):
        self.all_sprites.update()
        # spawns the mobs 
        now = pg.time.get_ticks()
        # checking for mob collisions
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
        # now using collision mask to determine collisions
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            # makes player boosts upwards if player hits top of mobs head 
            if self.player.pos.y - 35 < mob_hits[0].rect.top:
                print("hit top")
                print("player is " + str(self.player.pos.y))
                print("mob is " + str(mob_hits[0].rect.top))
                self.head_jump_sound.play()
                self.player.vel.y = -BOOST_POWER
            else:
            # kills player if he hits bottom of mob 
                print("player is " + str(self.player.pos.y))
                print("mob is " + str(mob_hits[0].rect.top))
                pg.mixer.music.stop()
                time.sleep(1)
                self.playing = False
                self.end_screen()
        # check to see if player can jump - if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                ''' set var to be current hit in list to find which to 'pop' to 
                when two or more collide with player'''
                find_lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > find_lowest.rect.bottom:
                        print("hit rect bottom " + str(hit.rect.bottom))
                        find_lowest = hit
                # player dies if it is off the platform
                if self.player.pos.x < find_lowest.rect.right + 5 and self.player.pos.x > find_lowest.rect.left - 5:
                    if self.player.pos.y < find_lowest.rect.centery:
                        self.player.pos.y = find_lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
        # if player reaches top 1/4 of screen...
        if self.player.rect.top <= HEIGHT / 4:
            # spawn a cloud
            if randrange(100) < 13:
                (self)
            # set player location based on velocity
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / randrange(2,10)), 2)
            # creates slight scroll at the top based on player y velocity
            # scroll plats and mobs with player
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT + 40:
                    plat.kill()
                    self.score += 10
        # if player the boost hits a power up
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

            else: 
                ''' coin_hits = pg.sprite.spritecollide(self.player, self.pointboost, True)
                # for pow in coin_hits:
                #     if pow.type == 'coin':
                above code no longer needed since the coin is a power up '''
                # if player hits the coin 
                self.coin_sound.play()
                self.score += 100
        cacti_hits = pg.sprite.spritecollide(self.player, self.cacti, False)
        # boosts player downwards if cactus hits them // does not always kill them 
        if cacti_hits:    
            if self.player.vel.y > 0 and self.player.pos.y > cacti_hits[0].rect.top:
                    print("falling")
                    print("player is " + str(self.player.pos.y))
                    print("mob is " + str(cacti_hits[0].rect.top))
                    self.player.vel.y = BOOST_POWER
                    self.end_screen
        # if player dies; plays the end screen
        if self.player.rect.bottom > HEIGHT:
            '''make all sprites fall up when player falls'''
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                '''get rid of sprites as they fall up'''
                if sprite.rect.bottom < -25:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False
            self.end_screen()
        # generating new random platforms
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0,WIDTH-width), 
                            random.randrange(-75, -30))
    def events(self):
        # making the game controls WASD
        # determining when game is playing and when not playing 
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.player.jump()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        """ # cuts the jump short if the space bar is released """
                        self.player.jump_cut()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_p:
                        """ pause """
                        self.paused = True
    def draw(self):
        # drawing the in-game animation
        self.screen.fill(SKY_BLUE)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # double buffering - renders a frame "behind" the displayed frame
        pg.display.flip()
    def wait_for_key(self): 
        # makes sure game only starts if player pressa key
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type ==pg.KEYUP:
                    waiting = False
# showing first screen when game is run
    def show_start_screen(self):
        """ # game splash screen """
        self.screen.fill(BLUE)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Use WASD to move and the space bar to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High score " + str(), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
# Showing screen if player wants to play again
    def show_go_screen(self):
        """ # game splash screen """
        if not self.running:
            print("not running...")
            return
        self.screen.fill(BLUE)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("WASD to move, Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 40)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("new high score!", 22, WHITE, WIDTH / 2, HEIGHT/2 + 60)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))

        else:
            self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 40)
        pg.display.flip()
        self.wait_for_key()
    ##### drawing text on the game screen
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
    
# playing the game function 
g = Game()

g.show_start_screen()


while g.running:
    g.new()
    try:
        g.show_go_screen()
    except:
        print("can't load go screen...")