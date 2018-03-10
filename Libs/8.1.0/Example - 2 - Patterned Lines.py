import pygame
from pygame.locals import *
import sys, os, traceback
if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"

import PAdLib as padlib

pygame.display.init()
pygame.font.init()

screen_size = [800,600]
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("Dotted/Dashed Line Demo with PAdLib - Ian Mallett - 2013")
surface = pygame.display.set_mode(screen_size)

aa = True
blend = True
def get_input():
    global mouse_position, aa,blend
    keys_pressed = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()
    mouse_rel = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
            elif event.key == K_a:
                aa = not aa
            elif event.key == K_b:
                blend = not blend
    return True

def draw():
    surface.fill((100,100,100))

    #The line is broken down into sections, each of which has a certain
    #length in pixels.  Sections repeat down the length of the line.
    
    #To draw a patterned line, the line is broken into sections, and
    #each pixel in the section is colored according to the pattern.

    #To determine the patter, we create a callback function.  This
    #function takes a number between 0.0 and 1.0, representing a
    #location on a section (e.g., 0.0 is the beginning of a section and
    #1.0 is the end of a section).

    #The function outputs the color.  It should do a minimal amount of
    #work because it is called for every pixel drawn.  This can be a
    #lot, especially with the antialiased version
    
    def f(x):
        if   x < 1.0/3.0: return (255,255,255)
        elif x < 2.0/3.0: return (  0,  0,255)
        else:             return (  0,255,  0)

    #Draw the patterned line
    if not aa:
        padlib.draw.  linepattern(surface, mouse_position,(screen_size[0]/2,screen_size[1]/2), f, 20,0       )
    else:
        padlib.draw.aalinepattern(surface, mouse_position,(screen_size[0]/2,screen_size[1]/2), f, 20,0, blend)
    
    
    pygame.display.flip()

def main():
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    while True:
        if not get_input(): break
        draw()
        clock.tick(60)
    pygame.mouse.set_visible(True)
    pygame.quit()
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()
