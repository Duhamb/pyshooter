import pygame as pg

# acho melhor essa ficar sem herança da sprite enquanto não resolver a colisão
class Background():
    def __init__(self, back, front):
        self.front = front
        self.back = back
        self.rect = self.front.get_rect()
        self.mask = pg.mask.from_surface(self.back)

        # print(self.front.get_size())
        # print(self.back.get_size())

    def draw(self, surface, player):
        self.update_position(player)
        surface.blit(self.front, self.rect)
        surface.blit(self.back, self.rect)

    def update_position(self, player):
        self.rect.center = player.position_on_screen - player.position_on_scenario