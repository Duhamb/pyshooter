import pygame as pg 
import helpers
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
        # ---------------------------------------------------------------------------
        default_directory = 'Assets/Images/player/knife/move/survivor-move_knife_'
        extension_file = '.png'
        cls.knife_move = helpers.load_image_list(default_directory, extension_file, 20)
        cls.knife_move = helpers.scale_image_list(cls.knife_move, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/knife/idle/survivor-idle_knife_'
        cls.knife_idle = helpers.load_image_list(default_directory, extension_file, 20)
        cls.knife_idle = helpers.scale_image_list(cls.knife_idle, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/knife/meleeattack/survivor-meleeattack_knife_'
        cls.knife_meleeattack = helpers.load_image_list(default_directory, extension_file, 15)
        cls.knife_meleeattack = helpers.scale_image_list(cls.knife_meleeattack, constants.SCALE_RATIO)
        # ---------------------------------------------------------------------------

        #---------------------------------------------------------------------------
        default_directory = 'Assets/Images/player/rifle/move/survivor-move_rifle_'
        cls.rifle_move = helpers.load_image_list(default_directory, extension_file, 20)
        cls.rifle_move = helpers.scale_image_list(cls.rifle_move, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/rifle/shoot/survivor-shoot_rifle_'
        cls.rifle_shoot = helpers.load_image_list(default_directory, extension_file, 3)
        cls.rifle_shoot = helpers.scale_image_list(cls.rifle_shoot, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/rifle/idle/survivor-idle_rifle_'
        cls.rifle_idle = helpers.load_image_list(default_directory, extension_file, 20)
        cls.rifle_idle = helpers.scale_image_list(cls.rifle_idle, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/rifle/reload/survivor-reload_rifle_'
        cls.rifle_reload = helpers.load_image_list(default_directory, extension_file, 20)
        cls.rifle_reload = helpers.scale_image_list(cls.rifle_reload, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/rifle/meleeattack/survivor-meleeattack_rifle_'
        cls.rifle_meleeattack = helpers.load_image_list(default_directory, extension_file, 15)
        cls.rifle_meleeattack = helpers.scale_image_list(cls.rifle_meleeattack, constants.SCALE_RATIO)
        #---------------------------------------------------------------------------

        #---------------------------------------------------------------------------
        default_directory = 'Assets/Images/player/shotgun/move/survivor-move_shotgun_'
        cls.shotgun_move = helpers.load_image_list(default_directory, extension_file, 20)
        cls.shotgun_move = helpers.scale_image_list(cls.shotgun_move, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/shotgun/shoot/survivor-shoot_shotgun_'
        cls.shotgun_shoot = helpers.load_image_list(default_directory, extension_file, 3)
        cls.shotgun_shoot = helpers.scale_image_list(cls.shotgun_shoot, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/shotgun/idle/survivor-idle_shotgun_'
        cls.shotgun_idle = helpers.load_image_list(default_directory, extension_file, 20)
        cls.shotgun_idle = helpers.scale_image_list(cls.shotgun_idle, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/shotgun/reload/survivor-reload_shotgun_'
        cls.shotgun_reload = helpers.load_image_list(default_directory, extension_file, 20)
        cls.shotgun_reload = helpers.scale_image_list(cls.shotgun_reload, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/shotgun/meleeattack/survivor-meleeattack_shotgun_'
        cls.shotgun_meleeattack = helpers.load_image_list(default_directory, extension_file, 15)
        cls.shotgun_meleeattack = helpers.scale_image_list(cls.shotgun_meleeattack, constants.SCALE_RATIO)
        #---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        default_directory = 'Assets/Images/player/handgun/move/survivor-move_handgun_'
        cls.handgun_move = helpers.load_image_list(default_directory, extension_file, 20)
        cls.handgun_move = helpers.scale_image_list(cls.handgun_move, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/handgun/shoot/survivor-shoot_handgun_'
        cls.handgun_shoot = helpers.load_image_list(default_directory, extension_file, 3)
        cls.handgun_shoot = helpers.scale_image_list(cls.handgun_shoot, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/handgun/idle/survivor-idle_handgun_'
        cls.handgun_idle = helpers.load_image_list(default_directory, extension_file, 20)
        cls.handgun_idle = helpers.scale_image_list(cls.handgun_idle, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/handgun/reload/survivor-reload_handgun_'
        cls.handgun_reload = helpers.load_image_list(default_directory, extension_file, 15)
        cls.handgun_reload = helpers.scale_image_list(cls.handgun_reload, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/handgun/meleeattack/survivor-meleeattack_handgun_'
        cls.handgun_meleeattack = helpers.load_image_list(default_directory, extension_file, 15)
        cls.handgun_meleeattack = helpers.scale_image_list(cls.handgun_meleeattack, constants.SCALE_RATIO)
        # ---------------------------------------------------------------------------

        default_directory = 'Assets/Images/player/feet/strafe_left/survivor-strafe_left_'
        cls.feet_strafe_left = helpers.load_image_list(default_directory, extension_file, 20)
        cls.feet_strafe_left = helpers.scale_image_list(cls.feet_strafe_left, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/feet/strafe_right/survivor-strafe_right_'
        cls.feet_strafe_right = helpers.load_image_list(default_directory, extension_file, 20)
        cls.feet_strafe_right = helpers.scale_image_list(cls.feet_strafe_right, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/feet/walk/survivor-walk_'
        cls.feet_walk = helpers.load_image_list(default_directory, extension_file, 20)
        cls.feet_walk = helpers.scale_image_list(cls.feet_walk, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/player/feet/idle/survivor-idle_'
        cls.feet_idle = helpers.load_image_list(default_directory, extension_file, 1)
        cls.feet_idle = helpers.scale_image_list(cls.feet_idle, constants.SCALE_RATIO)

class Zombie:

    idle = []
    move = []
    attack = []
    @classmethod
    def load(cls):
        default_directory = 'Assets/Images/zombie/idle/skeleton-idle_'
        extension_file = '.png'
        cls.idle = helpers.load_image_list(default_directory, extension_file, 17)
        cls.idle = helpers.scale_image_list(cls.idle, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/zombie/move/skeleton-move_'
        cls.move = helpers.load_image_list(default_directory, extension_file, 17)
        cls.move = helpers.scale_image_list(cls.move, constants.SCALE_RATIO)

        default_directory = 'Assets/Images/zombie/attack/skeleton-attack_'
        cls.attack = helpers.load_image_list(default_directory, extension_file, 9)
        cls.attack = helpers.scale_image_list(cls.attack, constants.SCALE_RATIO)


     # @staticmethod
     # @classmethod
     # def class_method(cls):
     #     # the class method gets passed the class (in this case ModCLass)
     #     return "I am a class method"
     # def instance_method(self):
     #     # An instance method gets passed the instance of ModClass
     #     return "I am an instance method"