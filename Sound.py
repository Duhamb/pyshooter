
import pygame as pg 

class Player:

    shoot = None

    # @staticmethod
    @classmethod
    def load(cls):
        # if len(cls.move) == 0:
        cls.shoot = pg.mixer.Sound('Assets/Sounds/mp5.wav')

    @classmethod
    def play(cls):
        cls.shoot.play()

    @classmethod
    def stop(cls):
        cls.shoot.stop()