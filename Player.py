import pygame as pg

class Player():
    def __init__(self, image, location_on_scenario, location_on_screen, animation, sound):
        self.animation = animation
        self.sound = sound
        self.index_animation_move = 0        
        self.index_animation_shoot = 0

        self.position_on_screen = pg.math.Vector2(location_on_screen)
        self.position_on_scenario = pg.math.Vector2(location_on_scenario)

        # handle events
        self.pressionou_w = False
        self.pressionou_a = False
        self.pressionou_s = False
        self.pressionou_d = False
        self.is_shooting = False

    def draw(self, surface):
        if self.pressionou_w or self.pressionou_d or self.pressionou_a or self.pressionou_s:
            self.actual_position = self.position_on_screen
            self.mouse_position = pg.mouse.get_pos()
            self.vector_position = self.mouse_position - self.actual_position

            if self.pressionou_w:
                self.direction_of_move = (self.vector_position)
                self.move(self.direction_of_move)

            if self.pressionou_s:
                self.direction_of_move = -(self.vector_position)
                self.move(self.direction_of_move)

            if self.pressionou_a:
                self.direction_of_move = -(self.vector_position).rotate(90)
                self.move(self.direction_of_move)

            if self.pressionou_d:
                self.direction_of_move = (self.vector_position).rotate(90)
                self.move(self.direction_of_move)
        
        if self.is_shooting:
            self.sound.play()

            self.image = self.animation.shoot[self.index_animation_shoot]
            self.original_image = self.animation.shoot[self.index_animation_shoot]
            self.index_animation_shoot += 1
            if self.index_animation_shoot == len(self.animation.shoot):
                self.index_animation_shoot = 0
        else:
            self.sound.shoot.fadeout(100)
            # self.sound.stop()
            self.image = self.animation.move[self.index_animation_move]
            self.original_image = self.animation.move[self.index_animation_move]
        
        self.rect = self.image.get_rect()
        self.update()
        surface.blit(self.image, self.rect)

    def update(self):
        self.rotate()
        self.rect.center = self.position_on_screen

    def move(self, direction):
        self.position_on_scenario += 5*(direction/direction.length())
        self.index_animation_move += 1
        if self.index_animation_move == len(self.animation.move):
            self.index_animation_move = 0

    def rotate(self):
        _, angle = (pg.mouse.get_pos()-self.position_on_screen).as_polar()
        self.image = pg.transform.rotozoom(self.original_image, -angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def handle_event(self, event):

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

        if event.type == pg.MOUSEBUTTONDOWN:
            self.is_shooting = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.is_shooting = False
