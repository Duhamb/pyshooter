# this file has constant values and auxiliar functions used in whole game

import pygame as pg


######################   FUNCTIONS    ##################################


# this function return the position on screen based on other coordinates
# is needed because all orientation is made by scenario position and
# render functions use screen position
def scenario_to_screen(position_on_scenario, scenario_rect):
    return position_on_scenario + scenario_rect.center

# this function return the position on scenario based on other coordinates
# see comments of scenario_to_screen function
def screen_to_scenario(position_on_screen, scenario_rect):
    return position_on_screen - scenario_rect.center

def screen_to_scenario_server(position_on_screen, scenario_rect):
    x = position_on_screen[0] - scenario_rect.centerx
    y = position_on_screen[1] - scenario_rect.centery
    return (x,y)

def scenario_to_screen_server(position_on_scenario, scenario_rect):
    x = position_on_scenario[0] + scenario_rect.centerx
    y = position_on_scenario[1] + scenario_rect.centery
    return (x,y)

# this function return the center of background image based on other coordinates
def background_center_position(position_on_screen, position_on_scenario):
    return position_on_screen - position_on_scenario

def convert_scenario_to_screen(background, position_on_scenario):
    change_basis = change_basis_matrix(background)
    position_on_screen = matrix_vector_mult(change_basis, position_on_scenario)
    return pg.math.Vector2(position_on_screen) + background.origin_axis

def convert_screen_to_scenario(background, position_on_screen):
    change_basis = change_basis_matrix(background)
    change_basis = matrix_inverse(change_basis)
    position_on_scenario = matrix_vector_mult(change_basis, position_on_screen)
    return pg.math.Vector2(position_on_scenario) - background.origin_axis

# create che change basis matrix from background and screen coordinates
# change screen to scenario
def change_basis_matrix(background):
    a11 = background.x_axis.dot(pg.math.Vector2((1, 0)))
    a12 = background.y_axis.dot(pg.math.Vector2((1, 0)))
    a21 = background.x_axis.dot(pg.math.Vector2((0, 1)))
    a22 = background.y_axis.dot(pg.math.Vector2((0, 1)))
    return [[a11, a12], [a21, a22]]

def matrix_inverse(matrix):
    det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    aux = matrix[0][0]
    matrix[0][0] = matrix[1][1]
    matrix[1][1] = aux
    matrix[1][0] *= -1
    matrix[0][1] *= -1
    for i in range(0, 2):
        for j in range(0, 2):
            matrix[i][j] /= det
    return matrix

def matrix_vector_mult(matrix, vector):
    a11 = matrix[0][0] * vector[0] + matrix[0][1] * vector[1]
    a21 = matrix[1][0] * vector[0] + matrix[1][1] * vector[1]
    return (a11, a21)

def scale_image_list(image_list, ratio):
    list_size = len(image_list)
    w, h = image_list[0].get_rect().size
    new_list = []
    for i in range(0, list_size):
        new_list.append(pg.transform.scale(image_list[i], (int(w / ratio), int(h / ratio))))
    return new_list

def scale_image(image, ratio):
    w, h = image.get_rect().size
    return pg.transform.scale(image, (int(w / ratio), int(h / ratio)))

def load_image_list(directory, extension, quantity):
    new_list = []
    for i in range(0, quantity):
        actual_file = directory + str(i) + extension
        new_list.append(pg.image.load(actual_file))
    return new_list

def increment(acc, increment, limit):
    acc += increment
    if acc > limit:
        acc = 0
    return acc

def rotate_fake_center(image, angle, offset, position_on_screen):
    new_image = pg.transform.rotate(image, -angle)
    rotated_center = offset.rotate(angle)
    new_rect_center = rotated_center + position_on_screen
    rect = new_image.get_rect(center=new_rect_center)
    return [new_image, rect]

def get_normal(position_on_scenario, background):
    qtd = 60
    vetor_base = pg.math.Vector2( (35,0) )
    angulo = 0
    lista_de_angulos = []
    angulo_inicial = None
    angulo_final = None

    position_on_screen = scenario_to_screen(position_on_scenario, background.rect)

    for i in range(0,qtd):
        vetor_rotacionado = pg.math.Vector2(position_on_screen) + vetor_base.rotate(angulo)
        pos_scenario =  -pg.math.Vector2(background.rect.topleft) + vetor_rotacionado
        x = int(pos_scenario[0])
        y = int(pos_scenario[1])

        if background.mask.get_at((x,y)):
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
