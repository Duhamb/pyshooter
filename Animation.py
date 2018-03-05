import pygame as pg 

"""
I'm not proud of this, but... :(
"""

def scale_image(list_images, ratio):
    size = list_images[0].get_rect().size
    for i in range(0, len(list_images)):
        list_images[i] = pg.transform.scale(list_images[i], (int(size[0]/ratio),int(size[1]/ratio)))
    return list_images

class Player:

    move = []
    shoot = []
    run = []

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
            cls.move = scale_image(cls.move, 2.7)

        if len(cls.shoot) == 0:
            cls.shoot.append(pg.image.load('Assets/Images/shoot/survivor-shoot_rifle_0.png'))
            cls.shoot.append(pg.image.load('Assets/Images/shoot/survivor-shoot_rifle_1.png'))
            cls.shoot.append(pg.image.load('Assets/Images/shoot/survivor-shoot_rifle_2.png'))
            cls.shoot = scale_image(cls.shoot, 2.7)

        if len(cls.run) == 0:
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_0.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_1.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_2.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_3.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_4.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_5.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_6.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_7.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_8.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_9.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_10.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_11.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_12.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_13.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_14.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_15.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_16.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_17.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_18.png'))
            cls.run.append(pg.image.load('Assets/Images/feet/run/survivor-run_19.png'))
            cls.run = scale_image(cls.run, 2.7)

     # @classmethod
     # def class_method(cls):
     #     # the class method gets passed the class (in this case ModCLass)
     #     return "I am a class method"
     # def instance_method(self):
     #     # An instance method gets passed the instance of ModClass
     #     return "I am an instance method"