#Imports
import pygame
from pygame.locals import *
import sys, os, traceback
#Center the screen
if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"

import PAdLib as padlib

#Initialize
pygame.display.init()
pygame.font.init()

#Set up a window
screen_size = [512,512]
#A blank icon
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
#This caption
pygame.display.set_caption("Rounded Rectangles Demo with PAdLib - Ian Mallett - 2013")
#Make the windowing surface!
surface = pygame.display.set_mode(screen_size)

def get_input():
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
    return True

def draw():
    surface.fill((50,0,0))

    #Similar semantics to pygame.draw.rrect(...).
    #surface, color, rect, radius, width=0
    padlib.draw.rrect(surface, (  0,255,  0), ( 10, 10,200,200), 31   )
    padlib.draw.rrect(surface, (255,  0,255), (230, 80,250,300), 18, 2)
    padlib.draw.rrect(surface, (  0,  0,255), ( 20,220,200,200), 11, 4)
    padlib.draw.rrect(surface, (255,  0,  0), ( 40,430,350, 64), 18, 3)
    
    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    while True:
        if not get_input(): break
        draw()
        clock.tick(60)
    pygame.quit()
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()
