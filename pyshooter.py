import os
import sys
import pygame as pg

from Menu import *
from Player import *
from Background import *
from Bot import *
from Projectiles import *
from ExtendedGroup import *
from Statistics import *
from Light import *
from helpers import *

import Animation
import Sound

###############################################

class Main:
    def __init__(self):
        self._running = True
        self.size = self.width, self.height = 800, 600
        self.fps = 60
    
    def on_init(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pg.mixer.pre_init(frequency=44100, size=0, channels=10, buffer=4096) #size - 16, channels 2
        pg.mixer.init()
        pg.init()
        self._running = True
        self.clock = pg.time.Clock()

        #self.resolution = (int(pg.display.Info().current_w), int(pg.display.Info().current_h))

        self.menu = Menu()
        self._display_surf = pg.display.set_mode(self.size)
        self.screen = pg.display.get_surface() # repetido?

        self.PLAYER_POSITION = (self.width/2, self.height/2)

        self.PLAY_IMAGE = pg.image.load("Assets/Images/player3.png")
        self.PLAY_IMAGE = pg.transform.scale(self.PLAY_IMAGE, (75,75))
        self.PLAY_IMAGE_BACK = pg.image.load("Assets/Images/back_player.png")
        self.PLAY_IMAGE_BACK = pg.transform.scale(self.PLAY_IMAGE_BACK, (75,75))
        
        self.BOT_IMAGE = pg.image.load("Assets/Images/player2.png")
        self.BOT_IMAGE = pg.transform.scale(self.BOT_IMAGE, (75,75))

        self.CROSS_IMAGE = pg.image.load("Assets/Images/cross.png").convert_alpha()
        self.CROSS_IMAGE = pg.transform.scale(self.CROSS_IMAGE, (15,15))
        
        self.player_animation = Animation.Player
        self.player_animation.load()
        self.player_sound = Sound.Player 
        self.player_sound.load()
        self.background = Background()
        self.player = Player((0,-1400), self.PLAYER_POSITION, self.player_animation, self.player_sound, self.background)
        self.bot0 = Bot((100,-1400), self.screen, self.background, self.player)
        self.bot1 = Bot((-100,-1400), self.screen, self.background, self.player)
        self.bot2 = Bot((200,-1400), self.screen, self.background, self.player)
        self.stats = Statistics(self.player, self.screen.get_rect().size)
        self.light = Light(self.size, self.player)
        # esse grupo herda da sprite group
        self.players = ExtendedGroup(self.player)
        self.bots = ExtendedGroup(self.bot0)
        self.bots.add(self.bot1)
        self.bots.add(self.bot2)
        self.bullet_list = ExtendedGroup()
        self.BULLET_IMAGE = pg.image.load("Assets/Images/bullets/bullet1.png")
        self.BULLET_IMAGE = pg.transform.scale(self.BULLET_IMAGE, (15, 3))

    def on_event(self, event):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            self._running = False

        self.players.handle_event(event)
        
        if self.player.is_shooting == True:
            bullet = Projectiles(self.player.position_on_scenario, self.player.position_on_screen, self.BULLET_IMAGE, self.background)
            self.bullet_list.add(bullet)
        
    def display_fps(self):
        pg.display.set_caption("{} - FPS: {:.2f}".format("PyShooter", self.clock.get_fps()))

    def on_loop(self):
        self.clock.tick(self.fps)

        for bullet in self.bullet_list:
            if bullet.distance > 300 or bullet.is_colliding:
                self.bullet_list.remove(bullet)

    def on_cleanup(self):
        pg.quit()
        sys.exit()

    def on_render(self):
        self.screen.fill((0,0,0))

        # sem sprite ainda
        self.background.draw(self.screen, self.player)

        self.players.update()
        self.players.draw(self.screen)
        self.bots.update()
        self.bots.draw(self.screen)

        self.bullet_list.update()
        self.bullet_list.draw(self.screen)

        # acho que não precisa de sprite pra essa
        self.screen.blit(self.CROSS_IMAGE, pg.mouse.get_pos())

        self.light.draw(self.screen)
        self.stats.draw(self.screen)
        
        self.display_fps()
        pg.display.update()

    def on_execute(self):
        self.on_init()

        self.menu.intro()

        pg.mouse.set_visible(0)

        while (self._running):
            for event in pg.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    Main().on_execute()
