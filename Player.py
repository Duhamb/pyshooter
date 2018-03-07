import pygame as pg

# [TODO] descobrir como alterar o group.draw pra renderizar duas imagens
# alternativa: unir as duas imagens e passar somente a união delas

class Player(pg.sprite.Sprite):
    def __init__(self, image, back_image, location_on_scenario, location_on_screen, animation, sound, background):
        super().__init__()
        self.animation = animation
        self.sound = sound
        self.index_animation_move = 0        
        self.index_animation_shoot = 0
        self.back_image = back_image
        self.original_back_image = back_image
        self.background = background
        self.loc = location_on_screen

        # the image center isnt correct
        self.delta_center_position = pg.math.Vector2((+56/2.7,-19/2.7))

        self.mask = pg.mask.from_surface(self.animation.move[0])
        self.rect = animation.move[0].get_rect(center = location_on_screen)
        self.image = animation.move[0]

        self.position_on_screen = pg.math.Vector2(location_on_screen)
        self.position_on_scenario = pg.math.Vector2(location_on_scenario)

        # handle events
        self.pressionou_w = False
        self.pressionou_a = False
        self.pressionou_s = False
        self.pressionou_d = False
        self.is_shooting = False

    def update(self):
        self.react_to_event()
        self.rotate()

    # esse metodo não sobrescreveu
    # a draw é um metodo do grupo
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.feet, self.position_on_screen)

    def move(self, direction):
        self.temp_position_on_scenario = self.position_on_scenario + 5*pg.math.Vector2(direction/direction.length())
        self.temp_index_animation_move = self.index_animation_move + 1
        if self.temp_index_animation_move == len(self.animation.move):
            self.temp_index_animation_move = 0
  
        self.temp_rect = self.animation.move[self.temp_index_animation_move].get_rect(center=self.position_on_screen)
        self.temp_mask = pg.mask.from_surface(self.back_image)

        self.background.rect.center = self.position_on_screen - self.temp_position_on_scenario
        self.offset = ((-self.background.rect.left + self.temp_rect.left), (-self.background.rect.top + self.temp_rect.top))
        self.is_colliding = self.background.mask.overlap(self.temp_mask, self.offset)
        if self.is_colliding:
            print("invalid move!")
            print(self.position_on_scenario + pg.math.Vector2(self.background.rect.size)/2)
            print(self.is_colliding)
        else:
            self.position_on_scenario += 5*(direction/direction.length())
            self.index_animation_move += 1
            if self.index_animation_move == len(self.animation.move):
                self.index_animation_move = 0


    def rotate(self):
        _, angle = (pg.mouse.get_pos()-self.position_on_screen).as_polar()
        self.image = pg.transform.rotozoom(self.original_image, -angle, 1)
        self.feet = pg.transform.rotozoom(self.original_feet, -angle, 1)
        self.back_image = pg.transform.rotozoom(self.original_back_image, -angle, 1)

        self.rotated_center = self.delta_center_position.rotate(+angle)
        self.new_rect_center = self.rotated_center + self.position_on_screen

        self.rect = self.image.get_rect(center=self.new_rect_center)

    # esse metodo pode estar no grupo também
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

    def react_to_event(self):
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
            # self.sound.zoa.play()

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

        self.feet = self.animation.run[self.index_animation_move]
        self.original_feet = self.animation.run[self.index_animation_move]