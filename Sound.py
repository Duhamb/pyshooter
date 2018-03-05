
import pygame as pg 

class Player:

    shoot = None
    zoa = None
    # @staticmethod
    @classmethod
    def load(cls):
        # if len(cls.move) == 0:
        cls.shoot = pg.mixer.Sound('Assets/Sounds/AK47.wav')
        cls.zoa = pg.mixer.Sound('Assets/Sounds/tacaopau.wav')
        cls.shoot.set_volume(0.2)
        cls.zoa.set_volume(0.6)

    @classmethod
    def play(cls):
        cls.shoot.play()

    @classmethod
    def stop(cls):
        cls.shoot.stop()