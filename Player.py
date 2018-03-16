import pygame
from helpers import *

# esse método de colisão tá bugado, mas apresenta desempenho minimamente razoável
# continuarei pensando em como consertar essa parte
def get_normal(position_on_scenario, back_mask, back_rect):
    qtd = 60
    vetor_base = pygame.math.Vector2( (35,0) )
    angulo = 0
    lista_de_angulos = []
    angulo_inicial = None
    angulo_final = None

    position_on_screen = back_rect.center + position_on_scenario

    for i in range(0,qtd):
        vetor_rotacionado = pygame.math.Vector2(position_on_screen) + vetor_base.rotate(angulo)
        pos_scenario =  -pygame.math.Vector2(back_rect.topleft) + vetor_rotacionado
        x = int(pos_scenario[0])
        y = int(pos_scenario[1])

        if back_mask.get_at((x,y)):
            if angulo_inicial == None:
                angulo_inicial = angulo
            else:
                angulo_final = angulo
        else:
            if angulo_final != None:
                diff = [angulo_inicial, angulo_final]
                lista_de_angulos.append( diff )
                
                angulo_final = None
                angulo_inicial = None

        angulo += 360/qtd
    if angulo_inicial != None and angulo_final != None:
        diff = [angulo_inicial, angulo_final]
        lista_de_angulos.append( diff )

    first = lista_de_angulos[0]
    last = lista_de_angulos[-1]
    if first[0] == 0 and last[1] == 354:
        first[0] = last[0]
        del lista_de_angulos[-1]

    for i in range(0, len(lista_de_angulos)):
        a = lista_de_angulos[i][0]
        b = lista_de_angulos[i][1]
        if a > b:
            lista_de_angulos[i] = [(a+b)/2-180, b-a+360]
        else:
            lista_de_angulos[i] = [(a+b)/2, b-a]

    return lista_de_angulos

class Player(pygame.sprite.Sprite):
    def __init__(self, location_on_scenario, location_on_screen, animation, sound, background):
        super().__init__()

        # set all animations
        self.animation = animation

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
        self.image = animation.idle[0]
        self.rect = self.image.get_rect(center = location_on_screen)

        # positions
        self.position_on_screen = pygame.math.Vector2(location_on_screen)
        self.position_on_scenario = pygame.math.Vector2(location_on_scenario)

        # index for animations
        self.index_animation_move = 0
        self.index_animation_shoot = 0
        self.index_animation_idle = 0
        self.index_animation_reload = 0
        self.index_animation_feet_walk = 0
        self.index_animation_feet_strafe_left = 0
        self.index_animation_feet_strafe_right = 0

        # flags for animation
        self.is_moving_forward = False
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_shooting = False
        self.is_reloading = False
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

        # slower animations
        self.float_index = 0

    def update(self):
        self.react_to_event()
        self.choose_animation()
        self.rotate()

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
            angles = get_normal(self.next_position_on_scenario, self.background.mask, self.background.rect)
            if len(angles) <= 1:
                big_size = False
                for k in angles:
                    if k[1] > 150:
                        big_size = True
                        break
                if not big_size:
                    for j in angles:
                        i = j[0]
                        new_direction = pygame.math.Vector2((1,0)).rotate(i + 90)
                        try:
                            new_direction = new_direction.dot(5*pygame.math.Vector2(direction/(direction.length()))) * new_direction
                        except:
                            new_direction = pygame.math.Vector2(0,0)
                        direction = new_direction

                    try:
                        self.position_on_scenario += 5*(direction/(direction.length()))
                    except:
                        self.position_on_scenario += 5*(direction)
        else:
            try:
                self.position_on_scenario += 5*(direction/(direction.length()))
            except: 
                self.position_on_scenario += 5*(direction)

    def is_possible_direction(self, direction):
        # prevê o estado caso o movimento ocorra
        self.next_position_on_scenario = self.position_on_scenario + 5*pygame.math.Vector2(direction/ (direction.length()))
        self.next_index_animation_move = increment(self.index_animation_move, 1, len(self.animation.move))
  
        self.next_rect = self.image.get_rect(center = self.new_rect_center)
        self.next_mask = pygame.mask.from_surface(self.collider_image)

        self.next_rect_background = self.background.rect.copy()

        # this command obtain the next position of background
        self.next_rect_background.center = background_center_position(self.position_on_screen, self.next_position_on_scenario)

        self.offset = ((self.next_rect.left - self.next_rect_background.left ), (self.next_rect.top - self.next_rect_background.top))
        self.is_colliding = self.background.mask.overlap(self.next_mask, self.offset)

        if self.is_colliding:
            return False
        return True

    def rotate(self):
        # get the angle between mouse and player
        _, angle = (pygame.mouse.get_pos()-self.position_on_screen).as_polar()
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
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.is_reloading = True
                pygame.mixer.Channel(1).play(self.sound.reload)
            if event.button == 1:
                if not self.is_shooting:
                    pygame.mixer.Channel(1).play(self.sound.shoot, -1)
                self.is_shooting = True
    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_shooting = False
                self.sound.shoot.fadeout(125)

    def react_to_event(self):
        if self.pressionou_w or self.pressionou_d or self.pressionou_a or self.pressionou_s:
            self.actual_position = self.position_on_screen
            self.mouse_position = pygame.mouse.get_pos()
            self.vector_position = self.mouse_position - self.actual_position

            if self.pressionou_w:
                self.direction_of_move = (self.vector_position)
                self.move(self.direction_of_move)

            if self.pressionou_s:
                self.direction_of_move = -(self.vector_position)
                self.move(self.direction_of_move)

            if self.pressionou_a:
                self.direction_of_move = -(self.vector_position).rotate(90)
                self.move(self.direction_of_move)

            if self.pressionou_d:
                self.direction_of_move = (self.vector_position).rotate(90)
                self.move(self.direction_of_move)
    
    def choose_animation(self):
        # body animation
        if self.is_shooting:
            self.index_animation_shoot = increment(self.index_animation_shoot, 1, 2)
            self.original_image = self.animation.shoot[self.index_animation_shoot]
            self.animation_body = 'shoot'
            self.animation_body_index = self.index_animation_shoot
        elif self.is_reloading:
            self.float_index = increment(self.float_index, 0.5, 1)
            self.index_animation_reload = increment(self.index_animation_reload,int(self.float_index),19)
            self.animation_body = 'rifle_reload'
            self.animation_body_index = self.index_animation_reload
            if self.index_animation_reload == 19:
                self.is_reloading = False
                self.index_animation_reload = 0
            self.original_image = self.animation.rifle_reload[self.index_animation_reload]
        elif self.is_idle:
            self.float_index = increment(self.float_index, 0.25, 1)
            self.index_animation_idle = increment(self.index_animation_idle, int(self.float_index), 19)
            self.original_image = self.animation.idle[self.index_animation_idle]
            self.animation_body = 'idle'
            self.animation_body_index = self.index_animation_idle
        elif self.is_moving_forward or self.is_moving_left or self.is_moving_right:
            self.index_animation_move = increment(self.index_animation_move, 1, 19)
            self.original_image = self.animation.move[self.index_animation_move]
            self.animation_body = 'move'
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
