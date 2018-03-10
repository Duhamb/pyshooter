import pygame as pg

# this function return the position on screen based on other coordinates
# is needed because all orientation is made by scenario position and
# render functions use screen position
def scenario_to_screen(position_on_scenario, scenario_rect):
	return position_on_scenario + scenario_rect.center

# this function return the position on scenario based on other coordinates
# see comments of scenario_to_screen function
def screen_to_scenario(position_on_screen, scenario_rect):
	return position_on_screen - scenario_rect.center

# this function return the center of background image based on other coordinates
def background_center_position(position_on_screen, position_on_scenario):
	return position_on_screen - position_on_scenario

def scale_image_list(image_list, ratio):
	list_size = len(image_list)
	w,h = image_list[0].get_rect().size
	new_list = []
	for i in range(0,list_size):
		new_list.append(pg.transform.scale(image_list[i], (int(w/ratio), int(h/ratio))))
	return new_list

def scale_image(image, ratio):
	w,h = image.get_rect().size
	return pg.transform.scale(image, (int(w/ratio), int(h/ratio)))

def load_image_list(directory, extension, quantity):
	new_list = []
	for i in range(0,quantity):
		actual_file = directory + str(i) + extension
		new_list.append(pg.image.load(actual_file))
	return new_list

def increment(acc, increment, limit):
	acc += increment
	if acc > limit:
		acc = 0
	return acc