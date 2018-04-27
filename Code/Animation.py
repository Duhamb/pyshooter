import pygame as pg 
import Code.helpers as helpers
import Code.constants as constants

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

        default_directory = 'Assets/Images/player/knife/idle/survivor-idle_knife_'
        cls.knife_idle = helpers.load_image_list(default_directory, extension_file, 20)

        default_directory = 'Assets/Images/player/knife/meleeattack/survivor-meleeattack_knife_'
        cls.knife_meleeattack = helpers.load_image_list(default_directory, extension_file, 15)
        # ---------------------------------------------------------------------------

        #---------------------------------------------------------------------------
        default_directory = 'Assets/Images/player/rifle/move/survivor-move_rifle_'
        cls.rifle_move = helpers.load_image_list(default_directory, extension_file, 20)

        default_directory = 'Assets/Images/player/rifle/shoot/survivor-shoot_rifle_'
        cls.rifle_shoot = helpers.load_image_list(default_directory, extension_file, 3)

        default_directory = 'Assets/Images/player/rifle/idle/survivor-idle_rifle_'
        cls.rifle_idle = helpers.load_image_list(default_directory, extension_file, 20)

        default_directory = 'Assets/Images/player/rifle/reload/survivor-reload_rifle_'
        cls.rifle_reload = helpers.load_image_list(default_directory, extension_file, 20)

        default_directory = 'Assets/Images/player/rifle/meleeattack/survivor-meleeattack_rifle_'
        cls.rifle_meleeattack = helpers.load_image_list(default_directory, extension_file, 15)
        #---------------------------------------------------------------------------

        #---------------------------------------------------------------------------
        default_directory = 'Assets/Images/player/shotgun/move/survivor-move_shotgun_'
        cls.shotgun_move = helpers.load_image_list(default_directory, extension_file, 20)

        default_directory = 'Assets/Images/player/shotgun/shoot/survivor-shoot_shotgun_'
        cls.shotgun_shoot = helpers.load_image_list(default_directory, extension_file, 3)

        default_directory = 'Assets/Images/player/shotgun/idle/survivor-idle_shotgun_'
        cls.shotgun_idle = helpers.load_image_list(default_directory, extension_file, 20)

        default_directory = 'Assets/Images/player/shotgun/reload/survivor-reload_shotgun_'
        cls.shotgun_reload = helpers.load_image_list(default_directory, extension_file, 20)

        default_directory = 'Assets/Images/player/shotgun/meleeattack/survivor-meleeattack_shotgun_'
        cls.shotgun_meleeattack = helpers.load_image_list(default_directory, extension_file, 15)
        #---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        default_directory = 'Assets/Images/player/handgun/move/survivor-move_handgun_'
        cls.handgun_move = helpers.load_image_list(default_directory, extension_file, 20)

        default_directory = 'Assets/Images/player/handgun/shoot/survivor-shoot_handgun_'
        cls.handgun_shoot = helpers.load_image_list(default_directory, extension_file, 3)

        default_directory = 'Assets/Images/player/handgun/idle/survivor-idle_handgun_'
        cls.handgun_idle = helpers.load_image_list(default_directory, extension_file, 20)

        default_directory = 'Assets/Images/player/handgun/reload/survivor-reload_handgun_'
        cls.handgun_reload = helpers.load_image_list(default_directory, extension_file, 15)

        default_directory = 'Assets/Images/player/handgun/meleeattack/survivor-meleeattack_handgun_'
        cls.handgun_meleeattack = helpers.load_image_list(default_directory, extension_file, 15)
        # ---------------------------------------------------------------------------

        default_directory = 'Assets/Images/player/feet/strafe_left/survivor-strafe_left_'
        cls.feet_strafe_left = helpers.load_image_list(default_directory, extension_file, 20)

        default_directory = 'Assets/Images/player/feet/strafe_right/survivor-strafe_right_'
        cls.feet_strafe_right = helpers.load_image_list(default_directory, extension_file, 20)

        default_directory = 'Assets/Images/player/feet/walk/survivor-walk_'
        cls.feet_walk = helpers.load_image_list(default_directory, extension_file, 20)

        default_directory = 'Assets/Images/player/feet/idle/survivor-idle_'
        cls.feet_idle = helpers.load_image_list(default_directory, extension_file, 1)

class Zombie:
    idle = []
    move = []
    attack = []
    @classmethod
    def load(cls):
        default_directory = 'Assets/Images/zombie/idle/skeleton-idle_'
        extension_file = '.png'
        cls.idle = helpers.load_image_list(default_directory, extension_file, 17)

        default_directory = 'Assets/Images/zombie/move/skeleton-move_'
        cls.move = helpers.load_image_list(default_directory, extension_file, 17)

        default_directory = 'Assets/Images/zombie/attack/skeleton-attack_'
        cls.attack = helpers.load_image_list(default_directory, extension_file, 9)