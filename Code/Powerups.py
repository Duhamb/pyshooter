import pygame
import Code.helpers as helpers

class Powerups(pygame.sprite.Sprite):
    life_image = None
    rifle_image = None
    shotgun_image = None
    rifle_ammo_image = None
    shotgun_ammo_image = None
    handgun_ammo_image = None

    def __init__(self, background, powerup_type):
        super().__init__()

        self.powerup_type = powerup_type

        if powerup_type == 'life':
            type(self).life_image = pygame.image.load("Assets/Images/powerups/life_up.png").convert_alpha()
            self.image = type(self).life_image

        elif powerup_type == 'rifle':
            type(self).rifle_image = pygame.image.load("Assets/Images/ak47.png").convert_alpha()
            self.image = type(self).rifle_image

        elif powerup_type == 'shotgun':
            type(self).shotgun_image = pygame.image.load("Assets/Images/shotgun.png").convert_alpha()
            self.image = type(self).shotgun_image

        elif powerup_type == 'rifle_ammo':
            type(self).rifle_ammo_image = pygame.image.load("Assets/Images/rifle_ammo.png").convert_alpha()
            self.image = type(self).rifle_ammo_image

        elif powerup_type == 'shotgun_ammo':
            type(self).shotgun_ammo_image = pygame.image.load("Assets/Images/shotgun_ammo.png").convert_alpha()
            self.image = type(self).shotgun_ammo_image

        elif powerup_type == 'handgun_ammo':
            type(self).handgun_ammo_image = pygame.image.load("Assets/Images/handgun_ammo.png").convert_alpha()
            self.image = type(self).handgun_ammo_image

        self.background = background

        self.position_on_scenario = None
        self.get_free_position()

        self.center = helpers.scenario_to_screen(self.position_on_scenario, self.background, False)
        self.rect = self.image.get_rect(center=self.center)

        self.life_current_quantity = 0
        self.life_maximum_quantity = 5

        self.player_name = None

    def update(self):
        self.rect.center = helpers.scenario_to_screen(self.position_on_scenario, self.background)

    def draw(self, screen):
        if helpers.is_visible_area(self.rect.center):
            screen.blit(self.image, self.rect)

    def get_free_position(self):
        self.position_on_scenario = helpers.generate_random_location()

    def get_server_info(self):
        info = {
        'type': self.powerup_type,
        'position_on_scenario': self.position_on_scenario,
        'player_name': self.player_name
        }
        return info
    
    @classmethod
    def draw_multiplayer(cls, screen, background, server_info):
        position_on_screen = helpers.scenario_to_screen(server_info['position_on_scenario'], background, False)
        if server_info['type'] == 'life':
            image = cls.life_image
            rect = image.get_rect(center=position_on_screen)
        screen.blit(image,rect)
        
        # pygame.draw.line(screen,(255,0,0),rect.center,(400,400),2)