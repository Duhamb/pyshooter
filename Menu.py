import pygame as pg

class Menu():
    def __init__(self):
        self._in_menu = True
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

    def on_render(self):
        pg.display.update()

    def on_event(self, event):
        if event.type == self.REPLAY:
            self.music.play()
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            self._in_menu = False
        if event.type == pg.KEYDOWN:
            self._in_menu = False

    def interactive(self):
        mouse = pg.mouse.get_pos()

        if 150+200 > mouse[0] > 150 and 450+50 > mouse[1] > 450:
            self.surface.blit(self.SINGLE_ON, (150, 450))
            if pg.mouse.get_pressed()[0]:
                self._in_menu = False
        else:
            self.surface.blit(self.SINGLE_OFF, (150, 450))

        if 450+200 > mouse[0] > 450 and 450+50 > mouse[1] > 450:
            self.surface.blit(self.MULTI_ON, (450, 450))
            if pg.mouse.get_pressed()[0]:
                self._in_menu = False
        else:
            self.surface.blit(self.MULTI_OFF, (450, 450))


    def intro(self):
        self.surface = pg.display.get_surface()
        self.surface.blit(self.MENU_IMAGE, (0, 0))

        self.music = pg.mixer.Sound('Assets/Sounds/BestMusic.wav')
        self.music.set_volume(0.5)
        self.music.play()
        self.REPLAY = pg.USEREVENT + 1
        pg.mixer.music.set_endevent(self.REPLAY)

        while(self._in_menu):
            for event in pg.event.get():
                self.on_event(event)
            self.interactive()
            self.on_render()

        self.music.stop()