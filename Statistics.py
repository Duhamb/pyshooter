import pygame as pg

class Statistics():
	def __init__(self, player, screen_size):
		self.player = player
		self.screen_size = screen_size
		
		self.ammo = pg.image.load("Assets/Images/ammo_level_display.png").convert_alpha()
		self.rect_ammo = self.ammo.get_rect(bottomright=screen_size)
		
		self.font_text = pg.font.Font("Assets/Fonts/UrbanJungleDEMO.otf", 25)
		self.score_label = self.font_text.render("SCORE", 1, (255,255,255))
		self.score_value = self.font_text.render("000000000", 1, (255,255,255))

	def draw(self, screen):
		points = str(self.player.index_animation_move)
		points = self.font_text.render(points, 1, (255,255,255))
		screen.blit(self.score_label, (10, 10))
		screen.blit(self.score_value, (10, 36))
		screen.blit(points, (10, 62))
		screen.blit(self.ammo, self.rect_ammo)