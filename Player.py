import pygame
import pygame.gfxdraw
import math

# [TODO] descobrir como alterar o group.draw pra renderizar duas imagens
# alternativa: unir as duas imagens e passar somente a união delas
def draw_rect(rect, screen):
    pygame.draw.line(screen, (255,0,0), rect.topleft, rect.topright, 1)
    pygame.draw.line(screen, (255,0,0), rect.bottomleft, rect.bottomright, 1)
    pygame.draw.line(screen, (255,0,0), rect.topleft, rect.bottomleft, 1)
    pygame.draw.line(screen, (255,0,0), rect.topright, rect.bottomright, 1)

def create_segments(list_points, pos_back):
    segment_list = []
    for points in list_points:
        points.append(points[0])
        for i in range(0, len(points)-1):
            screen_pos_1 = pygame.math.Vector2(pos_back) + pygame.math.Vector2(points[i])
            screen_pos_2 = pygame.math.Vector2(pos_back) + pygame.math.Vector2(points[i+1])
            if screen_pos_1[0] > 700 or screen_pos_1[0] < 100 or screen_pos_1[1] > 500 or screen_pos_1[1] < 100 or screen_pos_2[0] > 700 or screen_pos_2[0] < 100 or screen_pos_2[1] > 500 or screen_pos_2[1] < 100:
                pass
            else:
                new_segment = {"a":{"x":screen_pos_1[0],"y":screen_pos_1[1]}, "b":{"x":screen_pos_2[0],"y":screen_pos_2[1]}}
                segment_list.append(new_segment)

    segment_list.append({"a":{"x":800,"y":0}, "b":{"x":0,"y":0}})
    segment_list.append({"a":{"x":0,"y":600}, "b":{"x":0,"y":0}})
    segment_list.append({"a":{"x":800,"y":600}, "b":{"x":800,"y":0}})
    segment_list.append({"a":{"x":800,"y":600}, "b":{"x":0,"y":600}})
    return segment_list


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

def draw_rays(screen, position_on_scenario, back_mask, back_rect):
    qtd = 60
    vetor_base = pygame.math.Vector2( (35,0) )
    angulo = 0
    lista_de_angulos = []
    angulo_inicial = None
    angulo_final = None

    position_on_screen = back_rect.center + position_on_scenario
    ha_zero = None
    ha_final = None
    for i in range(0,qtd):
        vetor_rotacionado = pygame.math.Vector2(position_on_screen) + vetor_base.rotate(angulo)
        # converte  a posição da tela para a posição no campo
        pos_scenario =  -pygame.math.Vector2(back_rect.topleft) + vetor_rotacionado
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
        pygame.draw.line(screen, cor, position_on_screen, vetor_rotacionado, 2)
        angulo += 360/qtd

    if angulo_inicial != None and angulo_final != None:
        diff = (angulo_final, angulo_inicial)
        lista_de_angulos.append( diff )

    if ha_zero != None and ha_final != None:
        diff = (ha_zero + ha_final)/2 - 180
        lista_de_angulos.append( diff )

    return lista_de_angulos 


def draw_vision(screen, position_on_scenario, back_mask, back_rect):
    qtd = 60
    vetor_base_original = pygame.math.Vector2( (1,0) )
    angulo = 0

    position_on_screen = back_rect.center + position_on_scenario

    for i in range(0,qtd):
        # print(angulo)
        

        # pygame.draw.line(screen, (0,255,255), position_on_screen, vetor_rotacionado_original*50, 2)
        # converte  a posição da tela para a posição no campo
        mult = 1
        bateu = False

        while not bateu: 
            vetor_base = vetor_base_original*mult
            vetor_rotacionado = pygame.math.Vector2(position_on_screen) + vetor_base.rotate(angulo)
            # vetor_rotacionado = mult*vetor_rotacionado_original
            # if vetor_rotacionado[0] > 800 or vetor_rotacionado[0] < 0 or vetor_rotacionado[1] > 600 or vetor_rotacionado[1] < 0:
            #     pygame.draw.line(screen, (0,255,0), position_on_screen, vetor_rotacionado, 2)
            #     print('bateu 1')
            #     bateu = True
            # else:

            # print(vetor_rotacionado)

            pos_scenario =  -pygame.math.Vector2(back_rect.topleft) + vetor_rotacionado
            x = int(pos_scenario[0])
            y = int(pos_scenario[1])
            try:
                ponto = back_mask.get_at((x,y))
                if ponto:
                    pygame.draw.line(screen, (0,255,0), position_on_screen, vetor_rotacionado, 2)
                    bateu = True
                    # print('bateu 2')
                else:
                    mult += 1
            except:
                pygame.draw.line(screen, (0,255,0), position_on_screen, vetor_rotacionado, 2)
                bateu = True
                # print('bateu 3')
        angulo += 360/qtd
   

