# this file has constant values and auxiliar functions used in whole game

import pygame as pg
import constants
######################   FUNCTIONS    ##################################

# this function return the center of background image based on other coordinates
def background_center_position(position_on_screen, position_on_scenario, angle):
    # pygame returns -90 when player is correct
    if angle!=None:
        real_angle = angle # fix angle necessary
    else:
        real_angle = 0
    rotated_position_on_scenario = position_on_scenario.rotate(real_angle)
    rotated_center = position_on_screen - rotated_position_on_scenario
    return rotated_center
    # return position_on_screen - position_on_scenario

def scenario_to_screen(position_on_scenario, background, vector2=True):
    change_basis = change_basis_matrix(background)
    position_on_screen = matrix_vector_mult(change_basis, position_on_scenario)
    answer_vector = pg.math.Vector2(position_on_screen) + background.origin_axis
    
    if vector2:
        return pg.math.Vector2((answer_vector[0],answer_vector[1]))
    else:
        return (answer_vector[0],answer_vector[1])

def screen_to_scenario(position_on_screen_original, background, vector2=True):
    position_on_screen = pg.math.Vector2(position_on_screen_original) - pg.math.Vector2(background.origin_axis)
    change_basis = matrix_inverse(change_basis_matrix(background))
    position_on_scenario = matrix_vector_mult(change_basis, position_on_screen)
    answer_vector = pg.math.Vector2(position_on_scenario) 
    
    if vector2:
        return pg.math.Vector2((answer_vector[0],answer_vector[1]))
    else:
        return (answer_vector[0],answer_vector[1])


# create che change basis matrix from background and screen coordinates
# change screen to scenario
def change_basis_matrix(background):
    a11 = background.x_axis[0]
    a12 = background.y_axis[0]
    a21 = background.x_axis[1]
    a22 = background.y_axis[1]
    return [[a11, a12], [a21, a22]]

def matrix_inverse(matrix):
    a11 = matrix[1][1]
    a12 = -matrix[0][1]
    a21 = -matrix[1][0]
    a22 = matrix[0][0]
    return [[a11, a12], [a21, a22]]

def matrix_vector_mult(matrix, vector):
    a11 = matrix[0][0] * vector[0] + matrix[0][1] * vector[1]
    a21 = matrix[1][0] * vector[0] + matrix[1][1] * vector[1]
    return (a11, a21)

# translate an image coordinate to scenario coordinate
# scenario origin is the center
# image origin is the topleft
def image_to_scenario(position_on_image, background_rect, vector=True):
    x = position_on_image[0] - background_rect.width/2
    y = position_on_image[1] - background_rect.height/2
    if vector:
        return pg.math.Vector2((x,y))
    else:
        return (x,y)

def scenario_to_image(position_on_scenario, background_rect, vector=True):
    x = position_on_scenario[0] + background_rect.width/2
    y = position_on_scenario[1] + background_rect.height/2
    if vector:
        return pg.math.Vector2((x,y))
    else:
        return (x,y)

def image_to_screen(position_on_scenario, topleft):
    a = position_on_scenario[0]
    b = position_on_scenario[1]
    x = topleft[0]
    y = topleft[1]
    return (a+x, b+y)

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

def is_visible_area(position_on_screen):
    center = constants.PLAYER_POSITION_SCREEN
    visible_radius = constants.VISIBLE_RADIUS*constants.VISIBLE_RADIUS
    dx = position_on_screen[0]-center[0]
    dy = position_on_screen[1]-center[1]
    distance = dx*dx+dy*dy
    return distance < visible_radius

def to_int(vector):
    x = int(vector[0])
    y = int(vector[1])
    return (x,y)

def draw_rect_list(surface, rect_list, back_topleft):
    if rect_list:
        for rect in rect_list:
            center = image_to_screen(rect.center, back_topleft)
            topleft = image_to_screen(rect.topleft, back_topleft)
            topright = image_to_screen(rect.topright, back_topleft)
            bottomleft = image_to_screen(rect.bottomleft, back_topleft)
            bottomright = image_to_screen(rect.bottomright, back_topleft)

            if (bottomright[0] < 0 and bottomright[1] < 0) or (topleft[0] > 800 and topleft[1] > 600):
                pass
            else:
                pg.draw.line(surface, (255,0,0), topleft, topright)
                pg.draw.line(surface, (255,0,0), topleft, bottomleft)
                pg.draw.line(surface, (255,0,0), topright, bottomright)
                pg.draw.line(surface, (255,0,0), bottomleft, bottomright)

