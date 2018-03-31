import pygame as pg
import constants

class Light():
	def __init__(self, player):
		self.fog = pg.Surface(constants.SCREEN_SIZE)
		self.light_mask = pg.image.load('Assets/Images/light.png').convert_alpha()
		self.light_rect = self.light_mask.get_rect()
		self.player = player
		self.color = constants.BLACK
		self.fog.fill(self.color)
		self.light_rect.center = constants.PLAYER_POSITION_SCREEN
		self.fog.blit(self.light_mask, self.light_rect)

	def draw(self, screen):

		screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)