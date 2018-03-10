import pygame
from pygame.locals import *
import sys, os, traceback
if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"

import PAdLib as padlib

pygame.display.init()
pygame.font.init()

screen_size = [800,600]
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("Triangles Demo with PAdLib - Ian Mallett - 2013")
surface = pygame.display.set_mode(screen_size)

#Demonstrates some of the functionality of the draw module.  Uncomment some
#of the lines below--I recommend one at a time.  The first one is uncommented,
#and draws an interpolated triangle

texture = pygame.image.load("bg.png")

filter = False
clamp = True
def get_input():
    global mouse_position, filter, clamp
    mouse_position = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
            elif event.key == K_f:
                filter = not filter
            elif event.key == K_c:
                clamp = not clamp
    return True

def draw():
    #Clear
    surface.fill((100,100,100))

    #Draw an interpolated triangle.
    padlib.draw.trianglecolor( surface, (255,255,0),(255,0,0),(0,0,255), (10,20),(50,25),(60,100) )

    #Draw a triangle with a custom shader.  NumPy acceleration not demonstrated.
    def function(u,v,w):
        if u > v and u > w: return [255,0,0]
        if v > w and v > u: return [0,255,0]
        else:               return [0,0,255]
    #padlib.draw.trianglecustom( surface, (10,120),(50,125),(60,200), function,False )

    #Draw a textured triangle.
    #padlib.draw.triangletexture( surface, texture, (0.0,0.0),(1.0,0.0),(1.0,1.0), (170,50),(160,100),(200,90), filter,clamp )

    #Draw a textured quad, with one dynamically changing vertex
    vertex = list(mouse_position)
    tol = 20
    vertex[0] = max([min([vertex[0],290+tol]),290-tol])
    vertex[1] = max([min([vertex[1],160+tol]),160-tol])
    #padlib.draw.quadtexture( surface, texture, (0.0,0.0),(1.0,0.0),(1.0,1.0),(0.0,1.0), (170,150),(160,200),(200,250),vertex, filter,clamp )

    #Draw a larger texture just to show you an extremely magnified texture.  Can be slow, as the textured functions do not yet support NumPy acceleration.
    #padlib.draw.quadtexture( surface, texture, (0.0,0.0),(1.0,0.0),(1.0,1.0),(0.0,1.0), (190,150),(170,350),(370,350),(370,250), filter,clamp )

    #Flip
    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    while True:
        if not get_input(): break
        draw()
        clock.tick(60)
        #print(clock.get_fps())
    pygame.quit()
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()
