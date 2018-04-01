import pygame as pg

class Statistics():
    def __init__(self, player, screen_size, multiplayer_on, server_client, is_host):
        self.player = player
        self.screen_size = screen_size
        self.multiplayer_on = multiplayer_on
        self.is_host = is_host
        self.server_client = server_client
        self.position_on_screen = None

        self.image_weapon_rifle = pg.image.load("Assets/Images/ak47.png").convert_alpha()
        self.image_weapon_shotgun = pg.image.load("Assets/Images/shotgun.png").convert_alpha()
        self.rect_weapon = self.image_weapon_rifle.get_rect(bottomright=(screen_size[0]-20, screen_size[1]-20))

        self.image_minimap = pg.image.load("Assets/Images/minimap.png").convert_alpha()
        self.rect_minimap = self.image_minimap.get_rect(bottomleft=(0 + 15,self.screen_size[1] - 15))
        self.center_position_minimap = pg.math.Vector2(self.rect_minimap.center)
        self.ratio = 89.7

        self.font_text_25 = pg.font.Font("Assets/Fonts/BebasNeue-Regular.otf", 25)
        self.font_text_18 = pg.font.Font("Assets/Fonts/BebasNeue-Regular.otf", 18)
        self.score_label = self.font_text_18.render("SCORE", 1, (255,255,255))
        self.score_value = self.font_text_25.render("000000000", 1, (255,255,255))

        self.initial_radius = 10

    def draw(self, screen):
        self.draw_score(screen)
        self.draw_weapon(screen)
        self.draw_minimap(screen)
        self.draw_ammo(screen)
        if self.multiplayer_on:
            self.draw_minimap_multiplayer(screen)
            self.draw_score_multiplayer(screen)

    def draw_weapon(self, screen):
        if self.player.actual_weapon == 'rifle':
            screen.blit(self.image_weapon_rifle, self.rect_weapon)
        else:
            screen.blit(self.image_weapon_shotgun, self.rect_weapon)

    def draw_score(self, screen):

        points = "Your score: " + str(self.player.score)
        points = self.font_text_25.render(points, 1, (255,255,255))
        if self.multiplayer_on:
            name = self.font_text_18.render(self.server_client.name, 1, (255, 255, 255))
            screen.blit(name, (15, 15))
        screen.blit(points, (15, 41))

    def draw_minimap(self, screen):
        screen.blit(self.image_minimap, self.rect_minimap)
        position_on_minimap = self.player.position_on_scenario/self.ratio
        self.position_on_screen = position_on_minimap + self.center_position_minimap
        self.position_on_screen = (int(self.position_on_screen[0]), int(self.position_on_screen[1]))
        pg.draw.circle(screen, (255,0,0), self.position_on_screen, int(self.initial_radius), 2)
        if self.initial_radius > 3.2:
            self.initial_radius -= 0.1

    def draw_minimap_multiplayer(self, screen):
        self.server_client.push_minimap(self.position_on_screen)
        self.server_client.pull_minimaps()
        positions_list = self.server_client.minimaps_info
        for player_name in positions_list:
            if player_name != self.server_client.name:
                pg.draw.circle(screen, (0, 255, 0), positions_list[player_name], 2, 1)

    def draw_score_multiplayer(self, screen):
        self.server_client.push_scores(self.is_host)
        self.server_client.pull_scores(self.is_host)
        scores_list = self.server_client.scores
        y = 0
        for scores_name in scores_list:
            if scores_name == self.server_client.name:
                self.player.score = scores_list[scores_name]
            else:
                points = str(scores_name) +": "+ str(scores_list[scores_name])
                points = self.font_text_25.render(points, 1, (255,255,255))
                screen.blit(points, (15, 80+y))
                y = y + 30

    def draw_ammo(self, screen):
        ammo = str(self.player.bullet_counter) + "/15"
        ammo = self.font_text_25.render(ammo, 1, (255, 255, 255))
        screen.blit(ammo, (740, 555))
        