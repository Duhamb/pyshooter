import pygame as pg

class Player():
    def __init__(self, image, location):
        self.image = pg.transform.rotate(image, 90)
        self.original_image = image
        self.rect = self.image.get_rect(center=location)
        self.position = pg.math.Vector2(location)
        self.position = pg.math.Vector2(location)
        self.light = pg.image.load("circle.png")

    def draw(self, surface):
        self.update()
        surface.blit(self.image, self.rect)

    def update(self):
        self.rotate()
        self.rect.center = self.position

    def rotate(self):
        _, angle = (pg.mouse.get_pos()-self.position).as_polar()
        self.image = pg.transform.rotozoom(self.original_image, -angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)