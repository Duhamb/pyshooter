import pygame as pg
from helpers import *
# acho melhor essa ficar sem herança da sprite enquanto não resolver a colisão

class Background():
    def __init__(self):
        self.front = pg.image.load("Assets/Images/map-min.jpg").convert_alpha()
        self.back = pg.image.load("Assets/Images/map_back-min.png").convert_alpha()
        self.rect = self.front.get_rect()
        self.mask = pg.mask.from_surface(self.back)

        self.rect_list = self.get_rects_from_mask(self.mask)
        print('passou')

    def draw(self, surface, player):
        self.update_position(player)
        
        surface.blit(self.front, self.rect)

        draw_rect_list(surface, self.rect_list)
        # surface.blit(self.back, self.rect)

    def update_position(self, player):
        self.rect.center = background_center_position(player.position_on_screen, player.position_on_scenario)

    def get_rects_from_mask(self, mask):
        mask_list = mask.connected_components()
        print("agora")
        rect_list = []
        for mask in mask_list:
            temp_rect = mask.get_bounding_rects()
            rect_list.append(temp_rect)
        return rect_list