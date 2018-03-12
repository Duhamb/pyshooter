import pygame as pg

class Light():
	def __init__(self, screen_size, player):
		self.fog = pg.Surface(screen_size)
		self.light_mask = pg.image.load('Assets/Images/light.png').convert_alpha()
		self.light_rect = self.light_mask.get_rect()
		self.player = player
		self.color = (5,5,5)
		self.fog.fill(self.color)
		self.light_rect.center = self.player.position_on_screen
		self.fog.blit(self.light_mask, self.light_rect)

	def draw(self, screen):

		screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)