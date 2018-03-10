import pygame
from pygame.locals import *
import sys, os, traceback
if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"

import PAdLib.occluder as occluder
import PAdLib.shadow as shadow

pygame.display.init()
pygame.font.init()

screen_size = [512,512]
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("Shadows Demo with PAdLib - Ian Mallett - 2013")
surface = pygame.display.set_mode(screen_size)

#The basic idea here is to draw the scene normally, and then multiply
#everything by another surface holding all the lighting information.

#So, for example, if the lighting surface is black, the scene will
#appear black.  If the lighting surface is white, the scene will
#appear its normal colors.  If the lighting surface is grey, the scene
#will appear its normal colors, but darkened.  In practice, the effect
#gives good results when the lighting surface is by default grey, but
#lighter grey or white in certain areas.  This makes the scene look
#dark in most places, but illuminated in others.

#The shadowing object returns a black and white mask and a location to
#draw it.  We could just blend this into the lighting surface, but one
#option below causes it to be first multiplied by a falloff surface.
#The mask becomes a greyscale intensity map.  It is then drawn into
#the lighting surface in the right place.  This adjusts the color of
#the lighting surface so as to be lighter grey or white in these
#places.

#The lighting surface is multiplied into the scene, completing the
#algorithm.

#Holds all the lighting information
surf_lighting = pygame.Surface(screen_size)

#Our shadowing object
shad = shadow.Shadow()

#load the background
surf_bg = pygame.image.load("bg.png").convert()

#Add the occluders.  Occluders are objects which block light.
#This code adds a single occluder for each black pixel.
occluders = []
#   Example 1
for y in range(surf_bg.get_height()):
    for x in range(surf_bg.get_height()):
        color = surf_bg.get_at((x,y))
        if color == (0,0,0,255):
            occluders.append(occluder.Occluder([[x*16,y*16],[x*16,y*16+16],[x*16+16,y*16+16],[x*16+16,y*16]]))
#   Example 2
##occluders.append(occluder.Occluder([[256,256],[256,300],[300,300]]))
#   Example 3
##occluders.append(occluder.Occluder([[256,260],[300,260],[256,256]]))
shad.set_occluders(occluders)
shad.set_radius(100.0)

#Scale the background to the screen's size, and convert it for speed
surf_bg = pygame.transform.scale(surf_bg,screen_size)
surf_bg.convert()

#Falloff multiplier
surf_falloff = pygame.image.load("light_falloff100.png").convert()

with_background = True
with_falloff = True
def get_input():
    global with_background, with_falloff
    mouse_position = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
            elif event.key == K_f:
                with_falloff = not with_falloff
            elif event.key == K_b:
                with_background = not with_background
    #Set the position of the light
    shad.set_light_position(mouse_position)
    return True

def draw():
    #======First compute the lighting information======
    
    #   Returns a greyscale surface of the shadows and the coordinates to draw it at.
    #   False tell it to not consider the occluders' interiors to be shadowed.  True
    #   means that the occluders' interiors are shadowed.  Note that if the light is
    #   within any occluder, everything is always shadowed.
    mask,draw_pos = shad.get_mask_and_position(False)

    #   Falloff (just multiplies the black and white mask by the falloff to make it
    #   look smoother).  Disabling "with_falloff" might make the algorithm more clear.
    if with_falloff:
        mask.blit(surf_falloff,(0,0),special_flags=BLEND_MULT)

    #   Ambient light
    surf_lighting.fill((50,50,50))
    #   Add the contribution from the shadowed light source
    surf_lighting.blit(mask,draw_pos,special_flags=BLEND_MAX)

    #======Now actually draw the scene======
    
    #   Draw the background xor clear the screen
    if with_background:
        surface.blit(surf_bg,(0,0))
    else:
        surface.fill((255,0,0))

    #======Now multiply the lighting information onto the scene======

    #   If you comment this out, you'll see the scene without any lighting.
    #   If you comment out just the special flags part, the lighting surface
    #   will overwrite the scene, and you'll see the lighting information.
    surface.blit(surf_lighting,(0,0),special_flags=BLEND_MULT)

    #======Post processing======

    #   Hack to outline the occluders.  Don't use this yourself.
    for occluder in occluders:
        pygame.draw.lines(surface,(255,255,255),True,occluder.points)

    #======Flip screen so that drawing is visible======
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
