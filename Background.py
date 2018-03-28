import pygame as pg
from helpers import *
from ExtendedGroup import *
from Collider import *

class Background():
    def __init__(self):
        self.front = pg.image.load("Assets/Images/map-min.jpg").convert_alpha()
        self.back = pg.image.load("Assets/Images/map_back-min.png").convert_alpha()
        self.rect = self.front.get_rect()
        self.mask = pg.mask.from_surface(self.back)

        # rects representing walls
        self.corner_list = BACKGROUND_RECTS
        self.rect_list = transform_corners_to_rects(self.corner_list)
        self.collider_group = None #keep all walls
        self.create_group()

    def draw(self, surface, player):
        self.update_position(player)
        surface.blit(self.front, self.rect)
        # draw_rect_list(surface, self.rect_list, self.rect.topleft)
        # surface.blit(self.back, self.rect)

    def update_position(self, player):
        self.rect.center = background_center_position(player.position_on_screen, player.position_on_scenario)

    def create_group(self):
        self.collider_group = ExtendedGroup()
        for rect in self.rect_list:
            collider = Collider(rect, self.rect, None)
            self.collider_group.add(collider)
            