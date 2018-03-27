import pygame as pg

from Player import *
from Background import *
from Bot import *
from ExtendedGroup import *
from Projectiles import *

import Animation
import Sound

class ObjectsController:
    def __init__(self, player, background):

        self.screen = pg.display.get_surface()
        self.player = player
        self.background = background
        self.player_sound = Sound.Player
        self.player_sound.load()

        self.BOT_IMAGE = pg.image.load("Assets/Images/player2.png")
        self.BOT_IMAGE = pg.transform.scale(self.BOT_IMAGE, (75, 75))

        self.zombie_animation = Animation.Zombie
        self.zombie_animation.load()

        self.bot0 = Bot((100, -1400), self.screen, self.background, self.player, self.zombie_animation)
        self.bot1 = Bot((-100, -1400), self.screen, self.background, self.player, self.zombie_animation)
        self.bot2 = Bot((200, -1400), self.screen, self.background, self.player, self.zombie_animation)

        self.bot_list = ExtendedGroup(self.bot0)
        self.bot_list.add(self.bot1)
        self.bot_list.add(self.bot2)

        self.bullet_list = ExtendedGroup()
        self.BULLET_IMAGE = pg.image.load("Assets/Images/bullets/bullet1.png")
        self.BULLET_IMAGE = pg.transform.scale(self.BULLET_IMAGE, (15, 3))

        self.delta_time = 0
        self.second_get_ticks = 0
        self.fire_rate = 0

    def handle_event(self):
        if self.player.is_shooting and self.fire_rate > 300:
            bullet = Projectiles(self.player.position_on_scenario, self.player.position_on_screen, self.BULLET_IMAGE, self.background)
            self.bullet_list.add(bullet)
            self.fire_rate = 0
            pygame.mixer.Channel(1).play(self.player_sound.shoot, -1)

    def update(self):
        # Time references
        self.first_get_ticks = self.second_get_ticks
        self.second_get_ticks = pg.time.get_ticks()
        self.delta_time = self.second_get_ticks - self.first_get_ticks
        self.fire_rate += self.delta_time

        collisions = pg.sprite.groupcollide(self.bot_list, self.bullet_list, dokilla=False, dokillb=True)
        for zombie in collisions:
            zombie.gets_hit()

        # Update for zombies
        for bot in self.bot_list:
            if bot.is_dead:
                self.bot_list.remove(bot)

        # Update for bullets
        for bullet in self.bullet_list:
            if bullet.distance > 300 or bullet.is_colliding:
                self.bullet_list.remove(bullet)

    def draw(self):

        self.bot_list.update()
        self.bullet_list.update()

        self.bullet_list.draw(self.screen)
        self.bot_list.draw(self.screen)