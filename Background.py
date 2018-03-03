import pygame as pg

class Background():
    def __init__(self, back, front, location):
        self.front = front
        self.back = back
        self.center_image_position = pg.math.Vector2((0,0))
        self.rect = self.front.get_rect(center=location)
        self.back_array=pg.surfarray.array2d(self.back)
        # self.steps_sound = pg.mixer.Sound("stepstone_1.wav")
        # self.steps_sound.set_volume(10)

    def draw(self, surface):
        surface.blit(self.front, self.rect)

    def move(self, vector):
        # self.steps_sound.play()
        dx = vector[0]
        dy = vector[1]
        self.rect = self.front.get_rect(center = (self.rect.center[0] + 10*dx, self.rect.center[1] + 10*dy))
        self.center_image_position = pg.math.Vector2(self.rect.center)
