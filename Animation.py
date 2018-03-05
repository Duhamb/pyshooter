import pygame as pg 

"""
I'm not proud of this, but... :(
"""

def scale_image(list_images):
    for i in range(0, len(list_images)):
        list_images[i] = pg.transform.scale(list_images[i], (75,75))
    return list_images

class Player:

    move = []
    shoot = []

    # @staticmethod
    @classmethod
    def load(cls):
        if len(cls.move) == 0:
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_0.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_1.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_2.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_3.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_4.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_5.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_6.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_7.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_8.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_9.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_10.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_11.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_12.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_13.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_14.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_15.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_16.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_17.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_18.png'))
            cls.move.append(pg.image.load('Assets/Images/move/survivor-move_rifle_19.png'))
            cls.move = scale_image(cls.move)

        if len(cls.shoot) == 0:
            cls.shoot.append(pg.image.load('Assets/Images/shoot/survivor-shoot_rifle_0.png'))
            cls.shoot.append(pg.image.load('Assets/Images/shoot/survivor-shoot_rifle_1.png'))
            cls.shoot.append(pg.image.load('Assets/Images/shoot/survivor-shoot_rifle_2.png'))
            cls.shoot = scale_image(cls.shoot)


     # @classmethod
     # def class_method(cls):
     #     # the class method gets passed the class (in this case ModCLass)
     #     return "I am a class method"
     # def instance_method(self):
     #     # An instance method gets passed the instance of ModClass
     #     return "I am an instance method"