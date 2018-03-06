import pygame as pg

class Projectiles(pg.sprite.Sprite):
    def __init__(self, origin, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=origin)
        self.mask = pg.mask.from_surface(image)
        self.position_on_screen = pg.math.Vector2(origin)
        self.position_on_scenario = pg.math.Vector2(origin)
        self.direction = pg.mouse.get_pos() - self.position_on_screen

    def update(self):
        self.position_on_screen += 1 * (self.direction / self.direction.length())