class Player(pygame.sprite.Sprite):
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
        self.delta_center_position = pygame.math.Vector2((+56/2.7,-19/2.7))

        self.mask = pygame.mask.from_surface(self.back_image)
        self.rect = animation.move[0].get_rect(center = location_on_screen)
        self.rect_back = self.rect
        self.image = animation.move[0]

        self.position_on_screen = pygame.math.Vector2(location_on_screen)
        self.position_on_scenario = pygame.math.Vector2(location_on_scenario)

        self.is_colliding = False
        # handle events
        self.pressionou_w = False
        self.pressionou_a = False
        self.pressionou_s = False
        self.pressionou_d = False
        self.is_shooting = False


        # teste
        self.vision = SightAndLight(self.position_on_screen)

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
        pygame.draw.lines(screen,(200,150,150), 1, olist)
        if self.pressionou_w or self.pressionou_d or self.pressionou_a or self.pressionou_s:
            new_segments = create_segments(self.background.list_points, self.background.rect.topleft)
            self.vision.run(screen, new_segments, self.angle_param)

        # draw_rect(self.rect, screen)
        # draw_rays(screen, self.position_on_scenario, self.background.mask, self.background.rect)
        
        # draw_vision(screen, self.position_on_scenario, self.background.mask, self.background.rect)
            
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
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.pressionou_w = False
            if event.key == pygame.K_a:
                self.pressionou_a = False
            if event.key == pygame.K_s:
                self.pressionou_s = False
            if event.key == pygame.K_d:
                self.pressionou_d = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.is_shooting = True
        elif event.type == pygame.MOUSEBUTTONUP:
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



##########################################################################################################
class SightAndLight():
    def __init__(self, location_on_screen):
        # segments
        self.mouse_pos = location_on_screen
        
        self.segments = []
        self.angle_param = None
        # intersects
        self.intersects = []
        self.screen = None
        # Points
        self.points = []

    def run(self, screen, new_segments, angle_param):
        self.screen = screen
        self.angle_param = angle_param
        self.segments = new_segments
        self.update()
        self.render_frame()

    def update(self):
        # Clear old points
        self.points = []

        # Get all unique points
        for segment in self.segments:
            self.points.append((segment['a'], segment['b']))

        unique_points = []
        for point in self.points:
            if point not in unique_points:
                unique_points.append(point)

        # Get all angles
        unique_angles = []
        for point in unique_points:
            angle = math.atan2(point[0]["y"]-self.mouse_pos[1], point[0]["x"]-self.mouse_pos[0])
            print(math.degrees(angle) )
            if math.degrees(angle) < self.angle_param -90 + 50 or math.degrees(angle) > self.angle_param -90 - 50:
                point[0]["angle"] = angle
                unique_angles.append(angle-0.00001)
                unique_angles.append(angle)
                unique_angles.append(angle+0.00001)

        # RAYS IN ALL DIRECTIONS
        self.intersects = []
        for angle in unique_angles:
            # Calculate dx & dy from angle
            dx = math.cos(angle)
            dy = math.sin(angle)

            # Ray from center of screen to mouse
            ray = {
                    "a": {"x":self.mouse_pos[0], "y": self.mouse_pos[1]},
                    "b": {"x": self.mouse_pos[0]+dx, "y": self.mouse_pos[1]+dy}
            }

            # Find CLOSEST intersection
            closest_intersect = None
            for segment in self.segments:
                intersect = self.get_intersection(ray, segment)
                if not intersect: continue
                if not closest_intersect or intersect["param"] < closest_intersect["param"]:
                    closest_intersect = intersect

            # Intersect angle
            if not closest_intersect: continue
            closest_intersect["angle"] = angle

            # Add to list of intersects
            self.intersects.append(closest_intersect)

        # Sort intersects by angle
        self.intersects = sorted(self.intersects, key=lambda k: k['angle'])

    def render_frame(self):

        # draw segments
        # for segment in self.segments:
        #     pygame.draw.aaline(self.screen, (153, 153, 153), (segment['a']['x'], segment['a']['y']), (segment['b']['x'], segment['b']['y']))

        self.draw_polygon(self.intersects, (221, 56, 56))

        # draw debug lines
        for intersect in self.intersects:
            pygame.draw.aaline(self.screen, (255, 85, 85), self.mouse_pos, (intersect['x'], intersect['y']))

    def get_intersection(self, ray, segment):
        ''' Find intersection of RAY & SEGMENT '''
        # RAY in parametric: Point + Direction*T1
        r_px = ray['a']['x']
        r_py = ray['a']['y']
        r_dx = ray['b']['x'] - ray['a']['x']
        r_dy = ray['b']['y'] - ray['a']['y']

        # SEGMENT in parametric: Point + Direction*T2
        s_px = segment['a']['x']
        s_py = segment['a']['y']
        s_dx = segment['b']['x'] - segment['a']['x']
        s_dy = segment['b']['y'] - segment['a']['y']

        # Are they parallel? If so, no intersect
        r_mag = math.sqrt(r_dx*r_dx+r_dy*r_dy)
        s_mag = math.sqrt(s_dx*s_dx+s_dy*s_dy)
        if r_mag!=0 and s_mag!=0:
            if r_dx/r_mag == s_dx/s_mag and r_dy/r_mag == s_dy/s_mag:
                return None
        else:
            return None
        try:
            T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx)
        except:
            # T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx-0.01)
            T2 = 32000000

        try:
            T1 = (s_px+s_dx*T2-r_px)/r_dx
        except:
            # T1 = (s_px+s_dx*T2-r_px)/(r_dx-0.01)
            T1 = 32000000

        if T1 < 0: return None
        if T2 < 0 or T2>1: return None

        return {
                "x": r_px+r_dx*T1,
                "y": r_py+r_dy*T1,
                "param": T1
        }

    def draw_polygon(self, polygon, color):
        # collect coordinates for a giant polygon
        points = []
        for intersect in polygon:
            points.append((intersect['x'], intersect['y']))
        
        # draw as a giant polygon
        pygame.gfxdraw.aapolygon(self.screen, points, color)
        pygame.gfxdraw.filled_polygon(self.screen, points, color)
