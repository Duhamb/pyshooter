# this file has constant values and auxiliar functions used in whole game

import pygame as pg


######################   FUNCTIONS    ##################################

# this function return the position on screen based on other coordinates
# is needed because all orientation is made by scenario position and
# render functions use screen position
def scenario_to_screen(position_on_scenario, scenario_rect, vector2=True):
    x = position_on_scenario[0]+scenario_rect.center[0]
    y = position_on_scenario[1]+scenario_rect.center[1]
    if vector2:
        return pg.math.Vector2((x,y))
    else:
        return (x,y)

def scenario_to_screen2(position_on_scenario, topleft):
    a = position_on_scenario[0]
    b = position_on_scenario[1]
    x = topleft[0]
    y = topleft[1]
    return (a+x, b+y)

# this function return the position on scenario based on other coordinates
# see comments of scenario_to_screen function
def screen_to_scenario(position_on_screen, scenario_rect, vector2=True):
    x = position_on_screen[0]-scenario_rect.center[0]
    y = position_on_screen[1]-scenario_rect.center[1]
    if vector2:
        return pg.math.Vector2((x,y))
    else:
        return (x,y)

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

def tuple_of_ints(tuple_of_float):
    a = int(tuple_of_float[0])
    b = int(tuple_of_float[1])
    return (a,b)

def get_character_center_position(rect, offset_vector, angle_rotation):
    delta_position = pg.math.Vector2(rect.center) - pg.math.Vector2(rect.topleft)
    offset = (-offset_vector).rotate(angle_rotation)
    actual_position = delta_position + offset
    return  tuple_of_ints(actual_position)

def remove_parallel_component(reference_vector, original_vector):
    perpendicular_vector = reference_vector.rotate(90)
    new_direction = perpendicular_vector.dot(original_vector) * perpendicular_vector
    try:
        new_direction = new_direction.normalize()
    except:
        new_direction = pg.math.Vector2((0,0))
    return new_direction

def convert_vector_to_tuple(vector):
    return (vector[0], vector[1])

def draw_rect_list(surface, rect_list, background_rect):
    if rect_list:
        for rect in rect_list:
            center = scenario_to_screen2(rect.center, background_rect)
            topleft = scenario_to_screen2(rect.topleft, background_rect)
            topright = scenario_to_screen2(rect.topright, background_rect)
            bottomleft = scenario_to_screen2(rect.bottomleft, background_rect)
            bottomright = scenario_to_screen2(rect.bottomright, background_rect)

            if (bottomright[0] < 0 and bottomright[1] < 0) or (topleft[0] > 800 and topleft[1] > 600):
                pass
            else:
                pg.draw.line(surface, (255,0,0), topleft, topright)
                pg.draw.line(surface, (255,0,0), topleft, bottomleft)
                pg.draw.line(surface, (255,0,0), topright, bottomright)
                pg.draw.line(surface, (255,0,0), bottomleft, bottomright)


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

