import pygame as pg

from Player import *
from Background import *
from Bot import *
from ExtendedGroup import *
from Projectiles import *

import Animation
import Sound

class ObjectsController:
    def __init__(self, player, background, multiplayer_on, server_client, menu, players, is_host):

        self.screen = pg.display.get_surface()
        self.player = player
        self.background = background
        self.player_sound = Sound.Player
        self.player_sound.load()
        self.players_fire_rates = {}

        self.multiplayer_on = multiplayer_on
        self.server_client = server_client
        self.menu = menu
        self.players = players
        self.is_host = is_host

        self.BOT_IMAGE = pg.image.load("Assets/Images/player2.png")
        self.BOT_IMAGE = pg.transform.scale(self.BOT_IMAGE, (75, 75))

        self.zombie_animation = Animation.Zombie
        self.zombie_animation.load()

        self.bot_draw = Bot((0, 0), self.screen, self.background, self.player, self.zombie_animation)

        self.bot0 = Bot((0, -1400), self.screen, self.background, self.player, self.zombie_animation)
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
        self.can_render_bullet = False
        self.shooter_name = None

    def handle_event(self):
        if not self.player.is_reloading and self.player.is_shooting and self.fire_rate > 300:
            if self.player.bullet_counter > 0:
                self.can_render_bullet = True
                if self.multiplayer_on:
                    bullet = Projectiles(self.player.position_on_scenario, self.BULLET_IMAGE, self.background,
                                         screen_to_scenario_server(pg.mouse.get_pos(), self.background.rect),
                                         self.server_client.name)
                else:
                    bullet = Projectiles(self.player.position_on_scenario, self.BULLET_IMAGE, self.background,
                                     screen_to_scenario_server(pg.mouse.get_pos(), self.background.rect), None)
                self.bullet_list.add(bullet)
                self.fire_rate = 0
                self.player.bullet_counter -= 1
                self.player_sound.shoot.stop()
                pygame.mixer.Channel(1).play(self.player_sound.shoot)
            else:
                self.player_sound.empty.stop()
                pygame.mixer.Channel(1).play(self.player_sound.empty)
                self.fire_rate = 0

    def update(self):
        if not self.player.is_shooting or self.player.bullet_counter == 0:
            self.can_render_bullet = False
        # Time references
        self.first_get_ticks = self.second_get_ticks
        self.second_get_ticks = pg.time.get_ticks()
        self.delta_time = self.second_get_ticks - self.first_get_ticks
        self.fire_rate += self.delta_time
        for names in self.players_fire_rates:
            self.players_fire_rates[names] += self.delta_time

        # Collisions between zombies and bullets
        collisions_bullets = pg.sprite.groupcollide(self.bullet_list, self.bot_list, dokilla=False, dokillb=False)
        for bullet in collisions_bullets:
            self.shooter_name = bullet.shooter_name
        collisions_zombies = pg.sprite.groupcollide(self.bot_list, self.bullet_list, dokilla=False, dokillb=True)
        for zombie in collisions_zombies:
            zombie.gets_hit()


        # Update for zombies
        for bot in self.bot_list:
            if bot.is_dead:
                self.bot_list.remove(bot)
                if self.shooter_name == None:
                    self.player.score = self.player.score + 100
                else:
                    self.server_client.add_points(self.shooter_name)

        # Update for bullets
        for bullet in self.bullet_list:
            if bullet.distance > 300 or bullet.is_colliding:
                self.bullet_list.remove(bullet)

    def draw(self):

        if self.multiplayer_on:

            #Player Syn
            self.server_client.push_player(self.player, self.can_render_bullet)
            self.server_client.pull_players()
            player_list = self.server_client.players_info
            #print(player_list)
            for player_name in player_list:
                actual_player = player_list[player_name]
                self.player.draw_multiplayer(self.screen, actual_player)
                if actual_player['is_shooting'] and player_name != self.menu.name and self.players_fire_rates.get(player_name, 400) > 300:
                    self.players_fire_rates[player_name] = 0
                    bullet = Projectiles(actual_player['position_on_scenario'],
                                         self.BULLET_IMAGE, self.background, actual_player['mouse_position'],
                                         player_name)
                    self.bullet_list.add(bullet)

            #Zombie Syn
            #Host send zombie list
            if self.is_host:
                self.bot_list.update()
                zombie_server_list = {}
                id = 0
                for zombie in self.bot_list:
                    zombie_server_list[id] = zombie.get_server_info()
                    id = id +1
                self.server_client.push_zombies(zombie_server_list, True)
            else:
                self.server_client.push_zombies({}, False)
            #receive zombie list
            self.server_client.pull_zombies()
            zombie_list = self.server_client.zombies_info
            for zombie_id in zombie_list:
                self.bot_draw.draw_multiplayer(self.screen, zombie_list[zombie_id])
        else:
            self.bot_list.update()
            self.players.draw(self.screen)
            self.bot_list.draw(self.screen)

        self.bullet_list.update()
        self.bullet_list.draw(self.screen)