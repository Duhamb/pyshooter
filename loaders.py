import pygame
import os

def load_image(name, colorkey=None):
	fullname = os.path.join('data', name)
	image = pygame.image.load(fullname)
	image = image.convert_alpha()
	return image, image.get_rect()

def load_sound(name):
	fullname = os.path.join('data', name)
	sound = pygame.mixer.Sound(fullname)
	return sound