import pygame as pg 
from helpers import *

class Player:
    move = []
    shoot = []
    idle = []
    rifle_reload = []
    
    feet_walk = []
    feet_idle = []
    feet_strafe_left = []
    feet_strafe_right = []

    @classmethod
    def load(cls):
        
        default_directory = 'Assets/Images/player/rifle/move/survivor-move_rifle_'
        extension_file = '.png'
        cls.move = load_image_list(default_directory, extension_file, 20)
        cls.move = scale_image_list(cls.move, 2.7)

        default_directory = 'Assets/Images/player/rifle/shoot/survivor-shoot_rifle_'
        extension_file = '.png'
        cls.shoot = load_image_list(default_directory, extension_file, 3)
        cls.shoot = scale_image_list(cls.shoot, 2.7)

        default_directory = 'Assets/Images/player/rifle/idle/survivor-idle_rifle_'
        extension_file = '.png'
        cls.idle = load_image_list(default_directory, extension_file, 20)
        cls.idle = scale_image_list(cls.idle, 2.7)

        default_directory = 'Assets/Images/player/rifle/reload/survivor-reload_rifle_'
        extension_file = '.png'
        cls.rifle_reload = load_image_list(default_directory, extension_file, 20)
        cls.rifle_reload = scale_image_list(cls.rifle_reload, 2.7)


        default_directory = 'Assets/Images/player/feet/strafe_left/survivor-strafe_left_'
        extension_file = '.png'
        cls.feet_strafe_left = load_image_list(default_directory, extension_file, 20)
        cls.feet_strafe_left = scale_image_list(cls.feet_strafe_left, 2.7)

        default_directory = 'Assets/Images/player/feet/strafe_right/survivor-strafe_right_'
        extension_file = '.png'
        cls.feet_strafe_right = load_image_list(default_directory, extension_file, 20)
        cls.feet_strafe_right = scale_image_list(cls.feet_strafe_right, 2.7)

        default_directory = 'Assets/Images/player/feet/walk/survivor-walk_'
        extension_file = '.png'
        cls.feet_walk = load_image_list(default_directory, extension_file, 20)
        cls.feet_walk = scale_image_list(cls.feet_walk, 2.7)

        default_directory = 'Assets/Images/player/feet/idle/survivor-idle_'
        extension_file = '.png'
        cls.feet_idle = load_image_list(default_directory, extension_file, 1)
        cls.feet_idle = scale_image_list(cls.feet_idle, 2.7)

class Zombie:

    idle = []
    move = []
    attack = []
    @classmethod
    def load(cls):
        default_directory = 'Assets/Images/zombie/idle/skeleton-idle_'
        extension_file = '.png'
        cls.idle = load_image_list(default_directory, extension_file, 17)
        cls.idle = scale_image_list(cls.idle, 2.7)

        default_directory = 'Assets/Images/zombie/move/skeleton-move_'
        extension_file = '.png'
        cls.move = load_image_list(default_directory, extension_file, 17)
        cls.move = scale_image_list(cls.move, 2.7)

        default_directory = 'Assets/Images/zombie/attack/skeleton-attack_'
        extension_file = '.png'
        cls.attack = load_image_list(default_directory, extension_file, 9)
        cls.attack = scale_image_list(cls.attack, 2.7)


     # @staticmethod
     # @classmethod
     # def class_method(cls):
     #     # the class method gets passed the class (in this case ModCLass)
     #     return "I am a class method"
     # def instance_method(self):
     #     # An instance method gets passed the instance of ModClass
     #     return "I am an instance method"