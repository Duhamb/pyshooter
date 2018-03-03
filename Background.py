import pygame as pg

class Background():
    def __init__(self, back, front):
        self.front = front
        self.back = back
        self.rect = self.front.get_rect()
        # self.back_array=pg.surfarray.array2d(self.back)

    def draw(self, surface, player):
        self.update_position(player)
        surface.blit(self.front, self.rect)

    def update_position(self, player):
        self.rect.center = player.position_on_screen - player.position_on_scenario

