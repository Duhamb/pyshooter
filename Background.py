import pygame as pg
from helpers import *
from ExtendedGroup import *
from Collider import *

class Background():
    def __init__(self):
        self.front = pg.image.load("Assets/Images/map-min.jpg").convert_alpha()
        self.back = pg.image.load("Assets/Images/map_back-min.png").convert_alpha()
        self.rect = self.front.get_rect()
        self.size = self.rect.size
        self.mask = pg.mask.from_surface(self.back)

        self.crop_size = (400,400)

        # rects representing walls
        self.corner_list = BACKGROUND_RECTS
        self.rect_list = transform_corners_to_rects(self.corner_list)
        self.collider_group = None #keep all walls
        self.create_group()

        # coordinates
        self.x_axis = pg.math.Vector2((1,0))
        self.y_axis = pg.math.Vector2((0,1))
        self.origin_axis = pg.math.Vector2((0,0)) #arbitrary value at constructor

        self.player_position_on_scenario = None

    def draw(self, surface, player):
        self.update_position(player)
        # surface.blit(self.front, self.rect)
        self.define_area()
        surface.blit(self.area, self.area_rect)
        
        # debugger draws
        pg.draw.circle(surface, (255,0,0), to_int(self.origin_axis), 15, 5)
        x = self.origin_axis + 50*self.x_axis
        y = self.origin_axis + 50*self.y_axis
        pg.draw.line(surface, (0,255,0), to_int(self.origin_axis), to_int(x), 2)
        pg.draw.line(surface, (0,25,0), to_int(self.origin_axis), to_int(y), 2)


    def update_position(self, player):
        self.rect.center = background_center_position(player.position_on_screen, player.position_on_scenario)
        self.origin_axis = pg.math.Vector2(self.rect.center)
        self.player_position_on_scenario = player.position_on_scenario

    def create_group(self):
        self.collider_group = ExtendedGroup()
        for rect in self.rect_list:
            collider = Collider(rect, self.rect, None)
            self.collider_group.add(collider)
            
    def define_area(self):
        self.area = pg.Surface(self.crop_size)
        crop_area = (self.player_position_on_scenario[0]+self.size[0]/2-self.crop_size[0]/2, self.player_position_on_scenario[1]+self.size[1]/2-self.crop_size[1]/2, self.crop_size[0], self.crop_size[1])
        self.area.blit(self.front, (0,0), crop_area) 
  
        self.area_rect = self.area.get_rect(center=(400,300))