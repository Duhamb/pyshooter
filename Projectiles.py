import pygame as pg

class Projectiles(pg.sprite.Sprite):
    def __init__(self, origin_scenario, origin_screen, image, background):
        pg.sprite.Sprite.__init__(self)

        self.background = background
        self.mask = pg.mask.from_surface(image)
        self.player_position = pg.math.Vector2(origin_screen)

        #Start position correction
        self.direction = pg.mouse.get_pos() - self.player_position
        self.direction2 = self.direction.rotate(90)
        self.position_on_screen = pg.math.Vector2(origin_screen)+75*self.direction.normalize()+13*self.direction2.normalize()
        self.position_on_scenario = pg.math.Vector2(origin_scenario)+75*self.direction.normalize()+13*self.direction2.normalize()

        self.image = image
        self.rect = self.image.get_rect(center=self.position_on_screen)

        #Angle correction
        _, angle = (pg.mouse.get_pos() - self.player_position).as_polar()
        self.image = pg.transform.rotozoom(self.image, -angle, 1)

        self.distance = 0
        self.is_colliding = False

    def is_possible_direction(self):
        self.next_position_on_scenario = self.position_on_scenario + 10 * self.direction.normalize()

        self.next_rect = self.image.get_rect(center=self.position_on_screen)
        self.next_mask = pg.mask.from_surface(self.image)

        self.next_rect_background = self.background.rect.copy()

        # this command obtain the next position of background
        self.next_rect_background.center = self.position_on_screen - self.position_on_scenario

        self.offset = ((self.next_rect.left - self.next_rect_background.left), (self.next_rect.top - self.next_rect_background.top))

        self.is_colliding = self.background.mask.overlap(self.next_mask, self.offset)
        if self.is_colliding:
            return True
        return False

    def update(self):
        self.is_possible_direction()
        self.position_on_screen += 10 * self.direction.normalize()
        self.position_on_scenario = self.next_position_on_scenario

        self.distance += 10
        self.rect.center = self.position_on_screen
