import pygame as pg

class Statistics():
	def __init__(self, player, screen_size):
		self.player = player
		self.screen_size = screen_size
		
		self.ammo = pg.image.load("Assets/Images/ammo_display.png").convert_alpha()
		self.rect_ammo = self.ammo.get_rect(bottomright=screen_size)
		self.ammo_counter = pg.image.load("Assets/Images/ammo_counter.png").convert_alpha()
		self.rect_ammo_counter = self.ammo_counter.get_rect(bottomright=screen_size)
		
		self.font_text = pg.font.Font("Assets/Fonts/UrbanJungleDEMO.otf", 25)
		self.score_label = self.font_text.render("SCORE", 1, (255,255,255))
		self.score_value = self.font_text.render("000000000", 1, (255,255,255))

		self.ammo_real = player.ammo

	def draw(self, screen):
		points = str(self.player.index_animation_move)
		points = self.font_text.render(points, 1, (255,255,255))
		screen.blit(self.score_label, (10, 10))
		screen.blit(self.score_value, (10, 36))
		screen.blit(points, (10, 62))

		screen.blit(self.ammo, self.rect_ammo)
		
		self.ammo_real = self.player.ammo
		self.create_ammo_display(screen, self.ammo_real)

	def create_ammo_display(self, screen, ammo_qtd):
		degree = 10
		angle = 0
		for i in range(0, ammo_qtd):
			image_to_blit = pg.transform.rotozoom(self.ammo_counter, -angle, 1)
			self.rect_ammo_counter = image_to_blit.get_rect(center = self.rect_ammo.center)
			screen.blit(image_to_blit, self.rect_ammo_counter)
			angle += degree