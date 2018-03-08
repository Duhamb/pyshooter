import pygame as pg

# [TODO] descobrir como alterar o group.draw pra renderizar duas imagens
# alternativa: unir as duas imagens e passar somente a união delas
def draw_rect(rect, screen):
    pg.draw.line(screen, (255,0,0), rect.topleft, rect.topright, 1)
    pg.draw.line(screen, (255,0,0), rect.bottomleft, rect.bottomright, 1)
    pg.draw.line(screen, (255,0,0), rect.topleft, rect.bottomleft, 1)
    pg.draw.line(screen, (255,0,0), rect.topright, rect.bottomright, 1)

def get_normal(position_on_scenario, back_mask, back_rect):
    qtd = 60
    vetor_base = pg.math.Vector2( (35,0) )
    angulo = 0
    lista_de_angulos = []
    angulo_inicial = None
    angulo_final = None

    position_on_screen = back_rect.center + position_on_scenario

    for i in range(0,qtd):
        vetor_rotacionado = pg.math.Vector2(position_on_screen) + vetor_base.rotate(angulo)
        # converte  a posição da tela para a posição no campo
        pos_scenario =  -pg.math.Vector2(back_rect.topleft) + vetor_rotacionado
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

def draw_rays(screen, position_on_scenario, back_mask, back_rect):
    qtd = 60
    vetor_base = pg.math.Vector2( (35,0) )
    angulo = 0
    lista_de_angulos = []
    angulo_inicial = None
    angulo_final = None

    position_on_screen = back_rect.center + position_on_scenario
    ha_zero = None
    ha_final = None
    for i in range(0,qtd):
        vetor_rotacionado = pg.math.Vector2(position_on_screen) + vetor_base.rotate(angulo)
        # converte  a posição da tela para a posição no campo
        pos_scenario =  -pg.math.Vector2(back_rect.topleft) + vetor_rotacionado
        x = int(pos_scenario[0])
        y = int(pos_scenario[1])

        if back_mask.get_at((x,y)):
            cor = (255,0,0)
            if angulo_inicial == None:
                angulo_inicial = angulo
            else:
                angulo_final = angulo
        else:
            cor = (0,255,0)
            if angulo_final != None:
                if angulo_inicial == 0:
                    ha_zero = angulo_final
                elif angulo_final == 354:
                    ha_final = angulo_inicial
                else:
                    diff = (angulo_final + angulo_inicial)/2
                    lista_de_angulos.append( diff )
                
                angulo_final = None
                angulo_inicial = None
        pg.draw.line(screen, cor, position_on_screen, vetor_rotacionado, 2)
        angulo += 360/qtd

    if angulo_inicial != None and angulo_final != None:
        diff = (angulo_final, angulo_inicial)
        lista_de_angulos.append( diff )

    if ha_zero != None and ha_final != None:
        diff = (ha_zero + ha_final)/2 - 180
        lista_de_angulos.append( diff )

    return lista_de_angulos    

