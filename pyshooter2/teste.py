import os
import pygame as pg
import math

def loadImage(filename):
    return pg.image.load(os.path.join(filename))
player_surface = loadImage("player3.png")

class Player(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.transform.scale(player_surface, (75,75))
        self.orig_img = self.image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.math.Vector2(pos)
        self.vel = pg.math.Vector2(0, 0)

    def update(self):
        self.rotate()
        self.pos += self.vel
        self.rect.center = self.pos

    def rotate(self):
        _, angle = (pg.mouse.get_pos()-self.pos).as_polar()
        self.image = pg.transform.rotozoom(self.orig_img, -angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)


def main():
    resolution = (int(pg.display.Info().current_w), int(pg.display.Info().current_h))
    screen = pg.display.set_mode(resolution, pg.FULLSCREEN)
    clock = pg.time.Clock()

    center_x = pg.display.get_surface().get_rect().width/2
    center_y = pg.display.get_surface().get_rect().height - 50


    all_sprites = pg.sprite.Group()
    p1 = Player((center_x, center_y))
    all_sprites.add(p1)

    pg.mouse.set_pos(center_x, center_y - 100)

    pressionou_w = False
    pressionou_a = False
    pressionou_s = False
    pressionou_d = False

    done = False
    while not done:
        (mouse_pos_x, mouse_pos_y) = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                done = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    pressionou_s = True
                if event.key == pg.K_w:
                    pressionou_w = True
                if event.key == pg.K_d:
                    pressionou_d = True
                if event.key == pg.K_a:
                    pressionou_a = True
                    
            if event.type == pg.KEYUP:

                if event.key == pg.K_s:
                    pressionou_s = False
                if event.key == pg.K_w:
                    pressionou_w = False
                if event.key == pg.K_d:
                    pressionou_d = False
                if event.key == pg.K_a:
                    pressionou_a = False

        dx = mouse_pos_x - p1.pos.x
        dy = mouse_pos_y - p1.pos.y
        norm = math.sqrt(dx**2 + dy**2)

        if pressionou_w:
            p1.vel.x = dx/norm*5
            p1.vel.y = dy/norm*5

        if pressionou_s:
            p1.vel.x = -dx/norm*5
            p1.vel.y = -dy/norm*5

        if pressionou_d:
            p1.vel.x = -dy/norm*5
            p1.vel.y = dx/norm*5

        if pressionou_a:
            p1.vel.x = dy/norm*5
            p1.vel.y = -dx/norm*5
        
        if not pressionou_w and not pressionou_d and not pressionou_a and not pressionou_s:
            p1.vel.x = 0
            p1.vel.y = 0

        p1.pos += p1.vel

        all_sprites.update()
        screen.fill((30, 30, 30))
        all_sprites.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()