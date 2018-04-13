import os
import sys
import pygame as pg

###############################################

def scenario_to_screen(position, rect):
    x = position[0] + rect.topleft[0]
    y = position[1] + rect.topleft[1]
    return (x,y)
def screen_to_scenario(position, rect):
    x = position[0] - rect.topleft[0]
    y = position[1] - rect.topleft[1]
    return (x,y)

class Main:
    def __init__(self):
        self.rect_list = []
        self.first_point = True
        self.second_point = False
    
    def on_init(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self._running = True

        self.size = self.width, self.height = 800, 600
        self._display_surf = pg.display.set_mode(self.size)
        self.screen = pg.display.get_surface()
        self.background = pg.image.load("Assets/Images/map_back-min.png").convert_alpha()
        self.rect = self.background.get_rect(topleft=(0,0))
        self.background = pg.transform.scale(self.background, ( int(self.rect.width/10), int(self.rect.height/10)))
        self.rect = self.background.get_rect(topleft=(0,0))

    def on_event(self, event_queue):
        for event in event_queue:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self._running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.first_point:
                    self.first_point = False
                    self.second_point = True
                    self.first_coordinate = screen_to_scenario(pg.mouse.get_pos(), self.rect)
                else:
                    self.second_point = False
                    self.second_coordinate = screen_to_scenario(pg.mouse.get_pos(), self.rect)
            if event.type == pg.MOUSEBUTTONUP:
                if not self.second_point and not self.first_point:
                    self.first_point = True
                    self.second_point = False
                    coordinates = [self.first_coordinate, self.second_coordinate]
                    self.rect_list.append(coordinates)
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.first_point = True
                self.second_point = False
            if event.type == pg.KEYDOWN and event.key == pg.K_d:
                self.rect.centerx = self.rect.centerx - 10 
            if event.type == pg.KEYDOWN and event.key == pg.K_s:
                self.rect.centery = self.rect.centery - 10
            if event.type == pg.KEYDOWN and event.key == pg.K_a:
                self.rect.centerx = self.rect.centerx + 10
            if event.type == pg.KEYDOWN and event.key == pg.K_w:
                self.rect.centery = self.rect.centery + 10
    def draw(self):
        self.screen.fill((255,255,255))
        self.screen.blit(self.background, self.rect)
        for points in self.rect_list:
            point1 = scenario_to_screen(points[0], self.rect)
            point2 = scenario_to_screen(points[1], self.rect)
            point3 = (point1[0], point2[1])
            point4 = (point2[0],point1[1])
            pg.draw.polygon(self.screen, (255,0,0), [point1, point3, point2, point4], 0)
        if self.second_point:
            point1 = scenario_to_screen(self.first_coordinate, self.rect)
            point2 = pg.mouse.get_pos()
            point3 = (point1[0], point2[1])
            point4 = (point2[0],point1[1])
            pg.draw.polygon(self.screen, (255,255,0), [point1, point3, point2, point4], 0)
        pg.display.update()

    def on_execute(self):
        self.on_init()

        while (self._running):
            self.on_event(pg.event.get())
            self.draw()
        print(self.rect_list)

if __name__ == "__main__":
    Main().on_execute()
