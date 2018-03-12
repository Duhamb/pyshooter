import os
import sys
import pygame as pg

from Menu import *
from Player import *
from Background import *
from Bot import *
from Projectiles import *

import Animation
import Sound

###############################################

class Main:
    def __init__(self):
        self._running = True
        self.size = self.width, self.height = 800, 600
        self.fps = 60
        self.pressionou_w = False
        self.pressionou_a = False
        self.pressionou_s = False
        self.pressionou_d = False

    
    def on_init(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pg.mixer.pre_init(frequency=44100, size=0, channels=1, buffer=4096) #size - 16, channels 2
        pg.mixer.init()
        pg.init()
        self._running = True
        self.clock = pg.time.Clock()

        # self.resolution = (int(pg.display.Info().current_w), int(pg.display.Info().current_h))

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
        
        self.BACK_IMAGE = pg.image.load("Assets/Images/map_back.png").convert_alpha()
        self.FRONT_IMAGE = pg.image.load("Assets/Images/map.jpg").convert_alpha()

        self.CROSS_IMAGE = pg.image.load("Assets/Images/cross.png").convert_alpha()
        self.CROSS_IMAGE = pg.transform.scale(self.CROSS_IMAGE, (15,15))
        
        self.player_animation = Animation.Player
        self.player_animation.load()
        self.player_sound = Sound.Player 
        self.player_sound.load()

        self.back = Background(self.BACK_IMAGE, self.FRONT_IMAGE)
        self.player = Player(self.PLAY_IMAGE, self.PLAY_IMAGE_BACK, (0,-1400), self.PLAYER_POSITION, self.player_animation, self.player_sound, self.back)
        self.bot0 = Bot(self.BOT_IMAGE, (200,200), self.screen, self.back, self.player)

        self.players = pg.sprite.Group(self.player)
        self.bots = pg.sprite.Group(self.bot0)

        self.bullet_list = pg.sprite.Group()
        self.BULLET_IMAGE = pg.image.load("Assets/Images/bullets/bullet1.png")
        self.BULLET_IMAGE = pg.transform.scale(self.BULLET_IMAGE, (15, 3))

    def on_event(self, event):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            self._running = False

        # o grupo deveria chamar esses metodos também
        self.player.handle_event(event)
        
        if self.player.is_shooting == True:
            bullet = Projectiles(self.player.position_on_screen, self.BULLET_IMAGE)
            self.bullet_list.add(bullet)
        
    def display_fps(self):
        pg.display.set_caption("{} - FPS: {:.2f}".format("PyShooter", self.clock.get_fps()))

    def on_loop(self):
        self.clock.tick(self.fps)

        for bullet in self.bullet_list:
            if bullet.distance > 300:
                self.bullet_list.remove(bullet)

    def on_cleanup(self):
        pg.quit()
        sys.exit()

    def on_render(self):
        self.screen.fill((0,0,0))
        # sem sprite ainda
        self.back.draw(self.screen, self.player)

        # como que atualiza todos os grupos?
        self.players.update()
        self.players.draw(self.screen)
        self.bots.update()
        self.bots.draw(self.screen)

        self.bullet_list.draw(self.screen)
        self.bullet_list.update()

        # acho que não precisa de sprite pra essa
        self.screen.blit(self.CROSS_IMAGE, pg.mouse.get_pos())
        
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
