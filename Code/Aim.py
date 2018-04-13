import pygame as pg
import Code.constants as constants
import Code.helpers as helpers
###############################################

class Aim:
    def __init__(self):
        self.CROSS_IMAGE = pg.image.load("Assets/Images/cross.png").convert_alpha()
        self.CROSS_IMAGE = pg.transform.scale(self.CROSS_IMAGE, (15,15))
        self.cross_rect = self.CROSS_IMAGE.get_rect(center = constants.MOUSE_POSITION_SCREEN)
        self.max_down = constants.MOUSE_POSITION_SCREEN[1] + 80
        self.max_up = constants.MOUSE_POSITION_SCREEN[1] - 100
        self.position = self.cross_rect.center

        self.is_focused = True

    def update(self, is_focused):
        self.is_focused = is_focused
        if self.is_focused:
            actual_mouse_position = pg.mouse.get_pos()
            delta_y = actual_mouse_position[1] - constants.MOUSE_POSITION_SCREEN[1] 
            if self.cross_rect.centery + delta_y <= self.max_down and self.cross_rect.centery + delta_y >= self.max_up:
                self.cross_rect.centery = self.cross_rect.centery + delta_y
            self.position = self.cross_rect.center
            pg.mouse.set_pos(constants.MOUSE_POSITION_SCREEN)

    def draw(self, screen):
        screen.blit(self.CROSS_IMAGE, self.cross_rect)
