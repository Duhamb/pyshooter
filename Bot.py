import pygame as pg

class Bot():
    def __init__(self, image, location_on_scenario):
        self.image = pg.transform.rotate(image, 90)
        self.original_image = image
        self.rect = self.image.get_rect()
        # self.position_on_screen = pg.math.Vector2(location_on_screen)
        self.position_on_scenario = pg.math.Vector2(location_on_scenario)

    def draw(self, surface, back, player):
        self.update(back, player)
        surface.blit(self.image, self.rect)

    def update(self, back, player):
        self.rotate(player)
        self.rect.center = self.position_on_scenario + back.rect.center

    # def move(self, direction):
    #     self.position_on_scenario += 10*(direction/direction.length())

    def rotate(self, player):
        _, angle = (player.position_on_scenario-self.position_on_scenario).as_polar()
        self.image = pg.transform.rotozoom(self.original_image, -angle, 1)
        # self.rect = self.image.get_rect(center=self.rect.center)