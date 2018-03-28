import pygame as pg
from helpers import *

# IMPORTANT! All colliders are rects with positions based on background image
# background image has origin axis at topleft
class Collider(pg.sprite.Sprite):
    def __init__(self, rect, background_rect, screen):
        super().__init__()
        self.rect = rect.copy()
        self.background_rect = background_rect 

    def update(self, position_scenario):
        self.rect.center = scenario_to_image(position_scenario, self.background_rect)