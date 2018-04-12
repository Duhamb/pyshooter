import pygame as pg
import helpers
import constants
from ExtendedGroup import *
from Collider import *

class Background():
    def __init__(self, aim):
        self.front = pg.image.load("Assets/Images/map-min.jpg").convert_alpha()
        self.back = pg.image.load("Assets/Images/map_back-min.png").convert_alpha()
        self.rect = self.front.get_rect()
        self.size = self.rect.size
        self.mask = pg.mask.from_surface(self.back)

        self.crop_size = (2*constants.VISIBLE_RADIUS, 2*constants.VISIBLE_RADIUS)

        # rects representing walls
        self.corner_list = constants.BACKGROUND_RECTS
        self.rect_list = helpers.transform_corners_to_rects(self.corner_list)
        self.collider_group = self.create_group()

        # coordinates
        self.x_axis = pg.math.Vector2((1,0))
        self.y_axis = pg.math.Vector2((0,1))
        self.origin_axis = pg.math.Vector2((0,0)) #arbitrary value at constructor
        self.angle = 0
        self.turn_velocity = -4
        self.player_position_on_scenario = None
        self.last_mouse_position = constants.MOUSE_POSITION_SCREEN

        self.aim = aim

    def draw(self, surface, player):
        self.update_position(player)
        self.define_area()
        surface.blit(self.area, self.area_rect)
 
    def update_position(self, player):
        self.update_angle()
        self.rect.center = helpers.background_center_position(player.position_on_screen, player.position_on_scenario, self.turn_velocity*self.angle)
        self.origin_axis = self.rect.center
        self.x_axis = pg.math.Vector2((1,0))
        self.y_axis = pg.math.Vector2((0,1)) 
   
        self.x_axis.rotate_ip(self.turn_velocity*(self.angle))
        self.y_axis.rotate_ip(self.turn_velocity*(self.angle))

        self.player_position_on_scenario = player.position_on_scenario

    def create_group(self):
        collider_group = ExtendedGroup()
        for rect in self.rect_list:
            collider = Collider(rect, self.rect, None)
            collider_group.add(collider)
        return collider_group
            
    def define_area(self):
        self.area = pg.Surface(self.crop_size)
        crop_area = (self.player_position_on_scenario[0]+self.size[0]/2-self.crop_size[0]/2, self.player_position_on_scenario[1]+self.size[1]/2-self.crop_size[1]/2, self.crop_size[0], self.crop_size[1])
        self.area.blit(self.front, (0,0), crop_area) 
        self.area = pg.transform.rotate(self.area, -self.turn_velocity*(self.angle))
        self.area_rect = self.area.get_rect(center=constants.PLAYER_POSITION_SCREEN)

    def update_angle(self):
        if self.aim.is_focused:
            actual_mouse_position = pg.mouse.get_pos()
            delta_position = actual_mouse_position[0] - self.last_mouse_position[0]
            self.last_mouse_position = constants.MOUSE_POSITION_SCREEN
            step = 8
            self.angle += (delta_position/step)
