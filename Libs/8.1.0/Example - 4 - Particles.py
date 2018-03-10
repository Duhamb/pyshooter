import pygame
from pygame.locals import *
import sys, os, traceback
if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"

import PAdLib.occluder as occluder
import PAdLib.particles as particles

pygame.display.init()
pygame.font.init()

screen_size = [800,600]
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("Particles Demo with PAdLib - Ian Mallett - 2013")
surface = pygame.display.set_mode(screen_size)

#Make a particle emitter
emitter1 = particles.Emitter()
#   number of new particles added each second, on average
emitter1.set_density(100)
#   New particles will travel in the direction -135 degrees, distributed around
#   that by +/- 2.5 degrees.  Note PyGame's inverted y axis.
emitter1.set_angle(-135.0,5.0)
#   The range of initial speeds the particles will have, in pixels per second.
#   Each new particle's initial speed is chosen randomly from this range.
emitter1.set_speed([150.0,350.0])
#   New particles will last for a given amount of time, chosen randomly from
#   1.0 seconds to 2.0 seconds.
emitter1.set_life([1.0,2.0])
#   This specifies a list of colors each particle will have over its lifetime.
#   Particles' colors are defined continuously; smoothly blending between values
#   in this list as they get older.
emitter1.set_colors([(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(0,0,0)])

#Make another emitter
emitter2 = particles.Emitter()
emitter2.set_density(200)
emitter2.set_angle(45.0,2.0)
emitter2.set_speed([800.0,1200.0])
emitter2.set_life([1.0,2.0])
emitter2.set_colors([(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(0,0,0)])

#Make an occluder
points1 = [ [screen_size[0]//2-50,screen_size[1]-50], [screen_size[0]//2+50,screen_size[1]-50], [screen_size[0]//2-10,screen_size[1]-150] ]
occluder1 = occluder.Occluder(points1)
#   Particles bouncing off the occluder will do so with this elasticity.
occluder1.set_bounce(0.5)

#Make the particle system
particle_system = particles.ParticleSystem()
#   Set the global acceleration of all particles
particle_system.set_particle_acceleration([0.0,500.0])
#   Set the list of occluders
particle_system.set_particle_occluders([occluder1])
#   Add both emitters to the system
particle_system.add_emitter(emitter1,"emitter1")
particle_system.add_emitter(emitter2,"emitter2")

def get_input():
    mouse_position = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
    #Change the locations of the emitters to be two points near the mouse.
    emitter1.set_position([mouse_position[0]-10,mouse_position[1]-20])
    emitter2.set_position([mouse_position[0]+10,mouse_position[1]   ])
    return True

def update(dt):
    #Update the particle system.
    particle_system.update(dt)

def draw():
    surface.fill((0,0,0))

    #Draw the particle system to "surface".
    particle_system.draw(surface)
    
    #Draw the occluder
    pygame.draw.aalines(surface,(255,255,255),True,points1)

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
