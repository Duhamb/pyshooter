import pygame as pg

class Menu():
    def __init__(self):
        self._in_menu = True
        self.MENU_IMAGE = pg.image.load("Assets/Images/menu/background.png")
        self.MENU_IMAGE = pg.transform.scale(self.MENU_IMAGE, (800, 600))

    def on_render(self):
        pg.display.update()

    def on_event(self, event):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            self._in_menu = False
        if event.type == pg.KEYDOWN:
            self._in_menu = False

    def intro(self):
        self.surface = pg.display.get_surface()
        self.surface.blit(self.MENU_IMAGE, (0, 0))
        while(self._in_menu):
            for event in pg.event.get():
                self.on_event(event)
            self.on_render()