class Player(pg.sprite.Sprite):
    def __init__(self, image, back_image, location_on_scenario, location_on_screen, animation, sound, background):
        super().__init__()
        self.animation = animation
        self.sound = sound
        self.index_animation_move = 0        
        self.index_animation_shoot = 0
        self.back_image = back_image
        self.original_back_image = back_image
        self.background = background
        self.loc = location_on_screen
        # the image center isnt correct
        self.delta_center_position = pg.math.Vector2((+56/2.7,-19/2.7))

        self.mask = pg.mask.from_surface(self.back_image)
        self.rect = animation.move[0].get_rect(center = location_on_screen)
        self.rect_back = self.rect
        self.image = animation.move[0]

        self.position_on_screen = pg.math.Vector2(location_on_screen)
        self.position_on_scenario = pg.math.Vector2(location_on_scenario)

        self.is_colliding = False
        # handle events
        self.pressionou_w = False
        self.pressionou_a = False
        self.pressionou_s = False
        self.pressionou_d = False
        self.is_shooting = False

    def update(self):
        self.react_to_event()
        self.rotate()

    # esse metodo não sobrescreveu
    # a draw é um metodo do grupo
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.image, (0,0))
        # screen.blit(self.feet, self.position_on_screen)
        # screen.blit(self.back_image, self.rect_back)
        olist = self.mask.outline()
        pg.draw.lines(screen,(200,150,150), 1, olist)

        # draw_rect(self.rect, screen)
        # draw_rays(screen, self.position_on_scenario, self.background.mask, self.background.rect)
            
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
                        new_direction = pg.math.Vector2((1,0)).rotate(i + 90)
                        try:
                            new_direction = new_direction.dot(5*pg.math.Vector2(direction/(direction.length()))) * new_direction
                        except:
                            new_direction = pg.math.Vector2(0,0)
                        direction = new_direction

                    try:
                        self.position_on_scenario += 5*(direction/(direction.length()))
                    except:
                        self.position_on_scenario += 5*(direction)
                    self.index_animation_move += 1
                    if self.index_animation_move == len(self.animation.move):
                        self.index_animation_move = 0

        else:
            try:
                self.position_on_scenario += 5*(direction/(direction.length()))
            except: 
                self.position_on_scenario += 5*(direction)
            self.index_animation_move += 1
            if self.index_animation_move == len(self.animation.move):
                self.index_animation_move = 0

    def is_possible_direction(self, direction):
        # prevê o estado caso o movimento ocorra
        self.temp_position_on_scenario = self.position_on_scenario + 5*pg.math.Vector2(direction/ (direction.length()))
        self.temp_index_animation_move = self.index_animation_move + 1
        if self.temp_index_animation_move == len(self.animation.move):
            self.temp_index_animation_move = 0
  
        self.temp_rect = self.image.get_rect(center=self.new_rect_center)
        self.temp_mask = pg.mask.from_surface(self.back_image)

        self.temp_rect_back = self.background.rect.copy()

        self.temp_rect_back.center = self.position_on_screen - self.temp_position_on_scenario

        self.offset = ((-self.temp_rect_back.left + self.temp_rect.left), (-self.temp_rect_back.top + self.temp_rect.top))
        self.is_colliding = self.background.mask.overlap(self.temp_mask, self.offset)

        if self.is_colliding:
            return False
        return True

    def rotate(self):
        _, angle = (pg.mouse.get_pos()-self.position_on_screen).as_polar()
        # gira todas as imagens
        self.image = pg.transform.rotozoom(self.original_image, -angle, 1)
        self.feet = pg.transform.rotozoom(self.original_feet, -angle, 1)
        self.back_image = pg.transform.rotozoom(self.original_back_image, -angle, 1)

        # gira em torno do centro real
        # encontra a nova posição do centro do rect
        self.rotated_center = self.delta_center_position.rotate(+angle)
        self.new_rect_center = self.rotated_center + self.position_on_screen

        # atualiza o rect da imagem com o novo centro correto
        self.rect = self.image.get_rect(center=self.new_rect_center)
        self.rect_back = self.rect

        # atualiza a mascara relativa ao personagem
        # garante que a imagem estará sempre sobrepondo sua máscara
        self.mask = pg.mask.from_surface(self.back_image)


    # esse metodo pode estar no grupo também
    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.pressionou_w = True
            if event.key == pg.K_a:
                self.pressionou_a = True
            if event.key == pg.K_s:
                self.pressionou_s = True
            if event.key == pg.K_d:
                self.pressionou_d = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_w:
                self.pressionou_w = False
            if event.key == pg.K_a:
                self.pressionou_a = False
            if event.key == pg.K_s:
                self.pressionou_s = False
            if event.key == pg.K_d:
                self.pressionou_d = False

        if event.type == pg.MOUSEBUTTONDOWN:
            self.is_shooting = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.is_shooting = False

    def react_to_event(self):
        if self.pressionou_w or self.pressionou_d or self.pressionou_a or self.pressionou_s:
            self.actual_position = self.position_on_screen
            self.mouse_position = pg.mouse.get_pos()
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
            self.sound.play()
            # self.sound.zoa.play()

            self.image = self.animation.shoot[self.index_animation_shoot]
            self.original_image = self.animation.shoot[self.index_animation_shoot]
            self.index_animation_shoot += 1
            if self.index_animation_shoot == len(self.animation.shoot):
                self.index_animation_shoot = 0
        else:
            self.sound.shoot.fadeout(100)
            # self.sound.stop()
            self.image = self.animation.move[self.index_animation_move]
            self.original_image = self.animation.move[self.index_animation_move]

        self.feet = self.animation.run[self.index_animation_move]
        self.original_feet = self.animation.run[self.index_animation_move]