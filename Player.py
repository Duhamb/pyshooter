import pygame as pg

class Player():
    def __init__(self, image, location_on_scenario, location_on_screen):
        self.image = pg.transform.rotate(image, 90)
        self.original_image = image
        self.rect = self.image.get_rect(center=location_on_screen)
        self.position_on_screen = pg.math.Vector2(location_on_screen)
        self.position_on_scenario = pg.math.Vector2(location_on_scenario)

    def draw(self, surface):
        self.update()
        surface.blit(self.image, self.rect)

    def update(self):
        self.rotate()
        self.rect.center = self.position_on_screen

    def move(self, direction):
        self.position_on_scenario += 5*(direction/direction.length())

    def rotate(self):
        _, angle = (pg.mouse.get_pos()-self.position_on_screen).as_polar()
        self.image = pg.transform.rotozoom(self.original_image, -angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)