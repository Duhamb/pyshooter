import pygame as pg
import helpers
import Collider
from ExtendedGroup import *
import random

class Bot(pg.sprite.Sprite):

    def __init__(self, location_on_scenario, surface, background, player, animation):
        super().__init__()

        self.velocity = random.randint(2, 4)

        # load all objects necessary for bot interaction
        self.player = player
        self.background = background

        # original_image will be used in rotate
        self.original_image = None

        # surface to draw
        self.surface = surface

        # represent the position in relation to map
        # when drawing, this coordinate should be converted to position in screen
        self.position_on_scenario = pg.math.Vector2(location_on_scenario)

        # image and rect will be defined according with the animation
        self.image = animation.idle[0]
        self.center = helpers.scenario_to_screen(self.position_on_scenario, self.background, False)
        self.rect = self.image.get_rect(center=self.center)

        # add collider to bot
        self.collider = Collider.Collider(pg.Rect(0,0,40,40), self.background.rect, None)

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

        # life inicial status
        self.life = 3
        self.is_dead = False

        # group with all other zombies
        self.bot_group = None

    def update(self, bot_group):
        self.bot_group = bot_group
        self.choose_animation()
        self.rotate()
        self.choose_action()

        distance_to_player = self.position_on_scenario.distance_to(self.player.position_on_scenario)
        if distance_to_player < 500:
            if not self.is_grunting:
                self.is_grunting = True
                self.channel.play(self.grunt, -1)
            self.grunt.set_volume(1-distance_to_player/500)
        else:
            self.grunt.stop()
            self.is_grunting = False

        if self.is_dead and self.is_grunting:
            self.grunt.stop()
            self.is_grunting = False


    def rotate(self):
        player_position = self.player.position_on_screen
        bot_position = helpers.scenario_to_screen(self.position_on_scenario, self.background)
        # bot_position = pg.math.Vector2(self.rect.center)
        _, self.angle = (player_position-bot_position).as_polar()
        self.angle = self.angle
        # gira todas as imagens
        # self.image = pg.transform.rotozoom(self.original_image, -self.angle, 1)
        self.image = pg.transform.rotate(self.original_image, -self.angle)

        # gira em torno do centro real
        # encontra a nova posição do centro do rect
        self.rotated_center = self.delta_center_position.rotate(+self.angle)
        self.new_rect_center = self.rotated_center + helpers.scenario_to_screen(self.position_on_scenario, self.background)

        # atualiza o rect da imagem com o novo centro correto
        self.rect = self.image.get_rect(center=self.new_rect_center)

    def choose_animation(self):
        if self.is_attacking:
            self.float_index = helpers.increment(self.float_index, 0.5, 1)
            self.index_animation_attack = helpers.increment(self.index_animation_attack, int(self.float_index), 8)
            self.original_image = self.animation.attack[self.index_animation_attack]
            self.animation_name = "attack"

        elif self.is_moving:
            self.index_animation_move = helpers.increment(self.index_animation_move, 1, 16)
            self.original_image = self.animation.move[self.index_animation_move]
            self.animation_name = "move"

        else:
            self.float_index = helpers.increment(self.float_index, 0.25, 1)
            self.index_animation_idle = helpers.increment(self.index_animation_idle, int(self.float_index), 16)
            self.original_image = self.animation.idle[self.index_animation_idle]
            self.animation_name = "idle"

        self.animation_index = self.index_animation_attack

    def move(self):
        # define direction to move
        direction = self.player.position_on_scenario - self.position_on_scenario

        direction.normalize_ip()
        direction = direction * self.velocity
        # move
        last_position_on_scenario = tuple(self.position_on_scenario)

        # verify collision with walls
        alternative_move = [0,-120,120]
        self.position_on_scenario = pg.math.Vector2(last_position_on_scenario)
        for angle in alternative_move:
            self.position_on_scenario += direction.rotate(angle) + direction.rotate(angle)*abs(angle/50)
            self.collider.update(self.position_on_scenario)
            collisions = pg.sprite.spritecollide(self.collider, self.background.collider_group, False)
            if collisions:
                helpers.move_on_collision(self.collider, collisions, direction)
                # fix position if necessary based on collision
                self.position_on_scenario = helpers.image_to_scenario(self.collider.rect.center, self.background.rect)

            # verify collision with other zombies
            collisions = helpers.check_collision(self.collider, self.bot_group)
            if collisions:
                self.position_on_scenario = pg.math.Vector2(last_position_on_scenario)
            else:
                break
            
        self.collider.update(self.position_on_scenario)

    def choose_action(self):
        distance_to_player = self.position_on_scenario.distance_to(self.player.position_on_scenario)
        if distance_to_player < 70:
            self.is_moving = False
            self.is_attacking = True
        elif distance_to_player < 600:
            self.is_moving = True
            self.is_attacking = False
            self.move()
        else:
            self.is_attacking = False
            self.is_moving = False

    def get_server_info(self):
        info = {'position_on_scenario': tuple(self.position_on_scenario),
         'angle': self.angle,
         'animation_name': self.animation_name,
         'animation_index': self.animation_index
         }
        return info

    def draw(self, screen):
        if helpers.is_visible_area(self.rect.center):
            screen.blit(self.image, self.rect)

    def draw_multiplayer(self, screen, server_info ):
        position_on_screen = helpers.scenario_to_screen(server_info['position_on_scenario'], self.background, False)
        # body
        if helpers.is_visible_area(position_on_screen):
            animation = getattr(self.animation, server_info['animation_name'])
            original_image = animation[server_info['animation_index']]
            [imageMultiplayer, rect_multiplayer] = helpers.rotate_fake_center(original_image, server_info['angle'], self.delta_center_position, position_on_screen)
            # draw images
            screen.blit(imageMultiplayer, rect_multiplayer)

    def gets_hit(self):
        self.life -= self.player.weapon.damage_list[self.player.weapon.type]
        if self.life <= 0:
            self.is_dead = True

    def stop_grunt(self):
        if self.is_grunting:
            self.grunt.stop()
   