import os
import sys
import pygame as pg

import Code.Menu as Menu
import Code.Player as Player
import Code.Background as Background
import Code.Statistics as Statistics
import Code.Light as Light
import Code.ObjectsController as ObjectsController
import Code.Aim as Aim
import Code.ExtendedGroup as ExtendedGroup
import Code.helpers as helpers
import Code.constants as constants
import Code.Animation as Animation
import Code.Sound as Sound

###############################################
class Main:
    def __init__(self):
        self._running = True
        self.is_focused = True
        self.size = self.width, self.height = constants.SCREEN_SIZE
        self.fps = constants.FPS
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
        self.menu = Menu.Menu()

        self._display_surf = pg.display.set_mode(self.size)
        self.screen = pg.display.get_surface() # repetido?

        #initialize "loading menu"
        self.ICON = pg.image.load("Assets/Images/cross.png")
        self.ICON = pg.transform.scale(self.ICON, (32, 32))
        self.screen.blit(self.menu.MENU_IMAGE, (0, 0))
        pg.display.update()
        pg.display.set_caption("Pyshooter")
        pg.display.set_icon(self.ICON)

        #call menu Displays/Loops
        self.menu.intro()

        self.server_client = None
        self.is_host = None

        #Get informations about multiplayer/singleplayer
        #Observation is_host is True on Singleplayer
        self.multiplayer_on = self.menu.have_client
        if self.multiplayer_on:
            self.server_client = self.menu.server_client
            self.is_host = self.menu.is_host
        else:
            self.is_host = True

        self.aim = Aim.Aim()
        self.background = Background.Background(self.aim)

        #Set mouse invisible
        pg.mouse.set_visible(0)

        #Define Objects Controller
        self.ObjectsController = ObjectsController.ObjectsController(self.background,self.multiplayer_on, self.server_client, self.menu, self.is_host, self.aim)

        self.light = Light.Light(self.ObjectsController.player)
        self.stats = Statistics.Statistics(self.ObjectsController.player, constants.SCREEN_SIZE, self.multiplayer_on, self.server_client,
                                           self.is_host)

    def on_event(self, event_queue):
        for event in event_queue:
            if event.type == pg.QUIT:
                self._running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.is_focused = False
                pg.mouse.set_visible(1)
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.is_focused = True
                    pg.mouse.set_visible(0)

            self.ObjectsController.handle_event(event)

    def display_fps(self):
        pg.display.set_caption("{} - FPS: {:.2f}".format("PyShooter", self.clock.get_fps()))

    def on_loop(self):
        self.clock.tick(self.fps)
        self.ObjectsController.update()
        self.aim.update(self.is_focused)

    def on_cleanup(self):
        pg.quit()
        sys.exit()

    def on_render(self):
        self.screen.fill(constants.BLACK)
        self.background.draw(self.screen, self.ObjectsController.player)
        self.ObjectsController.draw()
        self.aim.draw(self.screen)
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

        if self.multiplayer_on:
            self.server_client.delete_player()
            self.server_client.pull_players()
            self.server_client.scores.pop(self.menu.name, None)

        self.on_cleanup()

if __name__ == "__main__":
    Main().on_execute()
