
import pygame as pg 

class Player:

    shoot = None
    zoa = None
    reload = None
    footstep = None
    # @staticmethod
    @classmethod
    def load(cls):
        # if len(cls.move) == 0:
        cls.shoot = pg.mixer.Sound('Assets/Sounds/ak47_shoot.wav')
        cls.reload = pg.mixer.Sound('Assets/Sounds/ak47_reload.wav')
        cls.footstep = pg.mixer.Sound('Assets/Sounds/footstep.wav')
        cls.zoa = pg.mixer.Sound('Assets/Sounds/tacaopau.wav')

    @classmethod
    def play(cls):
        cls.shoot.play()

    @classmethod
    def stop(cls):
        cls.shoot.stop()

class Bot:
    grunt = None
    # @staticmethod
    @classmethod
    def load(cls):
        # if len(cls.move) == 0:
        cls.grunt = pg.mixer.Sound('Assets/Sounds/zombie.wav')