BACKGROUND_RECTS = [[(104, 97), (147, 165)], [(303, 290), (188, 116)], 
[(195, 227), (177, 174)], [(139, 223), (100, 185)], [(288, 218), (290, 230)], 
[(290, 230), (290, 230)], [(290, 230), (290, 230)], [(290, 230), (290, 230)], 
[(121, 245), (159, 298)], [(408, 111), (467, 136)], [(406, 145), (480, 180)], 
[(572, 191), (496, 135)], [(590, 276), (590, 278)], [(590, 278), (590, 278)], 
[(590, 278), (590, 278)], [(590, 278), (590, 278)], [(471, 229), (526, 299)], 
[(460, 237), (537, 284)], [(433, 245), (406, 209)], [(407, 243), (397, 223)], 
[(453, 295), (422, 260)], [(411, 259), (424, 289)], [(397, 281), (422, 290)], 
[(499, 161), (465, 147)], [(465, 174), (444, 188)], [(529, 138), (500, 120)], 
[(549, 106), (573, 151)], [(688, 157), (740, 265)], [(685, 268), (708, 241)], 
[(792, 284), (751, 244)], [(778, 251), (762, 238)], [(832, 193), (858, 234)], 
[(869, 225), (834, 193)], [(713, 367), (716, 368)], [(716, 368), (716, 368)], 
[(716, 368), (716, 368)], [(304, 712), (182, 675)], [(135, 730), (109, 700)], 
[(138, 777), (108, 746)], [(178, 878), (105, 806)], [(183, 819), (235, 871)], 
[(302, 881), (267, 844)], [(303, 826), (267, 793)], [(309, 720), (276, 785)], 
[(511, 882), (391, 830)], [(506, 833), (490, 821)], [(396, 755), (433, 823)], 
[(428, 776), (443, 824)], [(442, 788), (455, 854)], [(451, 838), (396, 811)], 
[(442, 744), (395, 680)], [(591, 681), (411, 718)], [(466, 707), (463, 711)], 
[(461, 713), (461, 713)], [(460, 714), (446, 706)], [(446, 706), (446, 706)], 
[(446, 706), (446, 706)], [(446, 706), (446, 706)], [(285, 546), (284, 545)], 
[(139, 506), (100, 389)], [(223, 421), (128, 389)], [(303, 392), (262, 587)], 
[(252, 508), (270, 587)], [(240, 390), (270, 438)], [(387, 432), (386, 432)], 
[(386, 432), (384, 431)], [(384, 431), (384, 431)], [(157, 587), (116, 528)], 
[(208, 551), (235, 589)], [(195, 556), (168, 588)], [(141, 707), (172, 675)], 
[(261, 853), (234, 873)], [(255, 885), (230, 864)], [(531, 826), (593, 870)], 
[(558, 788), (592, 818)], [(554, 747), (593, 777)], [(592, 732), (511, 711)], 
[(719, 390), (686, 422)], [(721, 432), (684, 463)], [(712, 475), (684, 500)], 
[(710, 508), (684, 535)], [(686, 557), (805, 588)], [(814, 566), (846, 590)], 
[(883, 512), (851, 585)], [(883, 497), (845, 403)], [(833, 394), (870, 430)], 
[(823, 445), (768, 393)], [(770, 411), (735, 387)], [(787, 127), (755, 115)], 
[(787, 158), (757, 144)], [(787, 185), (754, 174)], [(786, 223), (757, 213)], 
[(810, 280), (801, 247)], [(828, 164), (800, 143)], [(827, 193), (804, 175)], 
[(828, 224), (798, 205)], [(834, 252), (873, 277)], [(840, 275), (864, 284)], 
[(863, 258), (840, 246)], [(864, 178), (837, 147)], [(838, 153), (819, 193)], 
[(869, 171), (851, 157)], [(850, 149), (837, 142)], [(928, 271), (928, 271)], 
[(928, 271), (928, 271)], [(929, 272), (930, 272)], [(437, 474), (431, 428)], 
[(431, 428), (478, 436)], [(431, 500), (438, 547)], [(432, 542), (478, 548)], 
[(502, 542), (551, 547)], [(545, 501), (549, 548)], [(549, 475), (542, 430)], 
[(504, 427), (550, 435)], [(478, 479), (503, 501)], [(406, 402), (422, 416)], 
[(447, 407), (462, 419)], [(520, 407), (532, 416)], [(562, 407), (577, 419)], 
[(565, 447), (575, 457)], [(561, 523), (573, 533)], [(563, 562), (575, 575)], 
[(523, 562), (534, 574)], [(449, 565), (461, 575)], [(409, 564), (423, 573)], 
[(408, 527), (420, 536)], [(408, 445), (421, 458)], [(695, 495), (693, 497)], 
[(692, 497), (690, 497)], [(689, 497), (687, 497)], [(984, 977), (980, 1)], 
[(980, 1), (1, 7)], [(5, 1), (1, 975)], [(1, 972), (983, 976)], [(729, 731), (818, 806)], 
[(799, 802), (754, 817)], [(799, 744), (833, 792)], [(811, 749), (742, 719)], [(733, 746), (718, 790)]]