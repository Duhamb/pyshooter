import pygame as pg

class Player:
    player_ugh = None
    @classmethod
    def load(cls):
        cls.footstep = pg.mixer.Sound('Assets/Sounds/footstep.wav')
        cls.player_ugh = pg.mixer.Sound('Assets/Sounds/Player/ugh.wav')

class Weapon:
    @classmethod
    def load(cls):
        cls.rifle_shoot = pg.mixer.Sound('Assets/Sounds/ak47_shoot2.wav')
        cls.rifle_reload = pg.mixer.Sound('Assets/Sounds/ak47_reload.wav')
        cls.shotgun_shoot = pg.mixer.Sound('Assets/Sounds/shotgun_shoot.wav')
        cls.shotgun_reload = pg.mixer.Sound('Assets/Sounds/shotgun_reload.wav')
        cls.meleeattack = pg.mixer.Sound('Assets/Sounds/meleeattack.wav')
        cls.empty = pg.mixer.Sound('Assets/Sounds/empty.wav')
        cls.player_reload = pg.mixer.Sound('Assets/Sounds/Player/reload.wav')
        cls.player_out_of_ammo = pg.mixer.Sound('Assets/Sounds/Player/out_of_ammo.wav')

class Bot:
    grunt = None
    @classmethod
    def load(cls):
        cls.grunt = pg.mixer.Sound('Assets/Sounds/zombie.wav')