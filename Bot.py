import pygame as pg

class Bot(pg.sprite.Sprite):
    def __init__(self, image, location_on_scenario, surface, background, player):
        super().__init__()
        self.image = pg.transform.rotate(image, 90)
        self.original_image = image
        self.rect = self.image.get_rect()
        self.player = player
        self.background = background
        self.surface = surface
        self.position_on_scenario = pg.math.Vector2(location_on_scenario)

    def update(self):
        self.rotate(self.player)
        self.rect.center = self.position_on_scenario + self.background.rect.center

    def rotate(self, player):
        _, angle = (self.player.position_on_scenario-self.position_on_scenario).as_polar()
        self.image = pg.transform.rotozoom(self.original_image, -angle, 1)
