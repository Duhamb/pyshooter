import pygame as pg 
from helpers import *
import constants

class Player:
    rifle_move = []
    rifle_shoot = []
    rifle_idle = []
    rifle_reload = []
    rifle_meleeattack = []

    shotgun_move = []
    shotgun_shoot = []
    shotgun_idle = []
    shotgun_reload = []
    shotgun_meleeattack = []
    
    feet_walk = []
    feet_idle = []
    feet_strafe_left = []
    feet_strafe_right = []

    @classmethod
    def load(cls):
        #---------------------------------------------------------------------------
        default_directory = 'Assets/Images/player/rifle/move/survivor-move_rifle_'
        extension_file = '.png'
        cls.rifle_move = load_image_list(default_directory, extension_file, 20)
        cls.rifle_move = scale_image_list(cls.rifle_move, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/rifle/shoot/survivor-shoot_rifle_'
        extension_file = '.png'
        cls.rifle_shoot = load_image_list(default_directory, extension_file, 3)
        cls.rifle_shoot = scale_image_list(cls.rifle_shoot, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/rifle/idle/survivor-idle_rifle_'
        extension_file = '.png'
        cls.rifle_idle = load_image_list(default_directory, extension_file, 20)
        cls.rifle_idle = scale_image_list(cls.rifle_idle, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/rifle/reload/survivor-reload_rifle_'
        extension_file = '.png'
        cls.rifle_reload = load_image_list(default_directory, extension_file, 20)
        cls.rifle_reload = scale_image_list(cls.rifle_reload, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/rifle/meleeattack/survivor-meleeattack_rifle_'
        extension_file = '.png'
        cls.rifle_meleeattack = load_image_list(default_directory, extension_file, 15)
        cls.rifle_meleeattack = scale_image_list(cls.rifle_meleeattack, constants.SCALE_RATIO)
        #---------------------------------------------------------------------------

        #---------------------------------------------------------------------------
        default_directory = 'Assets/Images/player/shotgun/move/survivor-move_shotgun_'
        extension_file = '.png'
        cls.shotgun_move = load_image_list(default_directory, extension_file, 20)
        cls.shotgun_move = scale_image_list(cls.shotgun_move, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/shotgun/shoot/survivor-shoot_shotgun_'
        extension_file = '.png'
        cls.shotgun_shoot = load_image_list(default_directory, extension_file, 3)
        cls.shotgun_shoot = scale_image_list(cls.shotgun_shoot, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/shotgun/idle/survivor-idle_shotgun_'
        extension_file = '.png'
        cls.shotgun_idle = load_image_list(default_directory, extension_file, 20)
        cls.shotgun_idle = scale_image_list(cls.shotgun_idle, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/shotgun/reload/survivor-reload_shotgun_'
        extension_file = '.png'
        cls.shotgun_reload = load_image_list(default_directory, extension_file, 20)
        cls.shotgun_reload = scale_image_list(cls.shotgun_reload, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/shotgun/meleeattack/survivor-meleeattack_shotgun_'
        extension_file = '.png'
        cls.shotgun_meleeattack = load_image_list(default_directory, extension_file, 15)
        cls.shotgun_meleeattack = scale_image_list(cls.shotgun_meleeattack, constants.SCALE_RATIO)
        #---------------------------------------------------------------------------

        default_directory = 'Assets/Images/player/feet/strafe_left/survivor-strafe_left_'
        extension_file = '.png'
        cls.feet_strafe_left = load_image_list(default_directory, extension_file, 20)
        cls.feet_strafe_left = scale_image_list(cls.feet_strafe_left, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/feet/strafe_right/survivor-strafe_right_'
        extension_file = '.png'
        cls.feet_strafe_right = load_image_list(default_directory, extension_file, 20)
        cls.feet_strafe_right = scale_image_list(cls.feet_strafe_right, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/feet/walk/survivor-walk_'
        extension_file = '.png'
        cls.feet_walk = load_image_list(default_directory, extension_file, 20)
        cls.feet_walk = scale_image_list(cls.feet_walk, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/feet/idle/survivor-idle_'
        extension_file = '.png'
        cls.feet_idle = load_image_list(default_directory, extension_file, 1)
        cls.feet_idle = scale_image_list(cls.feet_idle, constants.SCALE_RATIO)

class Zombie:

    idle = []
    move = []
    attack = []
    @classmethod
    def load(cls):
        default_directory = 'Assets/Images/zombie/idle/skeleton-idle_'
        extension_file = '.png'
        cls.idle = load_image_list(default_directory, extension_file, 17)
        cls.idle = scale_image_list(cls.idle, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/zombie/move/skeleton-move_'
        extension_file = '.png'
        cls.move = load_image_list(default_directory, extension_file, 17)
        cls.move = scale_image_list(cls.move, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/zombie/attack/skeleton-attack_'
        extension_file = '.png'
        cls.attack = load_image_list(default_directory, extension_file, 9)
        cls.attack = scale_image_list(cls.attack, constants.SCALE_RATIO)


     # @staticmethod
     # @classmethod
     # def class_method(cls):
     #     # the class method gets passed the class (in this case ModCLass)
     #     return "I am a class method"
     # def instance_method(self):
     #     # An instance method gets passed the instance of ModClass
     #     return "I am an instance method"