def draw_rect(rect, screen):
    pg.draw.line(screen, (255,0,0), rect.topleft, rect.topright, 2)
    pg.draw.line(screen, (255,0,0), rect.topleft, rect.bottomleft, 2)
    pg.draw.line(screen, (255,0,0), rect.topright, rect.bottomright, 2)
    pg.draw.line(screen, (255,0,0), rect.bottomleft, rect.bottomright, 2)
    pg.draw.line(screen, (0,255,0), rect.center, (400,300), 3)
    pg.draw.circle(screen, (0,255,0), to_int(rect.center),3, 2)

def transform_corners_to_rects(corner_list):
    rect_list = []
    for coordinates_list in corner_list:
        first_point = (10*coordinates_list[0][0], 10*coordinates_list[0][1])
        second_point = (10*coordinates_list[1][0], 10*coordinates_list[1][1])
        top = None
        left = None
        width = abs(first_point[0]-second_point[0])
        height = abs(first_point[1]-second_point[1])
        if second_point[0] > first_point[0] and second_point[1] > first_point[1]:
            top = first_point[1]
            left = first_point[0]
        if second_point[0] > first_point[0] and second_point[1] < first_point[1]:
            top = second_point[1]
            left = first_point[0]
        if second_point[0] < first_point[0] and second_point[1] > first_point[1]:
            top = first_point[1]
            left = second_point[0]
        if second_point[0] < first_point[0] and second_point[1] < first_point[1]:
            top = second_point[1]
            left = second_point[0]

        try:
            rect = pg.Rect(left, top, width, height)
            rect_list.append(rect)
        except:
            pass

    return rect_list

# for now, this function is exclusive for bot
# reason: bot_list is group of Bot, not Collider
def check_collision(actual_collider, object_group):
    collider_collisions_list = []
    for obj in object_group:
        if actual_collider.rect.colliderect(obj.collider.rect):
            if actual_collider.rect.center != obj.collider.rect.center:
                collider_collisions_list.append(obj)
    
    if len(collider_collisions_list)!=0:
        return collider_collisions_list
    else:
        return None

def move_on_collision(animated_collider, list_collisions, direction):
    x_move = direction[0]
    y_move = direction[1]

    for collider_wall in list_collisions:
        if x_move>=0 and y_move>=0:
            # bate na esquerda ou em cima
            deltax = collider_wall.rect.topleft[0]-animated_collider.rect.centerx
            deltay = collider_wall.rect.topleft[1]-animated_collider.rect.centery
            if deltax <= deltay:
                # bateu em cima
                animated_collider.rect.bottom = collider_wall.rect.top
            else:
                # bateu na esquerda
                animated_collider.rect.right = collider_wall.rect.left
        elif x_move>=0 and y_move<=0:
            # bate na esquerda ou embaixo
            deltax = collider_wall.rect.bottomleft[0]-animated_collider.rect.centerx
            deltay = -collider_wall.rect.bottomleft[1]+animated_collider.rect.centery
            if deltax <= deltay:
                animated_collider.rect.top = collider_wall.rect.bottom
            else:
                animated_collider.rect.right = collider_wall.rect.left
        elif x_move<=0 and y_move>=0:
            # bate na direita ou em cima
            deltax = -collider_wall.rect.topright[0]+animated_collider.rect.centerx
            deltay = collider_wall.rect.topright[1]-animated_collider.rect.centery
            if deltax <= deltay:
                animated_collider.rect.bottom = collider_wall.rect.top
            else:
                animated_collider.rect.left = collider_wall.rect.right
        elif x_move<=0 and y_move<=0:
            # bate na direita ou embaixo
            deltax = -collider_wall.rect.bottomright[0]+animated_collider.rect.centerx
            deltay = -collider_wall.rect.bottomright[1]+animated_collider.rect.centery
            if deltax <= deltay:
                animated_collider.rect.top = collider_wall.rect.bottom
            else:
                animated_collider.rect.left = collider_wall.rect.right
