import pygame

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
        # converte  a posição da tela para a posição no campo
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
    def __init__(self, image, back_image, location_on_scenario, location_on_screen, animation, sound, background):
        super().__init__()
        self.animation = animation
        self.sound = sound
        self.back_image = back_image
        self.original_back_image = back_image
        self.original_feet = animation.feet_run[0]
        self.background = background
        self.loc = location_on_screen
        # the image center isnt correct
        self.delta_center_position = pygame.math.Vector2((+56/2.7,-19/2.7))

        self.mask = pygame.mask.from_surface(self.back_image)
        self.rect = animation.idle[0].get_rect(center = location_on_screen)
        self.rect_back = self.rect
        self.image = animation.idle[0]

        self.position_on_screen = pygame.math.Vector2(location_on_screen)
        self.position_on_scenario = pygame.math.Vector2(location_on_scenario)

        # index for animations
        self.index_animation_move = 0
        self.index_animation_shoot = 0
        self.index_animation_idle = 0
        self.index_animation_reload = 0
        self.index_animation_feet = 0

        # flags for animation
        self.is_moving = False
        self.is_shooting = False
        self.is_reloading = False
        self.is_idle = True        

        # handle events
        self.is_colliding = False
        self.pressionou_w = False
        self.pressionou_a = False
        self.pressionou_s = False
        self.pressionou_d = False


        # for statistics
        self.ammo = 20


        # auxiliar: remover depois
        self.float_index = 0

    def update(self):
        self.react_to_event()
        self.choose_animation()
        self.rotate()

    def draw(self, screen):
        screen.blit(self.feet, self.feet.get_rect(center=self.position_on_screen).topleft)
        screen.blit(self.image, self.rect)

    def choose_animation(self):
        if self.is_shooting:
            self.index_animation_shoot += 1
            if self.index_animation_shoot > 2:
                self.index_animation_shoot = 0
            self.original_image = self.animation.shoot[self.index_animation_shoot]
        elif self.is_reloading:
            self.float_index += 0.5
            if self.float_index > 1:
                self.float_index = 0
            self.index_animation_reload += int(self.float_index)
            if self.index_animation_reload > 19:
                self.index_animation_reload = 0
                self.is_reloading = False
            self.original_image = self.animation.rifle_reload[self.index_animation_reload]
        elif self.is_idle:
            self.float_index += 0.25
            if self.float_index > 1:
                self.float_index = 0
            self.index_animation_idle += int(self.float_index)
            if self.index_animation_idle > 19:
                self.index_animation_idle = 0
            self.original_image = self.animation.idle[self.index_animation_idle]
        elif self.is_moving:
            self.index_animation_move += 1
            if self.index_animation_move > 19:
                self.index_animation_move = 0
            self.original_image = self.animation.move[self.index_animation_move]

    def move(self, direction):
        if not self.is_possible_direction(direction):
            angles = get_normal(self.temp_position_on_scenario, self.background.mask, self.background.rect)
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
        self.temp_position_on_scenario = self.position_on_scenario + 5*pygame.math.Vector2(direction/ (direction.length()))
        self.temp_index_animation_move = self.index_animation_move + 1
        if self.temp_index_animation_move == len(self.animation.move):
            self.temp_index_animation_move = 0
  
        self.temp_rect = self.image.get_rect(center=self.new_rect_center)
        self.temp_mask = pygame.mask.from_surface(self.back_image)

        self.temp_rect_back = self.background.rect.copy()

        self.temp_rect_back.center = self.position_on_screen - self.temp_position_on_scenario

        self.offset = ((-self.temp_rect_back.left + self.temp_rect.left), (-self.temp_rect_back.top + self.temp_rect.top))
        self.is_colliding = self.background.mask.overlap(self.temp_mask, self.offset)

        if self.is_colliding:
            return False
        return True

    def rotate(self):
        _, angle = (pygame.mouse.get_pos()-self.position_on_screen).as_polar()

        self.angle_param = angle
        # gira todas as imagens
        self.image = pygame.transform.rotozoom(self.original_image, -angle, 1)
        self.feet = pygame.transform.rotozoom(self.original_feet, -angle, 1)
        self.back_image = pygame.transform.rotozoom(self.original_back_image, -angle, 1)

        # gira em torno do centro real
        # encontra a nova posição do centro do rect
        self.rotated_center = self.delta_center_position.rotate(+angle)
        self.new_rect_center = self.rotated_center + self.position_on_screen

        # atualiza o rect da imagem com o novo centro correto
        self.rect = self.image.get_rect(center=self.new_rect_center)
        self.rect_back = self.rect

        # atualiza a mascara relativa ao personagem
        # garante que a imagem estará sempre sobrepondo sua máscara
        self.mask = pygame.mask.from_surface(self.back_image)


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
            # [TODO] a flag deve ser setada se uma das quatro direcionais forem pressionadas
            self.is_moving = True
            self.is_idle = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.pressionou_w = False
            if event.key == pygame.K_a:
                self.pressionou_a = False
            if event.key == pygame.K_s:
                self.pressionou_s = False
            if event.key == pygame.K_d:
                self.pressionou_d = False
            # [TODO] a flag deve ser setada se uma das quatro direcionais forem pressionadas
            self.is_moving = False
            self.is_idle = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.is_reloading = True
                pygame.mixer.Channel(1).play(self.sound.reload)
                self.ammo = 20
            if event.button == 1:
                self.is_shooting = True
                #print(self.rect)
                
                # a lógica de como as munições são reduzidas deve ser alterada depois
                if self.ammo != 0:
                    self.ammo -= 1
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_shooting = False

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
        
        if self.is_shooting:
            pygame.mixer.Channel(1).play(self.sound.shoot)
        else:
            self.sound.shoot.fadeout(100)
            # self.sound.stop()
        if self.is_moving:
            self.feet = self.animation.feet_run[self.index_animation_feet]
            self.original_feet = self.animation.feet_run[self.index_animation_feet]
            self.index_animation_feet += 1
            if self.index_animation_feet > 19:
                self.index_animation_feet = 0
