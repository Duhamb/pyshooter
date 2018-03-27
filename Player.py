import pygame
from helpers import *
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, location_on_scenario, location_on_screen, animation, sound, background, tela):
        super().__init__()

        self.velocity = 5

        self.tela = tela

        # set all animations
        self.animation = animation
        self.animation_move = self.animation.rifle_move
        self.animation_idle = self.animation.rifle_idle
        self.animation_reload = self.animation.rifle_reload
        self.animation_shoot = self.animation.rifle_shoot
        self.animation_meleeattack = self.animation.rifle_meleeattack

        self.actual_weapon = 'rifle'

        # set all sounds (shoot, move, reload)
        self.sound = sound

        # define the collider shape
        self.collider_image = pg.image.load("Assets/Images/back_player.png").convert_alpha()
        self.collider_image = scale_image(self.collider_image, 2.7)
        self.rect_back = self.collider_image.get_rect(center = location_on_screen)
        self.mask = pygame.mask.from_surface(self.collider_image)

        # this surface wont be modified on the execution
        self.original_back_image = self.collider_image

        # initialize the original_feet
        # It will be modified according with animation
        self.original_feet = animation.feet_walk[0]
        
        # represent the Background object
        # needed to orientation
        self.background = background

        # the image center isnt correct
        # each sprite has a different offset
        self.delta_center_position = pygame.math.Vector2((+56/2.7,-19/2.7))

        # the sprite and rect of player
        self.image = self.animation_idle[0]
        self.rect = self.image.get_rect(center = location_on_screen)

        # positions
        self.position_on_screen = pygame.math.Vector2(location_on_screen)
        self.position_on_scenario = pygame.math.Vector2(location_on_scenario)

        # index for animations
        self.index_animation_move = 0
        self.index_animation_shoot = 0
        self.index_animation_idle = 0
        self.index_animation_reload = 0
        self.index_animation_meleeattack = 0
        self.index_animation_feet_walk = 0
        self.index_animation_feet_strafe_left = 0
        self.index_animation_feet_strafe_right = 0

        # flags for animation
        self.is_moving_forward = False
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_shooting = False
        self.is_reloading = False
        self.is_meleeattack = False
        self.is_idle = True

        # flags for sounds
        self.sound_footstep_playing = False 

        # handle events
        self.is_colliding = False
        self.pressionou_w = False
        self.pressionou_a = False
        self.pressionou_s = False
        self.pressionou_d = False

        # aux param to multiplayer
        self.angle_vision = None
        self.animation_body = None
        self.animation_body_index = None
        self.animation_feet = None
        self.animation_feet_index = None
        self.prefix_animation_name = 'rifle_'

        # slower animations
        self.float_index = 0

    def update(self):
        self.choose_animation()
        self.rotate()
        self.react_to_event()

    def draw(self, screen):
        screen.blit(self.feet, self.feet.get_rect(center=self.position_on_screen).topleft)
        screen.blit(self.image, self.rect)

    def draw_multiplayer(self, screen, server_info ):
        position_on_screen = scenario_to_screen_server(server_info['position_on_scenario'], self.background.rect)
        
        # body
        animation = getattr(self.animation, server_info['animation_body'])
        original_image = animation[server_info['animation_body_index']]
        [imageMultiplayer, rect_multiplayer] = rotate_fake_center(original_image, server_info['angle'], self.delta_center_position, position_on_screen)
        
        # feet
        animation_feet = getattr(self.animation, server_info['animation_feet'])
        original_image = animation_feet[server_info['animation_feet_index']]
        [imageFeet, rect_feet] = rotate_fake_center(original_image, server_info['angle'], pg.math.Vector2((0,0)), position_on_screen)
        
        # draw images
        screen.blit(imageFeet, rect_feet)
        screen.blit(imageMultiplayer, rect_multiplayer)

    def move(self, direction):
        if not self.is_possible_direction(direction):
            angles = get_normal(self.next_position_on_scenario, self.background)
            if len(angles) <= 1:
                big_size = False
                for k in angles:
                    if k[1] > 150:
                        big_size = True
                        break
                if not big_size:
                    for j in angles:
                        i = j[0]
                        normal_vector = pygame.math.Vector2((1,0)).rotate(i)
                        new_direction = remove_parallel_component(normal_vector, direction)
                        direction = new_direction
        try:
            self.position_on_scenario += self.velocity*(direction.normalize())
        except:
            pass

    def is_possible_direction(self, direction):
        self.next_position_on_scenario = self.position_on_scenario + self.velocity*direction
        next_rect = self.rect
        next_mask = self.mask
        next_rect_background = self.background.rect.copy()
        # this command obtain the next position of background
        next_rect_background.center = background_center_position(self.position_on_screen, self.next_position_on_scenario)
        offset = ((next_rect.left - next_rect_background.left ), (next_rect.top - next_rect_background.top))
        is_colliding = self.background.mask.overlap(next_mask, offset)

        if is_colliding:
            return False
        return True

    def rotate(self):
        # get the angle between mouse and player
        _, angle = (pygame.mouse.get_pos()-self.position_on_screen).as_polar()
        
        try:
            D = (pygame.mouse.get_pos()-self.position_on_screen).length()
            angle -= math.degrees(math.asin(32/(2.7*D)))
        except:
            pass

        self.angle_vision = angle
        # gira todas as imagens
        self.image = pygame.transform.rotozoom(self.original_image, -angle, 1)
        self.feet = pygame.transform.rotozoom(self.original_feet, -angle, 1)
        self.collider_image = pygame.transform.rotozoom(self.original_back_image, -angle, 1)

        # gira em torno do centro real
        # encontra a nova posição do centro do rect
        self.rotated_center = self.delta_center_position.rotate(+angle)
        self.new_rect_center = self.rotated_center + self.position_on_screen

        # atualiza o rect da imagem com o novo centro correto
        self.rect = self.image.get_rect(center=self.new_rect_center)
        self.rect_back = self.rect

        # atualiza a mascara relativa ao personagem
        # garante que a imagem estará sempre sobrepondo sua máscara
        self.mask = pygame.mask.from_surface(self.collider_image)

    # esse metodo pode estar no grupo também
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.pressionou_w = True
            if event.key == pygame.K_a:
                self.pressionou_a = True
            if event.key == pygame.K_s:
                self.pressionou_s = True
            if event.key == pygame.K_d:
                self.pressionou_d = True
            if self.set_animation_move_flags() and not self.sound_footstep_playing:
                pygame.mixer.Channel(2).play(self.sound.footstep, -1)
                self.sound_footstep_playing = True
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.pressionou_w = False
            if event.key == pygame.K_a:
                self.pressionou_a = False
            if event.key == pygame.K_s:
                self.pressionou_s = False
            if event.key == pygame.K_d:
                self.pressionou_d = False
            if not self.set_animation_move_flags():
                self.sound.footstep.stop()
                self.sound_footstep_playing = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.is_reloading = True
                pygame.mixer.Channel(1).play(self.sound.reload)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.is_shooting = True
            if event.button == 3:
                self.is_meleeattack = True
                pygame.mixer.Channel(1).play(self.sound.meleeattack)
    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_shooting = False
                self.sound.shoot.fadeout(125)

        # change weapon
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.change_weapon(1)
            elif event.key == pygame.K_2:
                self.change_weapon(2)
        

    def react_to_event(self):
        if self.pressionou_w or self.pressionou_d or self.pressionou_a or self.pressionou_s:
            self.actual_position = self.position_on_screen
            self.mouse_position = pygame.mouse.get_pos()
            self.vector_position = self.mouse_position - self.actual_position

            # react to multiples move commands
            if self.pressionou_w:
                if self.pressionou_a:
                    self.direction_of_move = (self.vector_position).rotate(-45)
                elif self.pressionou_d:
                    self.direction_of_move = (self.vector_position).rotate(45)
                else:                    
                    self.direction_of_move = (self.vector_position)
            elif self.pressionou_s:
                if self.pressionou_a:
                    self.direction_of_move = -(self.vector_position).rotate(45)
                elif self.pressionou_d:
                    self.direction_of_move = -(self.vector_position).rotate(-45)
                else:                    
                    self.direction_of_move = -(self.vector_position)
            elif self.pressionou_a:
                self.direction_of_move = -(self.vector_position).rotate(90)
            elif self.pressionou_d:
                self.direction_of_move = (self.vector_position).rotate(90)
            try:
                self.move(self.direction_of_move.normalize())  
            except:
                pass

    def change_weapon(self, weapon_number):
        if weapon_number == 1:
            self.animation_move = self.animation.rifle_move
            self.animation_shoot = self.animation.rifle_shoot
            self.animation_idle = self.animation.rifle_idle
            self.animation_reload = self.animation.rifle_reload
            self.animation_meleeattack = self.animation.rifle_meleeattack
            self.prefix_animation_name = 'rifle_'
            self.actual_weapon = 'rifle'
            # self.delta_center_position
        elif weapon_number == 2:
            self.animation_move = self.animation.shotgun_move
            self.animation_shoot = self.animation.shotgun_shoot
            self.animation_idle = self.animation.shotgun_idle
            self.animation_reload = self.animation.shotgun_reload
            self.animation_meleeattack = self.animation.shotgun_meleeattack
            self.prefix_animation_name = 'shotgun_'
            self.actual_weapon = 'shotgun'

    def choose_animation(self):
        # body animation
        if self.is_shooting:
            self.index_animation_shoot = increment(self.index_animation_shoot, 1, len(self.animation_shoot)-1)
            self.original_image = self.animation_shoot[self.index_animation_shoot]
            self.animation_body = self.prefix_animation_name + 'shoot'
            self.animation_body_index = self.index_animation_shoot
        elif self.is_reloading:
            self.float_index = increment(self.float_index, 0.5, 1)
            self.index_animation_reload = increment(self.index_animation_reload, int(self.float_index),len(self.animation_reload)-1)
            self.animation_body = self.prefix_animation_name + 'reload'
            self.animation_body_index = self.index_animation_reload
            if self.index_animation_reload == len(self.animation_reload)-1:
                self.is_reloading = False
                self.index_animation_reload = 0
            self.original_image = self.animation_reload[self.index_animation_reload]
        elif self.is_meleeattack:
            self.float_index = increment(self.float_index, 0.5, 1)
            self.index_animation_meleeattack = increment(self.index_animation_meleeattack, int(self.float_index),len(self.animation_meleeattack)-1)
            self.animation_body = self.prefix_animation_name + 'meleeattack'
            self.animation_body_index = self.index_animation_meleeattack
            if self.index_animation_meleeattack == len(self.animation_meleeattack)-1:
                self.is_meleeattack = False
                self.index_animation_meleeattack = 0
            self.original_image = self.animation_meleeattack[self.index_animation_meleeattack]
        elif self.is_idle:
            self.float_index = increment(self.float_index, 0.25, 1)
            self.index_animation_idle = increment(self.index_animation_idle, int(self.float_index), len(self.animation_idle)-1)
            self.original_image = self.animation_idle[self.index_animation_idle]
            self.animation_body = self.prefix_animation_name + 'idle'
            self.animation_body_index = self.index_animation_idle
        elif self.is_moving_forward or self.is_moving_left or self.is_moving_right:
            self.index_animation_move = increment(self.index_animation_move, 1, len(self.animation_move)-1)
            self.original_image = self.animation_move[self.index_animation_move]
            self.animation_body = self.prefix_animation_name + 'move'
            self.animation_body_index = self.index_animation_move
        
        # feet animation
        if self.is_moving_forward:
            self.original_feet = self.animation.feet_walk[self.index_animation_feet_walk]
            self.animation_feet_index = self.index_animation_feet_walk
            self.animation_feet = 'feet_walk'
            self.index_animation_feet_walk = increment(self.index_animation_feet_walk, 1, 19)
        elif self.is_moving_left:
            self.original_feet = self.animation.feet_strafe_left[self.index_animation_feet_strafe_left]
            self.animation_feet_index = self.index_animation_feet_strafe_left
            self.animation_feet = 'feet_strafe_left'
            self.index_animation_feet_strafe_left = increment(self.index_animation_feet_strafe_left, 1, 19)
        elif self.is_moving_right:
            self.original_feet = self.animation.feet_strafe_right[self.index_animation_feet_strafe_right]
            self.animation_feet_index = self.index_animation_feet_strafe_right
            self.animation_feet = 'feet_strafe_right'
            self.index_animation_feet_strafe_right = increment(self.index_animation_feet_strafe_right, 1, 19)
        else:
            self.original_feet = self.animation.feet_idle[0]
            self.animation_feet_index = 0
            self.animation_feet = 'feet_idle'

    def get_server_info(self):
        # acho que o servidor não consegue tratar o tipo pg.math.Vector2
        info = {'position_on_scenario': (self.position_on_scenario[0], self.position_on_scenario[1]),
         'angle': self.angle_vision,
         'animation_body': self.animation_body,
         'animation_body_index': self.animation_body_index,
         'animation_feet': self.animation_feet,
         'animation_feet_index': self.animation_feet_index
         }
        return info

    def set_animation_move_flags(self):
        self.is_idle = False
        if self.pressionou_a:
            self.is_moving_left = True 
            self.is_moving_right = False
            self.is_moving_forward = False
        
        if self.pressionou_d:
            self.is_moving_right = True
            self.is_moving_left = False 
            self.is_moving_forward = False
        
        if self.pressionou_w or self.pressionou_s:
            self.is_moving_left = False 
            self.is_moving_forward = True
            self.is_moving_right = False

        if not self.pressionou_a and not self.pressionou_d and not self.pressionou_s and not self.pressionou_w:
            self.is_moving_left = False
            self.is_moving_forward = False
            self.is_moving_right = False
            self.is_idle = True
            return False
        return True
