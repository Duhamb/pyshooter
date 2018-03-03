import os
import sys
import pygame as pg

class Player():
    def __init__(self, image, location, speed):
        self.speed = speed
        self.image = pg.transform.rotate(image, 90)
        self.original_image = image
        self.rect = self.image.get_rect(center=location)
        self.position = pg.math.Vector2(location)
        self.velocity = pg.math.Vector2(0, 0)
        self.mask = pg.mask.from_surface(self.image)

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
    def __init__(self, back, front, location, speed):
        self.front = front
        self.back = back
        self.center_image_position = pg.math.Vector2(location)
        self.rect = self.front.get_rect(center=(-100,+50))
        self.mask = pg.mask.from_surface(self.back)

    def draw(self, surface):
        surface.blit(self.front, self.rect.center)
        surface.blit(self.back, self.rect.center)
        # olist = self.mask.outline()
        # pg.draw.polygon(surface,(200,150,150),olist,0)
        # pg.draw.lines(surface,(200,150,150),1,olist)

    def move(self, vector, player_mask, player_position):
        offset = ( int(player_position[0]-vector[0]*10- self.rect.centerx), int(player_position[1] -vector[1]*10- self.rect.centery))
        # print(offset)
        if self.mask.overlap(player_mask, offset):
            # print("bateu")
            print(self.mask.overlap(player_mask, offset))
        else:
            pass
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

    def on_init(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pg.init()
        self._running = True
        self.clock = pg.time.Clock()
        # resolution = (int(pg.display.Info().current_w), int(pg.display.Info().current_h))
        
        self._display_surf = pg.display.set_mode(self.size) 
        self.screen = pg.display.get_surface() # repetido?
        
        self.PLAYER_POSITION = (self.width/2, self.height/2)
        self.PLAY_IMAGE = pg.image.load("player2.png")
        self.PLAY_IMAGE = pg.transform.scale(self.PLAY_IMAGE, (75,75))
        self.BACK_IMAGE = pg.image.load("city1_back.png").convert_alpha()
        self.FRONT_IMAGE = pg.image.load("city1.jpg").convert_alpha()
        
        self.player = Player(self.PLAY_IMAGE, self.PLAYER_POSITION, 7)
        self.back = Background(self.BACK_IMAGE, self.FRONT_IMAGE, self.PLAYER_POSITION, 7)

    def on_event(self, event):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            self._running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.pressionou_w = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_w:
                self.pressionou_w = False
        
    def display_fps(self):
        pg.display.set_caption("{} - FPS: {:.2f}".format("PyShooter", self.clock.get_fps()))

    def on_loop(self):
        if self.pressionou_w:
            self.actual_position = self.player.position
            self.mouse_position = pg.mouse.get_pos()
            self.direction_of_move = -(self.mouse_position - self.actual_position)
            self.direction_of_move /= self.direction_of_move.length()
            self.back.move(self.direction_of_move, self.player.mask, self.player.position)
        self.clock.tick(self.fps)

    def on_cleanup(self):
        pg.quit()
        sys.exit()

    def on_render(self):
        self.screen.fill((0,0,0))
        self.back.draw(self.screen)
        self.player.draw(self.screen)
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
