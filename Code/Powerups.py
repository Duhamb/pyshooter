import pygame
import Code.helpers as helpers

class Powerups(pygame.sprite.Sprite):
    life_image = None
    def __init__(self, background):
        super().__init__()
        
        type(self).life_image = pygame.image.load("Assets/Images/powerups/life_up.png").convert_alpha()
        self.background = background

        self.image = type(self).life_image
        self.rect = self.image.get_rect()
        self.life_current_quantity = 0
        self.life_maximum_quantity = 5

        self.position_on_scenario = None
        self.get_free_position()

        self.powerup_type = 'life'

        self.player_name = None

    def update(self):
        self.rect.center = helpers.scenario_to_screen(self.position_on_scenario, self.background)

    def draw(self, screen):
        self.rect.center = helpers.scenario_to_screen(self.position_on_scenario, self.background, False)
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