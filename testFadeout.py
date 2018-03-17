from pygame.locals import *
import pygame
import os
import sys


pygame.init()

CAPTION = "TEST"

class Game():
    def __init__(self):
        #window setup
        pygame.display.set_caption(CAPTION)
        os.environ["SDL_VIDEO_CENTERED"] = "True"
        self.fps = 60.0

        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [200, 200]

        self.screen = pygame.display.set_mode(self.screen_res,pygame.HWSURFACE)

        self.rect = pygame.Surface((100, 100))
        self.rect.fill((250, 0,0))

        self.alpha = 1
        self.a_change = True
        #Tweak this to change speed
        self.blink_spd = 0.1

        #start loop
        self.clock.tick(self.fps)
        while 1:
            self.Loop()

    def Loop(self):
        # main game loop
        self.eventLoop()

        self.last_tick = pygame.time.get_ticks()

        self.screen.fill((0,0,0))
        #Check if alpha is going up
        if self.a_change:
            self.alpha += self.blink_spd
            if self.alpha >= 175:#if all the way up go down
                self.a_change = False
        #Check if alpha is going down        
        elif self.a_change == False:
            self.alpha += -self.blink_spd
            if self.alpha <= 30: #if all the way down go up
                self.a_change = True

        self.rect.set_alpha(self.alpha)
        self.screen.blit(self.rect,(50,50))

        pygame.display.update()


    def eventLoop(self):
        # the main event loop, detects keypresses
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

Game()