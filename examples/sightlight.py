''' 
    SIGHT & LIGHT by ncase (https://github.com/ncase/sight-and-light)
    Ported to Python/PyGame by Marcus Møller (https://github.com/marcusmoller)
'''

import pygame
import pygame.gfxdraw
import math

class SightAndLight():
    def __init__(self):
        # initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("SIGHT & LIGHT Demo - Python/PyGame")

        # mouse position
        self.mouse_pos = (0, 0)

        # general
        self.fps_clock = pygame.time.Clock()
        self.running = True
        self.update_shadows = True # only call update on mouse movement

        # segments
        self.segments = [
                # Border
                {"a":{"x":0,"y":0}, "b":{"x":640,"y":0}},
                {"a":{"x":640,"y":0}, "b":{"x":640,"y":360}},
                {"a":{"x":640,"y":360}, "b":{"x":0,"y":360}},
                {"a":{"x":0,"y":360}, "b":{"x":0,"y":0}},

                # Polygon #1
                {"a":{"x":100,"y":150}, "b":{"x":120,"y":50}},
                {"a":{"x":120,"y":50}, "b":{"x":200,"y":80}},
                {"a":{"x":200,"y":80}, "b":{"x":140,"y":210}},
                {"a":{"x":140,"y":210}, "b":{"x":100,"y":150}},

                # Polygon #2
                {"a":{"x":100,"y":200}, "b":{"x":120,"y":250}},
                {"a":{"x":120,"y":250}, "b":{"x":60,"y":300}},
                {"a":{"x":60,"y":300}, "b":{"x":100,"y":200}},

                # Polygon #3
                {"a":{"x":200,"y":260}, "b":{"x":220,"y":150}},
                {"a":{"x":220,"y":150}, "b":{"x":300,"y":200}},
                {"a":{"x":300,"y":200}, "b":{"x":350,"y":320}},
                {"a":{"x":350,"y":320}, "b":{"x":200,"y":260}},

                # Polygon #4
                {"a":{"x":340,"y":60}, "b":{"x":360,"y":40}},
                {"a":{"x":360,"y":40}, "b":{"x":370,"y":70}},
                {"a":{"x":370,"y":70}, "b":{"x":340,"y":60}},

                # Polygon #5
                {"a":{"x":450,"y":190}, "b":{"x":560,"y":170}},
                {"a":{"x":560,"y":170}, "b":{"x":540,"y":270}},
                {"a":{"x":540,"y":270}, "b":{"x":430,"y":290}},
                {"a":{"x":430,"y":290}, "b":{"x":450,"y":190}},

                # Polygon #6
                {"a":{"x":400,"y":95}, "b":{"x":580,"y":50}},
                {"a":{"x":580,"y":50}, "b":{"x":480,"y":150}},
                {"a":{"x":480,"y":150}, "b":{"x":400,"y":95}}
        ]

        # Intersects
        self.intersects = []

        # Points
        self.points = []

    def run(self):
        while self.running:
            self.main_loop()

    def main_loop(self):
        self.handle_input()
        if self.update_shadows:
            self.update()
            self.update_shadows = False
        
        self.render_frame()


    def update(self):
        # Clear old points
        self.points = []

        # Get all unique points
        for segment in self.segments:
            self.points.append((segment['a'], segment['b']))

        unique_points = []
        for point in self.points:
            if point not in unique_points:
                unique_points.append(point)

        # Get all angles
        unique_angles = []
        for point in unique_points:
            angle = math.atan2(point[0]["y"]-self.mouse_pos[1], point[0]["x"]-self.mouse_pos[0])
            point[0]["angle"] = angle
            unique_angles.append(angle-0.00001)
            unique_angles.append(angle)
            unique_angles.append(angle+0.00001)

        # RAYS IN ALL DIRECTIONS
        self.intersects = []
        for angle in unique_angles:
            # Calculate dx & dy from angle
            dx = math.cos(angle)
            dy = math.sin(angle)

            # Ray from center of screen to mouse
            ray = {
                    "a": {"x":self.mouse_pos[0], "y": self.mouse_pos[1]},
                    "b": {"x": self.mouse_pos[0]+dx, "y": self.mouse_pos[1]+dy}
            }

            # Find CLOSEST intersection
            closest_intersect = None
            for segment in self.segments:
                intersect = self.get_intersection(ray, segment)
                if not intersect: continue
                if not closest_intersect or intersect["param"] < closest_intersect["param"]:
                    closest_intersect = intersect

            # Intersect angle
            if not closest_intersect: continue
            closest_intersect["angle"] = angle

            # Add to list of intersects
            self.intersects.append(closest_intersect)

        # Sort intersects by angle
        self.intersects = sorted(self.intersects, key=lambda k: k['angle'])

    def render_frame(self):
        self.screen.fill((255, 255, 255))

        # draw segments
        for segment in self.segments:
            pygame.draw.aaline(self.screen, (153, 153, 153), (segment['a']['x'], segment['a']['y']), (segment['b']['x'], segment['b']['y']))

        self.draw_polygon(self.intersects, (221, 56, 56))

        # draw debug lines
        for intersect in self.intersects:
            pygame.draw.aaline(self.screen, (255, 85, 85), self.mouse_pos, (intersect['x'], intersect['y']))

        # limit fps
        self.fps_clock.tick(60)

        # update screen
        pygame.display.update()

    def handle_input(self):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                print("quit")
                break

            # KEYBOARD
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.running = False

            # MOUSE
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                self.update_shadows = True

    def get_intersection(self, ray, segment):
        ''' Find intersection of RAY & SEGMENT '''
        # RAY in parametric: Point + Direction*T1
        r_px = ray['a']['x']
        r_py = ray['a']['y']
        r_dx = ray['b']['x'] - ray['a']['x']
        r_dy = ray['b']['y'] - ray['a']['y']

        # SEGMENT in parametric: Point + Direction*T2
        s_px = segment['a']['x']
        s_py = segment['a']['y']
        s_dx = segment['b']['x'] - segment['a']['x']
        s_dy = segment['b']['y'] - segment['a']['y']

        # Are they parallel? If so, no intersect
        r_mag = math.sqrt(r_dx*r_dx+r_dy*r_dy)
        s_mag = math.sqrt(s_dx*s_dx+s_dy*s_dy)
        if r_dx/r_mag == s_dx/s_mag and r_dy/r_mag == s_dy/s_mag:
            return None

        # SOLVE FOR T1 & T2
        # r_px+r_dx*T1 = s_px+s_dx*T2 && r_py+r_dy*T1 = s_py+s_dy*T2
        # ==> T1 = (s_px+s_dx*T2-r_px)/r_dx = (s_py+s_dy*T2-r_py)/r_dy
        # ==> s_px*r_dy + s_dx*T2*r_dy - r_px*r_dy = s_py*r_dx + s_dy*T2*r_dx - r_py*r_dx
        # ==> T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx)

        # todo: fix zerodivision error handling
        try:
            T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx)
        except ZeroDivisionError:
            T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx-0.01)

        try:
            T1 = (s_px+s_dx*T2-r_px)/r_dx
        except ZeroDivisionError:
            T1 = (s_px+s_dx*T2-r_px)/(r_dx-0.01)

        # Must be within parametic whatevers for RAY/SEGMENT
        if T1 < 0: return None
        if T2 < 0 or T2>1: return None

        # Return the POINT OF INTERSECTION
        return {
                "x": r_px+r_dx*T1,
                "y": r_py+r_dy*T1,
                "param": T1
        }

    def draw_polygon(self, polygon, color):
        # collect coordinates for a giant polygon
        points = []
        for intersect in polygon:
            points.append((intersect['x'], intersect['y']))
        
        # draw as a giant polygon
        pygame.gfxdraw.aapolygon(self.screen, points, color)
        pygame.gfxdraw.filled_polygon(self.screen, points, color)

if __name__ == "__main__":
    demo = SightAndLight()
demo.run()