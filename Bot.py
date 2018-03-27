import pygame as pg
from helpers import *

class Bot(pg.sprite.Sprite):
    def __init__(self, location_on_scenario, surface, background, player, animation):
        super().__init__()

        # image and rect will be defined according with the animation
        self.image = None
        self.rect = None
        
        # original_image will be used in rotate
        self.original_image = None

        # load all objects necessary for bot interaction
        self.player = player
        self.background = background

        # surface to draw
        self.surface = surface

        # represent the position in relation to map
        # when drawing, this coordinate should be converted to position in screen
        self.position_on_scenario = pg.math.Vector2(location_on_scenario)

        # the center of sprite isnt the center of the own image file
        # so, this is needed to find the real center
        self.delta_center_position = pg.math.Vector2((+35.5/2.7,-8/2.7))
        
        # [TODO] sounds should be loaded in Sounds.py
        self.grunt = pg.mixer.Sound('Assets/Sounds/zombie.wav')
        self.channel = pg.mixer.find_channel(True)

        # flag
        self.is_grunting = False
        self.is_moving = False
        self.is_attacking = False

        # load animation
        self.animation = animation

        # index for animations
        self.index_animation_idle = 0
        self.index_animation_move = 0
        self.index_animation_attack = 0
        self.float_index = 0

        #multiplayer animation
        self.animation_name = None
        self.animation_index = None

    def update(self):
        self.choose_action()
        self.choose_animation()
        self.rotate()

        distance_to_player = self.position_on_scenario.distance_to(self.player.position_on_scenario)
        if distance_to_player < 500:
            if not self.is_grunting:
                self.is_grunting = True
                self.channel.play(self.grunt, -1)
            self.grunt.set_volume(1-distance_to_player/500)
        else:
            self.grunt.stop()
            self.is_grunting = False

        self.animation

    def rotate(self):
        _, self.angle = (self.player.position_on_scenario-self.position_on_scenario).as_polar()

        # gira todas as imagens
        self.image = pg.transform.rotozoom(self.original_image, -self.angle, 1)

        # gira em torno do centro real
        # encontra a nova posição do centro do rect
        self.rotated_center = self.delta_center_position.rotate(+self.angle)
        self.new_rect_center = self.rotated_center + scenario_to_screen(self.position_on_scenario, self.background.rect)

        # atualiza o rect da imagem com o novo centro correto
        self.rect = self.image.get_rect(center=self.new_rect_center)

    def choose_animation(self):
        if self.is_attacking:
            self.float_index = increment(self.float_index, 0.5, 1)
            self.index_animation_attack = increment(self.index_animation_attack, int(self.float_index), 8)
            self.original_image = self.animation.attack[self.index_animation_attack]
            self.animation_name = "attack"

        elif self.is_moving:
            self.index_animation_move = increment(self.index_animation_move, 1, 16)
            self.original_image = self.animation.move[self.index_animation_move]
            self.animation_name = "move"

        else:
            self.float_index = increment(self.float_index, 0.25, 1)
            self.index_animation_idle = increment(self.index_animation_idle, int(self.float_index), 16)
            self.original_image = self.animation.idle[self.index_animation_idle]
            self.animation_name = "idle"

        self.animation_index = self.index_animation_attack

    def move(self):
        direction = self.player.position_on_scenario - self.position_on_scenario
        direction.normalize_ip()
        direction = direction * 4
        self.position_on_scenario += direction

    def choose_action(self):
        distance_to_player = self.position_on_scenario.distance_to(self.player.position_on_scenario)
        if distance_to_player < 50:
            self.is_moving = False
            self.is_attacking = True
        elif distance_to_player < 300:
            self.is_moving = True
            self.is_attacking = False
            self.move()
        else:
            self.is_attacking = False
            self.is_moving = False

    def get_server_info(self):
        # acho que o servidor não consegue tratar o tipo pg.math.Vector2
        info = {'position_on_scenario': (self.position_on_scenario[0], self.position_on_scenario[1]),
         'angle': self.angle,
         'animation_name': self.animation_name,
         'animation_index': self.animation_index
         }
        return info

    def draw_multiplayer(self, screen, server_info ):
        position_on_screen = scenario_to_screen_server(server_info['position_on_scenario'], self.background.rect)
        # body
        animation = getattr(self.animation, server_info['animation_name'])
        original_image = animation[server_info['animation_index']]
        [imageMultiplayer, rect_multiplayer] = rotate_fake_center(original_image, server_info['angle'], self.delta_center_position, position_on_screen)
        # draw images
        screen.blit(imageMultiplayer, rect_multiplayer)