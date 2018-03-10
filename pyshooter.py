import os
import sys
import pygame as pg

from Menu import *
from Player import *
from Background import *
from Bot import *
from ExtendedGroup import *
from Statistics import *

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
        pg.mixer.pre_init(frequency=44100, size=0, channels=1, buffer=4096) #size - 16, channels 2
        pg.mixer.init()
        pg.init()
        self._running = True
        self.clock = pg.time.Clock()

        #self.resolution = (int(pg.display.Info().current_w), int(pg.display.Info().current_h))

        self.menu = Menu()

        # no final vai ser melhor usar o self.resolution no lugar de self.size e usar o pg.FULLSCREEN
        # mas em desenvolvimento pode ser melhor manter assim para permitir a visualização no console
        self._display_surf = pg.display.set_mode(self.size)
        self.screen = pg.display.get_surface() # repetido?
        
        self.PLAYER_POSITION = (self.width/2, self.height/2)

        self.CROSS_IMAGE = pg.image.load("Assets/Images/cross.png").convert_alpha()
        self.CROSS_IMAGE = pg.transform.scale(self.CROSS_IMAGE, (15,15))
        
        self.player_animation = Animation.Player
        self.player_animation.load()
        self.player_sound = Sound.Player 
        self.player_sound.load()

        self.background = Background()
        self.player = Player((0,0), self.PLAYER_POSITION, self.player_animation, self.player_sound, self.background)
        self.bot0 = Bot((200,200), self.screen, self.background, self.player)
        self.stats = Statistics(self.player, self.screen.get_rect().size)
        
        # esse grupo herda da sprite group
        self.players = ExtendedGroup(self.player)
        self.bots = ExtendedGroup(self.bot0)

        # test lighting effect
        #########################################
        self.fog = pg.Surface(self.size)
        self.fog.fill((20,20,20))
        self.light_mask = pg.image.load('Assets/Images/light.png').convert_alpha()
        self.light_rect = self.light_mask.get_rect()
        #########################################

    def on_event(self, event):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            self._running = False

        self.players.handle_event(event)
        
    def display_fps(self):
        pg.display.set_caption("{} - FPS: {:.2f}".format("PyShooter", self.clock.get_fps()))

    def on_loop(self):
        self.clock.tick(self.fps)

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

        # acho que não precisa de sprite pra essa
        self.screen.blit(self.CROSS_IMAGE, pg.mouse.get_pos())

        # test lighting effect
        ######################################################
        self.fog.fill((20,20,20))
        self.light_rect.center = self.player.position_on_screen
        # rot_light = pg.transform.rotozoom(self.light_mask, -self.player.sight_angle - 90, 1)
        # new_rect = rot_light.get_rect(center = self.light_rect.center)
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)
        ######################################################
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
