import pygame as pg

class Statistics():
	def __init__(self, player, screen_size):
		self.player = player
		self.screen_size = screen_size
		
		self.image_weapon_rifle = pg.image.load("Assets/Images/ak47.png").convert_alpha()
		self.image_weapon_shotgun = pg.image.load("Assets/Images/shotgun.png").convert_alpha()
		self.rect_weapon = self.image_weapon_rifle.get_rect(bottomright=(screen_size[0]-20, screen_size[1]-20))

		self.image_minimap = pg.image.load("Assets/Images/minimap.png").convert_alpha()
		self.rect_minimap = self.image_minimap.get_rect(bottomleft=(0 + 15,self.screen_size[1] - 15))
		self.center_position_minimap = pg.math.Vector2(self.rect_minimap.center)
		self.ratio = 89.7	
		
		self.font_text_25 = pg.font.Font("Assets/Fonts/UrbanJungleDEMO.otf", 25)
		self.font_text_18 = pg.font.Font("Assets/Fonts/UrbanJungleDEMO.otf", 18)
		self.score_label = self.font_text_18.render("SCORE", 1, (255,255,255))
		self.score_value = self.font_text_25.render("000000000", 1, (255,255,255))

	def draw(self, screen):
		self.draw_score(screen)
		self.draw_weapon(screen)
		self.draw_minimap(screen)

	def draw_weapon(self, screen):
		if self.player.actual_weapon == 'rifle':
			screen.blit(self.image_weapon_rifle, self.rect_weapon)
		else:
			screen.blit(self.image_weapon_shotgun, self.rect_weapon)

	def draw_score(self, screen):
		points = str(self.player.index_animation_move)
		points = self.font_text_25.render(points, 1, (255,255,255))
		screen.blit(self.score_label, (15, 15))
		screen.blit(self.score_value, (15, 41))
		screen.blit(points, (15, 67))

	def draw_minimap(self, screen):
		screen.blit(self.image_minimap, self.rect_minimap)
		position_on_minimap = self.player.position_on_scenario/self.ratio
		position_on_screen = position_on_minimap + self.center_position_minimap
		position_on_screen = (int(position_on_screen[0]), int(position_on_screen[1]))
		pg.draw.circle(screen, (255,0,0), position_on_screen, 2, 1)	