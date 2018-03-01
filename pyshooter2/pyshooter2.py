import pygame, sys, os, time, random, math
from pygame.locals import *

pygame.init()

def loadImage(filename):
	return pygame.image.load(os.path.join(filename))
	
player_surface = loadImage("player2.png")

class Player:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y
		self.xv = 0
		self.yv = 0
		self.face_vector = (1 , 0) 

	def setPosition(self, x = 0, y = 0):
		self.x = x
		self.y = y

	def setSurface(self, surf):
		self.surface = surf

	def draw(self, screen):
		screen.blit(self.surface, (self.x, self.y))
	
p1 = Player()
players = [p1]

width = 760
height = 760
ballsize = 10
paddlespeed = ballsize
ballspeed = paddlespeed/2
clock = pygame.time.Clock()
	
def startgame():		
	global p1
	p1.setPosition(screen.get_width()/2, screen.get_height()/2)
	# random.seed()
	# r1 = random.randint(0, 1)
	# r2 = random.randint(0, 1)


resolution = (int(pygame.display.Info().current_w), int(pygame.display.Info().current_h))
	
screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
pygame.display.set_caption('Pyshooter')
pygame.mouse.set_visible(1)

pressionou_w = False
pressionou_a = False
pressionou_s = False
pressionou_d = False
	
startgame()

for player in [p1]:
	player.setSurface(player_surface)

def readinput(events):
	global p1
	global pressionou_w
	global pressionou_a
	global pressionou_s
	global pressionou_d

	(mouse_pos_x, mouse_pos_y) = pygame.mouse.get_pos()
	for event in events:
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
			sys.exit()
		if event.type == MOUSEMOTION:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			vision_vector = (mouse_x - p1.x, mouse_y - p1.y)
			# angle = math.acos(vision_vector - p1.face_vector)


		if event.type == KEYDOWN:
			if event.key == K_s:
				pressionou_s = True
			if event.key == K_w:
				pressionou_w = True
			if event.key == K_d:
				pressionou_d = True
			if event.key == K_a:
				pressionou_a = True
				
		if event.type == KEYUP:

			if event.key == K_s:
				pressionou_s = False
			if event.key == K_w:
				pressionou_w = False
			if event.key == K_d:
				pressionou_d = False
			if event.key == K_a:
				pressionou_a = False

	dx = mouse_pos_x - p1.x
	dy = mouse_pos_y - p1.y
	norm = math.sqrt(dx**2 + dy**2)

	if pressionou_w:
		p1.xv = dx/norm*paddlespeed
		p1.yv = dy/norm*paddlespeed

	if pressionou_s:
		p1.xv = -dx/norm*paddlespeed
		p1.yv = -dy/norm*paddlespeed

	if pressionou_d:
		p1.xv = -dy/norm*paddlespeed
		p1.yv = dx/norm*paddlespeed

	if pressionou_a:
		p1.xv = dy/norm*paddlespeed
		p1.yv = -dx/norm*paddlespeed
	
	if not pressionou_w and not pressionou_d and not pressionou_a and not pressionou_s:
		p1.xv = 0
		p1.yv = 0
		
while (True):
	clock.tick(20)
	
	screen.fill((0, 56, 0))
		
	readinput(pygame.event.get())
	
	for player in [p1]:
		player.x += player.xv
		player.y += player.yv
		player.draw(screen)
	
	pygame.display.flip()

