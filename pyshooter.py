import os
import sys
import pygame as pg
from Player import *
from Background import *

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
        pg.init()
        self._running = True
        self.clock = pg.time.Clock()
        pg.mouse.set_visible(0)
        self.resolution = (int(pg.display.Info().current_w), int(pg.display.Info().current_h))
        
        self._display_surf = pg.display.set_mode(self.resolution, pg.FULLSCREEN) 
        self.screen = pg.display.get_surface() # repetido?
        
        self.PLAYER_POSITION = (self.width/2, self.height/2)
        self.PLAY_IMAGE = pg.image.load("player3.png")
        self.PLAY_IMAGE = pg.transform.scale(self.PLAY_IMAGE, (75,75))
        self.BACK_IMAGE = pg.image.load("city1_back.png").convert_alpha()
        self.FRONT_IMAGE = pg.image.load("city1.jpg").convert_alpha()
        self.CROSS_IMAGE = pg.image.load("cross.png").convert_alpha()
        self.CROSS_IMAGE = pg.transform.scale(self.CROSS_IMAGE, (15,15))
        
        self.player = Player(self.PLAY_IMAGE, self.PLAYER_POSITION)
        self.back = Background(self.BACK_IMAGE, self.FRONT_IMAGE, self.PLAYER_POSITION)

    def on_event(self, event):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            self._running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.pressionou_w = True
            if event.key == pg.K_a:
                self.pressionou_a = True
            if event.key == pg.K_s:
                self.pressionou_s = True
            if event.key == pg.K_d:
                self.pressionou_d = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_w:
                self.pressionou_w = False
            if event.key == pg.K_a:
                self.pressionou_a = False
            if event.key == pg.K_s:
                self.pressionou_s = False
            if event.key == pg.K_d:
                self.pressionou_d = False
        
    def display_fps(self):
        pg.display.set_caption("{} - FPS: {:.2f}".format("PyShooter", self.clock.get_fps()))

    def on_loop(self):
        self.actual_position = self.player.position
        self.mouse_position = pg.mouse.get_pos()
        self.vector_position = self.mouse_position - self.actual_position
        
        if self.pressionou_w:
            self.direction_of_move = -(self.vector_position)
            self.direction_of_move /= self.direction_of_move.length()
            self.back.move(self.direction_of_move)

        if self.pressionou_s:
            self.direction_of_move = +(self.vector_position)
            self.direction_of_move /= self.direction_of_move.length()
            self.back.move(self.direction_of_move)

        if self.pressionou_a:
            self.direction_of_move = +(self.vector_position).rotate(90)
            self.direction_of_move /= self.direction_of_move.length()
            self.back.move(self.direction_of_move)

        if self.pressionou_d:
            self.direction_of_move = -(self.vector_position).rotate(90)
            self.direction_of_move /= self.direction_of_move.length()
            self.back.move(self.direction_of_move)

        self.clock.tick(self.fps)

    def on_cleanup(self):
        pg.quit()
        sys.exit()

    def on_render(self):
        self.screen.fill((0,0,0))
        self.back.draw(self.screen)
        self.player.draw(self.screen)
        self.screen.blit(self.CROSS_IMAGE, pg.mouse.get_pos())
        self.display_fps()
        pg.display.update()

    def on_execute(self):
        self.on_init()
        while (self._running):
            for event in pg.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    Main().on_execute()
