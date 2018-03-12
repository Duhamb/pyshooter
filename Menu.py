import pygame as pg
import time
from NetworkSettings import *
import NetworkServer
from pyshooterClient import *

class Menu():
    def __init__(self):
        self._in_menu = True
        self._in_menu_multiplayer = False
        self.MENU_IMAGE = pg.image.load("Assets/Images/menu/background.png")
        self.MENU_IMAGE = pg.transform.scale(self.MENU_IMAGE, (800, 600))
        self.SINGLE_OFF = pg.image.load("Assets/Images/menu/button_singleplayer_off.png")
        self.SINGLE_OFF = pg.transform.scale(self.SINGLE_OFF, (200, 50))
        self.SINGLE_ON = pg.image.load("Assets/Images/menu/button_singleplayer_on.png")
        self.SINGLE_ON = pg.transform.scale(self.SINGLE_ON, (200, 50))
        self.MULTI_OFF = pg.image.load("Assets/Images/menu/button_multiplayer_off.png")
        self.MULTI_OFF = pg.transform.scale(self.MULTI_OFF, (200, 50))
        self.MULTI_ON = pg.image.load("Assets/Images/menu/button_multiplayer_on.png")
        self.MULTI_ON = pg.transform.scale(self.MULTI_ON, (200, 50))
        self.SERVER_OFF = pg.image.load("Assets/Images/menu/button_create_server_off.png")
        self.SERVER_OFF = pg.transform.scale(self.SERVER_OFF, (200, 50))
        self.SERVER_ON = pg.image.load("Assets/Images/menu/button_create_server_on.png")
        self.SERVER_ON = pg.transform.scale(self.SERVER_ON, (200, 50))
        self.CONNECT_OFF = pg.image.load("Assets/Images/menu/button_connect_off.png")
        self.CONNECT_OFF = pg.transform.scale(self.CONNECT_OFF, (200, 50))
        self.CONNECT_ON = pg.image.load("Assets/Images/menu/button_connect_on.png")
        self.CONNECT_ON = pg.transform.scale(self.CONNECT_ON, (200, 50))

        self.have_client = False

    def on_render(self):
        pg.display.update()

    def on_event(self, event):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            self._in_menu = False
            self._in_menu_multiplayer = False
        if event.type == pg.KEYDOWN:
            self._in_menu = False
            self._in_menu_multiplayer = False

    def interactive(self, event):
        mouse = pg.mouse.get_pos()

        if 150+200 > mouse[0] > 150 and 450+50 > mouse[1] > 450:
            self.surface.blit(self.SINGLE_ON, (150, 450))
            if event.type == pg.MOUSEBUTTONDOWN:
                self._in_menu = False
        else:
            self.surface.blit(self.SINGLE_OFF, (150, 450))

        if 450+200 > mouse[0] > 450 and 450+50 > mouse[1] > 450:
            self.surface.blit(self.MULTI_ON, (450, 450))
            if event.type == pg.MOUSEBUTTONDOWN:
                self._in_menu = False
                self._in_menu_multiplayer = True

        else:
            self.surface.blit(self.MULTI_OFF, (450, 450))

    def interactive_multiplayer(self, event):
        mouse = pg.mouse.get_pos()

        if 150 + 200 > mouse[0] > 150 and 450 + 50 > mouse[1] > 450:
            self.surface.blit(self.SERVER_ON, (150, 450))
            if event.type == pg.MOUSEBUTTONDOWN:
                self.server_client = pyshooterClient('Name')
                self.server_client.start()
                self.have_client = True
                self._in_menu_multiplayer = False
        else:
            self.surface.blit(self.SERVER_OFF, (150, 450))

        if 450 + 200 > mouse[0] > 450 and 450 + 50 > mouse[1] > 450:
            self.surface.blit(self.CONNECT_ON, (450, 450))
            if event.type == pg.MOUSEBUTTONDOWN:
                self._in_menu_multiplayer = False
        else:
            self.surface.blit(self.CONNECT_OFF, (450, 450))

    def intro(self):
        self.surface = pg.display.get_surface()
        self.surface.blit(self.MENU_IMAGE, (0, 0))

        self.music = pg.mixer.Sound('Assets/Sounds/BestMusic.wav')
        self.music.set_volume(0.5)
        self.music.play()

        while(self._in_menu):
            for event in pg.event.get():
                self.on_event(event)
                self.interactive(event)
            self.on_render()

        button_up = True
        while (button_up):
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    button_up = False

        while(self._in_menu_multiplayer):
            for event in pg.event.get():
                self.on_event(event)
                self.interactive_multiplayer(event)
            self.on_render()
        self.music.stop()
