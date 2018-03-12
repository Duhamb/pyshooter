import pygame as pg
from helpers import *
# acho melhor essa ficar sem herança da sprite enquanto não resolver a colisão

class Background():
    def __init__(self):
        self.front = pg.image.load("Assets/Images/city1.jpg").convert_alpha()
        self.back = pg.image.load("Assets/Images/city1_back.png").convert_alpha()
        self.rect = self.front.get_rect()
        self.mask = pg.mask.from_surface(self.back)

    def draw(self, surface, player):
        self.update_position(player)
   
        surface.blit(self.front, self.rect)
        # surface.blit(self.back, self.rect)

    def update_position(self, player):
        self.rect.center = background_center_position(player.position_on_screen, player.position_on_scenario)

