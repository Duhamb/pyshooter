import os
import sys
import pygame as pg

class Player():
    def __init__(self, image, location):
        self.image = pg.transform.rotate(image, 90)
        self.original_image = image
        self.rect = self.image.get_rect(center=location)
        self.position = pg.math.Vector2(location)
        self.position = pg.math.Vector2(location)
        self.light = pg.image.load("circle.png")

    def draw(self, surface):
        self.update()
        surface.blit(self.image, self.rect)

    def update(self):
        self.rotate()
        self.rect.center = self.position

    def rotate(self):
        _, angle = (pg.mouse.get_pos()-self.position).as_polar()
        self.image = pg.transform.rotozoom(self.original_image, -angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

class Background():
    def __init__(self, back, front, location):
        self.front = front
        self.back = back
        self.center_image_position = pg.math.Vector2((0,0))
        self.rect = self.front.get_rect(center=location)
        self.back_array=pg.surfarray.array2d(self.back)
        # self.steps_sound = pg.mixer.Sound("stepstone_1.wav")
        # self.steps_sound.set_volume(10)

    def draw(self, surface):
        surface.blit(self.front, self.rect)

    def move(self, vector):
        # self.steps_sound.play()
        dx = vector[0]
        dy = vector[1]
        self.rect = self.front.get_rect(center = (self.rect.center[0] + 10*dx, self.rect.center[1] + 10*dy))
        self.center_image_position = pg.math.Vector2(self.rect.center)

###############################################

class Main:
    def __init__(self):
        self._running = True
        self.size = self.width, self.height = 800, 600
        self.fps = 60
        self.pressionou_w = False
        self.pressionou_a = False
        self.pressionou_s = False
        self.pressionou_d = False


    def on_init(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pg.init()
        self._running = True
        self.clock = pg.time.Clock()
        pg.mouse.set_visible(0)
        # resolution = (int(pg.display.Info().current_w), int(pg.display.Info().current_h))
        
        self._display_surf = pg.display.set_mode(self.size, pg.FULLSCREEN) 
        self.screen = pg.display.get_surface() # repetido?
        
        self.PLAYER_POSITION = (self.width/2, self.height/2)
        self.PLAY_IMAGE = pg.image.load("player3.png")
        self.PLAY_IMAGE = pg.transform.scale(self.PLAY_IMAGE, (75,75))
        self.BACK_IMAGE = pg.image.load("city1_back.png").convert_alpha()
        self.FRONT_IMAGE = pg.image.load("city1.jpg").convert_alpha()
        self.CROSS_IMAGE = pg.image.load("cross.png").convert_alpha()
        self.CROSS_IMAGE = pg.transform.scale(self.CROSS_IMAGE, (15,15))
        
        self.player = Player(self.PLAY_IMAGE, self.PLAYER_POSITION)
        self.back = Background(self.BACK_IMAGE, self.FRONT_IMAGE, self.PLAYER_POSITION)

    def on_event(self, event):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            self._running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.pressionou_w = True
            if event.key == pg.K_a:
                self.pressionou_a = True
            if event.key == pg.K_s:
                self.pressionou_s = True
            if event.key == pg.K_d:
                self.pressionou_d = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_w:
                self.pressionou_w = False
            if event.key == pg.K_a:
                self.pressionou_a = False
            if event.key == pg.K_s:
                self.pressionou_s = False
            if event.key == pg.K_d:
                self.pressionou_d = False
        
    def display_fps(self):
        pg.display.set_caption("{} - FPS: {:.2f}".format("PyShooter", self.clock.get_fps()))

    def on_loop(self):
        if self.pressionou_w:
            self.actual_position = self.player.position
            self.mouse_position = pg.mouse.get_pos()
            self.direction_of_move = -(self.mouse_position - self.actual_position)
            self.direction_of_move /= self.direction_of_move.length()
            self.back.move(self.direction_of_move)

        if self.pressionou_s:
            self.actual_position = self.player.position
            self.mouse_position = pg.mouse.get_pos()
            self.direction_of_move = +(self.mouse_position - self.actual_position)
            self.direction_of_move /= self.direction_of_move.length()
            self.back.move(self.direction_of_move)

        if self.pressionou_a:
            self.actual_position = self.player.position
            self.mouse_position = pg.mouse.get_pos()
            self.direction_of_move = +(self.mouse_position - self.actual_position).rotate(90)
            self.direction_of_move /= self.direction_of_move.length()
            self.back.move(self.direction_of_move)

        if self.pressionou_d:
            self.actual_position = self.player.position
            self.mouse_position = pg.mouse.get_pos()
            self.direction_of_move = -(self.mouse_position - self.actual_position).rotate(90)
            self.direction_of_move /= self.direction_of_move.length()
            self.back.move(self.direction_of_move)
        self.clock.tick(self.fps)

    def on_cleanup(self):
        pg.quit()
        sys.exit()

    def on_render(self):
        self.screen.fill((0,0,0))
        self.back.draw(self.screen)
        self.player.draw(self.screen)
        self.screen.blit(self.CROSS_IMAGE, pg.mouse.get_pos())
        # filter = pg.surface.Surface(self.size)
        # filter.fill(pg.color.Color('Grey'))
        # filter.blit(self.player.light, self.player.rect)
        # self.screen.blit(filter, (0, 0), special_flags=pg.BLEND_RGBA_SUB)
        self.display_fps()
        pg.display.update()

    def on_execute(self):
        self.on_init()
        while (self._running):
            for event in pg.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    Main().on_execute()
