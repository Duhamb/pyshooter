import pygame
from helpers import *
# link contendo as classes do sprite.Group
# https://github.com/pygame/pygame/blob/67026e3c51843d9313bbc8cc8a35d219eee3d4d4/lib/sprite.py#L464

class ExtendedGroup(pygame.sprite.Group):

    def handle_event(self, event):
        for spr in self.sprites():
            try:
                spr.handle_event(event)
            except:
                pass

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            try:
                spr.draw(surface)
            except:
                self.spritedict[spr] = surface_blit(spr.image, spr.rect)
            # draw_rect(spr.rect, surface)
        self.lostsprites = []