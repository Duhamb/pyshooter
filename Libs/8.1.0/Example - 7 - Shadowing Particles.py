import pygame
from pygame.locals import *
import sys, os, traceback
if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"

import PAdLib.occluder as occluder
import PAdLib.particles as particles
import PAdLib.shadow as shadow

pygame.display.init()
pygame.font.init()

screen_size = [512,512]
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("Shadows/Particles Demo with PAdLib - Ian Mallett - 2013")
surface = pygame.display.set_mode(screen_size)

surf_lighting = pygame.Surface(screen_size)

shad = shadow.Shadow()
shad.set_radius(100.0)
shad.set_light_position([screen_size[0]/2,screen_size[1]/2])

surf_falloff = pygame.image.load("light_falloff100.png").convert()

emitter = particles.Emitter()
emitter.set_density(200)
emitter.set_angle(90.0,360.0)
emitter.set_speed([50.0,50.0])
emitter.set_life([1.0,1.0])
emitter.set_colors([(255,0,0),(255,255,0),(255,128,0),(0,0,0)])

particle_system = particles.ParticleSystem()
particle_system.add_emitter(emitter)

def get_input():
    mouse_position = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
    emitter.set_position(mouse_position)
    return True

def update(dt):
    #Update the particle system.
    particle_system.update(dt)
def draw():
    #Lighting pass
    light_occluders = []
    for particle in particle_system.particles:
        x,y = particle.position
        light_occluders.append(
            occluder.Occluder([[x,y],[x,y+1],[x+1,y+1],[x+1,y]])
        )
    shad.set_occluders(light_occluders)
    
    mask,draw_pos = shad.get_mask_and_position(False)
    mask.blit(surf_falloff,(0,0),special_flags=BLEND_MULT)

    surf_lighting.fill((50,50,50))
    surf_lighting.blit(mask,draw_pos,special_flags=BLEND_MAX)

    #Scene pass
    surface.fill((128,128,128))
    particle_system.draw(surface)

    #Composite pass
    surface.blit(surf_lighting,(0,0),special_flags=BLEND_MULT)

    #Redraw the particle system.  In this case we don't want it shadowed
    particle_system.draw(surface)
    
    #Flip
    pygame.display.flip()

def main():
    target_fps = 60
    clock = pygame.time.Clock()
    while True:
        if not get_input(): break
        update(1.0/float(target_fps))
        draw()
        clock.tick(target_fps)
    pygame.quit()
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()
