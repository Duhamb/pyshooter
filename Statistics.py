import pygame as pg

class Statistics():
	def __init__(self, player, screen_size):
		self.player = player
		self.font_text = pg.font.Font("Assets/Fonts/UrbanJungleDEMO.otf", 25)
		self.score_label = self.font_text.render("SCORE", 1, (255,255,255))
		self.score_value = self.font_text.render("000000000", 1, (255,255,255))
		self.screen_size = screen_size

	def draw(self, screen):
		points = str(self.player.index_animation_move)
		points = self.font_text.render(points, 1, (255,255,255))
		screen.blit(self.score_label, (10, 10))
		screen.blit(self.score_value, (10, 36))
		screen.blit(points, (10, 62))