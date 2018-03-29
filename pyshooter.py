import os
import sys
import pygame as pg

from Menu import *
from Player import *
from Background import *
from Statistics import *
from Light import *
from helpers import *
from ObjectsController import *

import Animation
import Sound

###############################################

class Main:
    def __init__(self):
        self._running = True
        self.size = self.width, self.height = 800, 600
        self.fps = 60
        self.multiplayer_on = False
    
    def on_init(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pg.mixer.pre_init(frequency=44100, size=0, channels=10, buffer=4096) #size - 16, channels 2
        pg.mixer.init()
        pg.init()
        self._running = True
        self.clock = pg.time.Clock()

        #self.resolution = (int(pg.display.Info().current_w), int(pg.display.Info().current_h))

        #create Menu object
        self.menu = Menu()

        self._display_surf = pg.display.set_mode(self.size)
        self.screen = pg.display.get_surface() # repetido?

        #initialize "loading menu"
        self.ICON = pg.image.load("Assets/Images/cross.png")
        self.ICON = pg.transform.scale(self.ICON, (32, 32))
        self.screen.blit(self.menu.MENU_IMAGE, (0, 0))
        pg.display.update()
        pg.display.set_caption("Pyshooter")
        pg.display.set_icon(self.ICON)

        self.PLAYER_POSITION = (self.width/2, self.height/2)

        self.PLAY_IMAGE = pg.image.load("Assets/Images/player3.png")
        self.PLAY_IMAGE = pg.transform.scale(self.PLAY_IMAGE, (75,75))
        self.PLAY_IMAGE_BACK = pg.image.load("Assets/Images/back_player.png")
        self.PLAY_IMAGE_BACK = pg.transform.scale(self.PLAY_IMAGE_BACK, (75,75))
        
        self.CROSS_IMAGE = pg.image.load("Assets/Images/cross.png").convert_alpha()
        self.CROSS_IMAGE = pg.transform.scale(self.CROSS_IMAGE, (15,15))
        
        self.player_animation = Animation.Player
        self.player_animation.load()
        self.player_sound = Sound.Player 
        self.player_sound.load()

        self.background = Background()


        self.player = Player((0, -1400), self.PLAYER_POSITION, self.player_animation, self.player_sound, self.background)

        self.light = Light(self.size, self.player)

        # esse grupo herda da sprite group
        self.players = ExtendedGroup(self.player)


        #call menu Displays/Loops
        self.menu.intro()

        self.server_client = None
        self.is_host = None

        #Get informations about multiplayer/singleplayer
        self.multiplayer_on = self.menu.have_client
        if self.multiplayer_on:
            self.server_client = self.menu.server_client
            self.is_host = self.menu.is_host

        self.player = Player((0, -1400), self.PLAYER_POSITION, self.player_animation, self.player_sound, self.background)

        self.light = Light(self.size, self.player)

        # esse grupo herda da sprite group
        self.players = ExtendedGroup(self.player)

        self.stats = Statistics(self.player, self.screen.get_rect().size, self.multiplayer_on, self.server_client, self.is_host)

        #Set mouse invisible
        pg.mouse.set_visible(0)

        #Define Objects Controller
        self.ObjectsController = ObjectsController(self.player, self.background,self.multiplayer_on, self.server_client, self.menu, self.players, self.is_host)
        
    def on_event(self, event_queue):
        for event in event_queue:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self._running = False

            self.players.handle_event(event)
        self.ObjectsController.handle_event()

    def display_fps(self):
        pg.display.set_caption("{} - FPS: {:.2f}".format("PyShooter", self.clock.get_fps()))

    def on_loop(self):
        self.clock.tick(self.fps)
        self.ObjectsController.update()

    def on_cleanup(self):
        pg.quit()
        sys.exit()

    def on_render(self):
        self.screen.fill((0,0,0))

        # sem sprite ainda
        self.background.draw(self.screen, self.player)

        self.players.update()

        self.ObjectsController.draw()

        self.cross_rect = self.CROSS_IMAGE.get_rect(center = pg.mouse.get_pos())
        self.screen.blit(self.CROSS_IMAGE, self.cross_rect)

        self.light.draw(self.screen)
        self.stats.draw(self.screen)
        
        self.display_fps()
        pg.display.update()

    def on_execute(self):
        self.on_init()

        while (self._running):
            self.on_event(pg.event.get())
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    Main().on_execute()
