import pygame as pg

class Projectiles(pg.sprite.Sprite):
    def __init__(self, origin, image):
        pg.sprite.Sprite.__init__(self)

        self.mask = pg.mask.from_surface(image)
        self.player_position = pg.math.Vector2(origin)

        #Start position correction
        self.direction = pg.mouse.get_pos() - self.player_position
        self.direction2 = self.direction.rotate(90)
        self.position_on_screen = pg.math.Vector2(origin)+75*self.direction.normalize()+13*self.direction2.normalize()
        self.position_on_scenario = pg.math.Vector2(origin)

        self.image = image
        self.rect = self.image.get_rect(center=self.position_on_screen)

        #Angle correction
        _, angle = (pg.mouse.get_pos() - self.player_position).as_polar()
        self.image = pg.transform.rotozoom(self.image, -angle, 1)

        self.distance = 0

    def update(self):
        self.position_on_screen += 10 * self.direction.normalize()
        self.distance += 10
        self.rect.center = self.position_on_screen
