from helpers import *
import math

class Projectiles(pg.sprite.Sprite):
    def __init__(self, origin_scenario, origin_screen, image, background):
        pg.sprite.Sprite.__init__(self)

        self.background = background
        self.mask = pg.mask.from_surface(image)
        self.player_position = pg.math.Vector2(origin_screen)

        # vector between player head and rifle
        self.vector_offset = pg.math.Vector2((172.5/2.7, 32/2.7))

        #Angle correction
        _, angle = (pg.mouse.get_pos() - self.player_position).as_polar()
        try:
            D = (pg.mouse.get_pos()-self.player_position).length()
            add_angle = math.degrees(math.asin(32/(2.7*D)))
            angle -= add_angle
        except:
            pass
        
        correction_angle = math.degrees(math.atan(32/172))
        self.direction = self.vector_offset.rotate(angle-correction_angle)

        #Start position correction
        self.new_vector = self.vector_offset.rotate(angle)
        self.position_on_screen = self.player_position + self.new_vector
        self.position_on_scenario = screen_to_scenario(self.position_on_screen, self.background.rect)

        self.image = image
        self.image = pg.transform.rotozoom(self.image, -angle, 1)
        self.rect = self.image.get_rect(center=self.position_on_screen)

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
