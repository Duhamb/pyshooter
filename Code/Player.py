import pygame as pg
import pygame
import math
import Code.helpers as helpers
import Code.Collider as Collider
import Code.Weapon as Weapon

class Player(pygame.sprite.Sprite):
    def __init__(self, location_on_scenario, location_on_screen, animation, sound, background, aim):
        super().__init__()

        self.weapon = Weapon.Weapon()
        self.velocity = 5

        self.score = 0

        # set all animations
        self.animation = animation
        self.animation_move = self.animation.rifle_move
        self.animation_idle = self.animation.rifle_idle
        self.animation_reload = self.animation.rifle_reload
        self.animation_shoot = self.animation.rifle_shoot
        self.animation_meleeattack = self.animation.rifle_meleeattack

        # set all sounds (shoot, move, reload)
        self.sound = sound

        # define the collider shape
        self.collider_image = pg.image.load("Assets/Images/back_player.png").convert_alpha()
        self.collider_image = helpers.scale_image(self.collider_image, 2.7)
        self.rect_back = self.collider_image.get_rect(center = location_on_screen)
        self.mask = pygame.mask.from_surface(self.collider_image)
        self.rect_for_collisions = self.mask.get_bounding_rects()[0]
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
        self.collider = Collider.Collider(self.rect_for_collisions, self.background.rect)

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
        self.sound_empty_playing = False

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
        self.aim = aim

        # slower animations
        self.float_index = 0

    def update(self):
        self.choose_animation()
        self.choose_sound()
        self.rotate()
        self.react_to_event()

    def draw(self, screen):
        screen.blit(self.feet, self.feet.get_rect(center=self.position_on_screen).topleft)
        screen.blit(self.image, self.rect)

    def draw_multiplayer(self, screen, server_info):
        position_on_screen = helpers.scenario_to_screen(server_info['position_on_scenario'], self.background, False)

        _, angle = (pg.math.Vector2(server_info['mouse_position']) - pg.math.Vector2(server_info['position_on_scenario'])).as_polar()
        angle = angle - self.background.angle

        # body
        animation = getattr(self.animation, server_info['animation_body'])
        original_image = animation[server_info['animation_body_index']]
        [imageMultiplayer, rect_multiplayer] = helpers.rotate_fake_center(original_image, angle, self.delta_center_position, position_on_screen)
        
        # feet
        animation_feet = getattr(self.animation, server_info['animation_feet'])
        original_image = animation_feet[server_info['animation_feet_index']]
        [imageFeet, rect_feet] = helpers.rotate_fake_center(original_image, angle, pg.math.Vector2((0,0)), position_on_screen)
        
        # draw images
        screen.blit(imageFeet, rect_feet)
        screen.blit(imageMultiplayer, rect_multiplayer)

    def move(self, direction):
        self.position_on_scenario += self.velocity*direction
        self.collider.update(self.position_on_scenario)
        collisions = pg.sprite.spritecollide(self.collider, self.background.collider_group, False)
        
        if collisions:
            helpers.move_on_collision(self.collider, collisions, direction)
            self.position_on_scenario = helpers.image_to_scenario(self.collider.rect.center, self.background.rect)

    def rotate(self):
        # get the angle between mouse and player
        angle = -90
        try:
            D = (pg.math.Vector2(self.aim.position)-self.position_on_screen).length()
            angle -= math.degrees(math.asin(32/(2.7*D)))
        except:
            pass
        self.angle_vision = angle

        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.feet = pygame.transform.rotate(self.original_feet, -angle)
        self.collider_image = pygame.transform.rotate(self.original_back_image, -angle)

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
                if self.weapon.type != 'knife':
                    self.is_reloading = True
                    self.weapon.ammo_list[self.weapon.type] = self.weapon.ammo_limit_list[self.weapon.type]

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.weapon.type != 'knife':
                    self.is_shooting = True
                else:
                    self.is_meleeattack = True
            if event.button == 3:
                if self.weapon.type != 'knife':
                    self.is_meleeattack = True
                    pygame.mixer.Channel(1).play(self.sound.meleeattack)
                else:
                    self.is_meleeattack = True
    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_shooting = False
                self.sound.shoot.fadeout(125)

        # change weapon
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.weapon.change_weapon('rifle')
                self.change_weapon()
            elif event.key == pygame.K_2:
                self.weapon.change_weapon('shotgun')
                self.change_weapon()
            elif event.key == pygame.K_3:
                self.weapon.change_weapon('handgun')
                self.change_weapon()
            elif event.key == pygame.K_4:
                self.weapon.change_weapon('knife')
                self.change_weapon()
        
    def react_to_event(self):
        if self.pressionou_w or self.pressionou_d or self.pressionou_a or self.pressionou_s:
            self.actual_position = helpers.screen_to_scenario(self.position_on_screen, self.background)
            # self.mouse_position = screen_to_scenario(pygame.mouse.get_pos(), self.background)
            self.mouse_position = helpers.screen_to_scenario((400,200), self.background)
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

    def change_weapon(self):
        self.is_shooting = False
        if self.weapon.type == 'rifle':
            self.animation_move = self.animation.rifle_move
            self.animation_shoot = self.animation.rifle_shoot
            self.animation_idle = self.animation.rifle_idle
            self.animation_reload = self.animation.rifle_reload
            self.animation_meleeattack = self.animation.rifle_meleeattack
            self.prefix_animation_name = 'rifle_'
            # self.delta_center_position

        elif self.weapon.type == 'shotgun':
            self.animation_move = self.animation.shotgun_move
            self.animation_shoot = self.animation.shotgun_shoot
            self.animation_idle = self.animation.shotgun_idle
            self.animation_reload = self.animation.shotgun_reload
            self.animation_meleeattack = self.animation.shotgun_meleeattackd
            self.prefix_animation_name = 'shotgun_'

        elif self.weapon.type == 'handgun':
            self.animation_move = self.animation.handgun_move
            self.animation_shoot = self.animation.handgun_shoot
            self.animation_idle = self.animation.handgun_idle
            self.animation_reload = self.animation.handgun_reload
            self.animation_meleeattack = self.animation.handgun_meleeattack
            self.prefix_animation_name = 'handgun_'

        elif self.weapon.type == 'knife':
            self.animation_move = self.animation.knife_move
            self.animation_idle = self.animation.knife_idle
            self.animation_meleeattack = self.animation.knife_meleeattack
            self.prefix_animation_name = 'knife_'

    def choose_sound(self):
        # Reloading sound
        if self.is_reloading and not self.sound_empty_playing:
            self.sound.empty.stop()
            pygame.mixer.Channel(1).play(self.sound.reload)
            self.sound_empty_playing = True
        if not self.is_reloading:
            self.sound_empty_playing = False

    def choose_animation(self):
        # body animation
        if self.is_reloading:
            self.float_index = helpers.increment(self.float_index, 0.5, 1)
            self.index_animation_reload = helpers.increment(self.index_animation_reload, int(self.float_index),len(self.animation_reload)-1)

            self.animation_body = self.prefix_animation_name + 'reload'
            self.animation_body_index = self.index_animation_reload
            if self.index_animation_reload == len(self.animation_reload)-1:
                self.is_reloading = False
                self.index_animation_reload = 0
            self.original_image = self.animation_reload[self.index_animation_reload]

        elif self.is_shooting and self.weapon.ammo_list[self.weapon.type] > 0:
            self.index_animation_shoot = helpers.increment(self.index_animation_shoot, 1, len(self.animation_shoot)-1)
            self.original_image = self.animation_shoot[self.index_animation_shoot]
            self.animation_body = self.prefix_animation_name + 'shoot'
            self.animation_body_index = self.index_animation_shoot

        elif self.is_meleeattack:
            self.float_index = helpers.increment(self.float_index, 1, 1)
            self.index_animation_meleeattack = helpers.increment(self.index_animation_meleeattack, int(self.float_index),len(self.animation_meleeattack)-1)
            self.animation_body = self.prefix_animation_name + 'meleeattack'
            self.animation_body_index = self.index_animation_meleeattack
            if self.index_animation_meleeattack == len(self.animation_meleeattack)-1:
                self.is_meleeattack = False
                self.index_animation_meleeattack = 0
            self.original_image = self.animation_meleeattack[self.index_animation_meleeattack]

        elif self.is_idle:
            self.float_index = helpers.increment(self.float_index, 0.25, 1)
            self.index_animation_idle = helpers.increment(self.index_animation_idle, int(self.float_index), len(self.animation_idle)-1)
            self.original_image = self.animation_idle[self.index_animation_idle]
            self.animation_body = self.prefix_animation_name + 'idle'
            self.animation_body_index = self.index_animation_idle

        elif self.is_moving_forward or self.is_moving_left or self.is_moving_right:
            self.index_animation_move = helpers.increment(self.index_animation_move, 1, len(self.animation_move)-1)
            self.original_image = self.animation_move[self.index_animation_move]
            self.animation_body = self.prefix_animation_name + 'move'
            self.animation_body_index = self.index_animation_move
        
        # feet animation
        if self.is_moving_forward:
            self.original_feet = self.animation.feet_walk[self.index_animation_feet_walk]
            self.animation_feet_index = self.index_animation_feet_walk
            self.animation_feet = 'feet_walk'
            self.index_animation_feet_walk = helpers.increment(self.index_animation_feet_walk, 1, 19)
        elif self.is_moving_left:
            self.original_feet = self.animation.feet_strafe_left[self.index_animation_feet_strafe_left]
            self.animation_feet_index = self.index_animation_feet_strafe_left
            self.animation_feet = 'feet_strafe_left'
            self.index_animation_feet_strafe_left = helpers.increment(self.index_animation_feet_strafe_left, 1, 19)
        elif self.is_moving_right:
            self.original_feet = self.animation.feet_strafe_right[self.index_animation_feet_strafe_right]
            self.animation_feet_index = self.index_animation_feet_strafe_right
            self.animation_feet = 'feet_strafe_right'
            self.index_animation_feet_strafe_right = helpers.increment(self.index_animation_feet_strafe_right, 1, 19)
        else:
            self.original_feet = self.animation.feet_idle[0]
            self.animation_feet_index = 0
            self.animation_feet = 'feet_idle'

    def get_server_info(self):
        # acho que o servidor não consegue tratar o tipo pg.math.Vector2
        info = {'position_on_scenario': (self.position_on_scenario[0], self.position_on_scenario[1]),
         'position_on_screen': (self.position_on_screen[0], self.position_on_screen[1]),
         'angle': self.angle_vision,
         'mouse_position': helpers.screen_to_scenario(self.aim.position, self.background, False),
         'animation_body': self.animation_body,
         'animation_body_index': self.animation_body_index,
         'animation_feet': self.animation_feet,
         'animation_feet_index': self.animation_feet_index,
         'weapon_type': self.weapon.type
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
