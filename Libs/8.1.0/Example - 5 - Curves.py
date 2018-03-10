import pygame
from pygame.locals import *
import sys, os, traceback
if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"

import PAdLib as padlib

pygame.display.init()
pygame.font.init()

screen_size = [512,512]
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("Splines/Curves Demo with PAdLib - Ian Mallett - 2013")
surface = pygame.display.set_mode(screen_size)

pygame.key.set_repeat(400,25)

control_points = []
deltas = [
    [-100, 100],
    [- 80,  40],
    [- 40,   0],
    [   0,- 20],
    [  40,   0],
    [  80,  40],
    [ 100, 100]
]
for delta in deltas:
    control_points.append([delta[0]+screen_size[0]/2,delta[1]+screen_size[1]/2])

t=b=c=0.0
dragging = None
closed = False
aa = True
blend = True
spline_bezier = 1
width = 1
def get_input():
    global dragging, t,b,c, closed, aa, spline_bezier, width, blend
    keys_pressed = pygame.key.get_pressed()
    mouse_position = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
            elif event.key == K_UP:
                if keys_pressed[K_t]: t += 0.1; print("t = "+str(round(t,1)))
                if keys_pressed[K_b]: b += 0.1; print("b = "+str(round(b,1)))
                if keys_pressed[K_c]: c += 0.1; print("c = "+str(round(c,1)))
                if keys_pressed[K_w] and width < 10: width += 1
            elif event.key == K_DOWN:
                if keys_pressed[K_t]: t -= 0.1; print("t = "+str(round(t,1)))
                if keys_pressed[K_b]: b -= 0.1; print("b = "+str(round(b,1)))
                if keys_pressed[K_c]: c -= 0.1; print("c = "+str(round(c,1)))
                if keys_pressed[K_w] and width >  1: width -= 1
            elif event.key == K_b: #pixel blending for aa
                blend = not blend
            elif event.key == K_r: #reset spline
                t = b = c = 0.0
            elif event.key == K_RETURN: #toggle spline closed
                closed = not closed
            elif event.key == K_a: #toggle antialiasing
                aa = not aa
            elif event.key == K_d: #change demo
                spline_bezier = 3 - spline_bezier
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                i = 0
                for control_point in control_points:
                    if abs(mouse_position[0]-control_point[0]) < 4 and \
                       abs(mouse_position[1]-control_point[1]) < 4:
                        dragging = i
                        break
                    i += 1
        elif event.type == MOUSEBUTTONUP:
            dragging = None
    if dragging != None:
        control_points[dragging][0] = mouse_position[0]
        control_points[dragging][1] = mouse_position[1]
    return True

def draw():
    global control_points
    surface.fill((32,32,32))

    if spline_bezier == 1:
        #"t" affects the tangents
        #"b" is the bias
        #"c" explands and contracts
        #The 10 is the number of subdivisions between each point
        if not aa:
            padlib.draw.  spline(surface, (255,0,0), closed, control_points,       100, t,b,c, width)
        else:
            padlib.draw.aaspline(surface, (255,0,0), closed, control_points,       100, t,b,c, blend)
        for control_point in control_points:
            pygame.draw.circle(surface,(0,0,255),list(map(lambda x:int(x+0.5),control_point)),3)
    else:
        num = 4 #Use fewer control points for the Bézier curve demo, because it's more intuitive.
                #Set to any 2 <= number <= len(control_points) (the latter being, by default, 7)
        pygame.draw.aalines(surface,(64,64,64),False,control_points[:num],True)
        if not aa:
            padlib.draw.  bezier(surface, (255,0,0),         control_points[:num], 100,        width)
        else:
            padlib.draw.aabezier(surface, (255,0,0),         control_points[:num], 100,        blend)
        for control_point in control_points[:num]:
            pygame.draw.circle(surface,(0,0,255),list(map(lambda x:int(x+0.5),control_point)),3)
    
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
