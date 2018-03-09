import pygame as pg 

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
            default_directory = 'Assets/Images/move/survivor-move_rifle_'
            extension_file = '.png'
            for i in range(0,20):
                actual_file = default_directory + str(i) + extension_file
                cls.move.append(pg.image.load(actual_file))
            cls.move = scale_image(cls.move, 2.7)

        if len(cls.shoot) == 0:
            default_directory = 'Assets/Images/shoot/survivor-shoot_rifle_'
            extension_file = '.png'
            for i in range(0,3):
                actual_file = default_directory + str(i) + extension_file
                cls.shoot.append(pg.image.load(actual_file))
            cls.shoot = scale_image(cls.shoot, 2.7)

        if len(cls.run) == 0:
            default_directory = 'Assets/Images/feet/run/survivor-run_'
            extension_file = '.png'
            for i in range(0,20):
                actual_file = default_directory + str(i) + extension_file
                cls.run.append(pg.image.load(actual_file))
            cls.run = scale_image(cls.run, 2.7)

     # @classmethod
     # def class_method(cls):
     #     # the class method gets passed the class (in this case ModCLass)
     #     return "I am a class method"
     # def instance_method(self):
     #     # An instance method gets passed the instance of ModClass
     #     return "I am an instance method"