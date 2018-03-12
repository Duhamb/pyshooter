import pygame as pg 
from helpers import *

class Player:
    move = []
    shoot = []
    feet_run = []
    idle = []
    rifle_reload = []

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

        default_directory = 'Assets/Images/player/feet/walk/survivor-walk_'
        extension_file = '.png'
        cls.feet_run = load_image_list(default_directory, extension_file, 20)
        cls.feet_run = scale_image_list(cls.feet_run, 2.7)

     # @staticmethod
     # @classmethod
     # def class_method(cls):
     #     # the class method gets passed the class (in this case ModCLass)
     #     return "I am a class method"
     # def instance_method(self):
     #     # An instance method gets passed the instance of ModClass
     #     return "I am an instance method"