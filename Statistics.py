import pygame as pg

class Statistics():
	def __init__(self, player, screen_size):
		self.player = player
		self.screen_size = screen_size
		
		self.image_weapon = pg.image.load("Assets/Images/ak47.png").convert_alpha()
		self.rect_weapon = self.image_weapon.get_rect(bottomright=(screen_size[0]-20, screen_size[1]-20))
		
		self.font_text_25 = pg.font.Font("Assets/Fonts/UrbanJungleDEMO.otf", 25)
		self.font_text_18 = pg.font.Font("Assets/Fonts/UrbanJungleDEMO.otf", 18)
		self.score_label = self.font_text_18.render("SCORE", 1, (255,255,255))
		self.score_value = self.font_text_25.render("000000000", 1, (255,255,255))

	def draw(self, screen):
		self.draw_score(screen)
		self.draw_weapon(screen)

	def draw_weapon(self, screen):
		screen.blit(self.image_weapon, self.rect_weapon)

	def draw_score(self, screen):
		points = str(self.player.index_animation_move)
		points = self.font_text_25.render(points, 1, (255,255,255))
		screen.blit(self.score_label, (15, 15))
		screen.blit(self.score_value, (15, 41))
		screen.blit(points, (15, 67))