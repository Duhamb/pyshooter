import pygame as pg

import Code.Player as Player
import Code.Background as Background
import Code.Bot as Bot
import Code.ExtendedGroup as ExtendedGroup
import Code.Projectiles as Projectiles
import Code.constants as constants
import Code.Animation as Animation
import Code.Sound as Sound
import Code.helpers as helpers

class ObjectsController:
    def __init__(self, player, background, multiplayer_on, server_client, menu, players, is_host, aim):

        self.aim = aim

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

        self.bot_draw = Bot.Bot((0, 0), self.screen, self.background, self.player, self.zombie_animation)

        self.bot0 = Bot.Bot((0, -1400), self.screen, self.background, self.player, self.zombie_animation)
        self.bot1 = Bot.Bot((-100, -1400), self.screen, self.background, self.player, self.zombie_animation)
        self.bot2 = Bot.Bot((100, -1400), self.screen, self.background, self.player, self.zombie_animation)
        self.bot3 = Bot.Bot((200, -1400), self.screen, self.background, self.player, self.zombie_animation)
        self.bot4 = Bot.Bot((300, -1400), self.screen, self.background, self.player, self.zombie_animation)
        self.bot5 = Bot.Bot((400, -1400), self.screen, self.background, self.player, self.zombie_animation)
        self.bot6 = Bot.Bot((500, -1400), self.screen, self.background, self.player, self.zombie_animation)
        self.bot7 = Bot.Bot((600, -1400), self.screen, self.background, self.player, self.zombie_animation)
        self.bot8 = Bot.Bot((700, -1400), self.screen, self.background, self.player, self.zombie_animation)
        self.bot9 = Bot.Bot((800, -1400), self.screen, self.background, self.player, self.zombie_animation)

        self.bot_list = ExtendedGroup.ExtendedGroup(self.bot0)
        self.bot_list.add(self.bot1)
        self.bot_list.add(self.bot2)
        self.bot_list.add(self.bot3)
        self.bot_list.add(self.bot4)
        self.bot_list.add(self.bot5)
        self.bot_list.add(self.bot6)
        self.bot_list.add(self.bot7)
        self.bot_list.add(self.bot8)
        self.bot_list.add(self.bot9)


        self.bullet_list = ExtendedGroup.ExtendedGroup()
        self.BULLET_IMAGE = pg.image.load("Assets/Images/bullets/bullet1.png")
        self.BULLET_IMAGE = pg.transform.scale(self.BULLET_IMAGE, (15, 3))

        self.delta_time = 0
        self.second_get_ticks = 0
        self.fire_rate_counter = 0
        self.can_render_bullet = False
        self.shooter_name = None

    def handle_event(self):
        if self.player.weapon.type != 'knife' and not self.player.is_reloading and self.player.is_shooting and self.fire_rate_counter > self.player.weapon.fire_rate():
            if self.player.weapon.ammo_list[self.player.weapon.type] > 0:
                self.can_render_bullet = True
                mouse_position = self.aim.position
                if self.multiplayer_on:
                    bullet = Projectiles.Projectiles(self.player.position_on_scenario,
                                         self.BULLET_IMAGE,
                                         self.background,
                                         helpers.screen_to_scenario(mouse_position, self.background, False),
                                         self.server_client.name,
                                         self.player.weapon.type)
                else:
                    bullet = Projectiles.Projectiles(self.player.position_on_scenario,
                                         self.BULLET_IMAGE, self.background,
                                         helpers.screen_to_scenario(mouse_position, self.background, False),
                                         None,
                                         self.player.weapon.type)
                    
                self.bullet_list.add(bullet)
                self.fire_rate_counter = 0
                self.player.weapon.ammo_list[self.player.weapon.type] -= 1
                self.player_sound.shoot.stop()
                helpers.get_free_channel().play(self.player_sound.shoot)
            else:
                self.player_sound.empty.stop()
                helpers.get_free_channel().play(self.player_sound.empty)
                self.fire_rate_counter = 0

    def update(self):
        if self.player.weapon.type != 'knife' and (not self.player.is_shooting or self.player.weapon.ammo_list[self.player.weapon.type] == 0):
            self.can_render_bullet = False
        # Time references
        self.first_get_ticks = self.second_get_ticks
        self.second_get_ticks = pg.time.get_ticks()
        self.delta_time = self.second_get_ticks - self.first_get_ticks
        self.fire_rate_counter += self.delta_time
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
                bot.stop_grunt()
                self.bot_list.remove(bot)
                if self.shooter_name == None:
                    self.player.score = self.player.score + 100
                else:
                    self.server_client.add_points(self.shooter_name)

        # Update for bullets
        for bullet in self.bullet_list:
            if bullet.distance > self.player.weapon.max_distance(bullet.weapon_type) or bullet.is_colliding:
                self.bullet_list.remove(bullet)

    def draw(self):
        if self.multiplayer_on:
            #Player Syn
            self.server_client.push_player(self.player, self.can_render_bullet)
            self.server_client.pull_players()
            player_list = self.server_client.players_info
            for player_name in player_list:
                actual_player = player_list[player_name]
                self.player.draw_multiplayer(self.screen, actual_player)
                if actual_player['is_shooting'] and player_name != self.menu.name and self.players_fire_rates.get(player_name, 400) > 300:
                    self.players_fire_rates[player_name] = 0
                    bullet = Projectiles.Projectiles(actual_player['position_on_scenario'],
                                         self.BULLET_IMAGE,
                                         self.background,
                                         actual_player['mouse_position'],
                                         player_name)
                    self.bullet_list.add(bullet)

            #Zombie Syn
            #Host send zombie list
            if self.is_host:
                self.bot_list.update(self.bot_list)
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
            self.bot_list.update(self.bot_list)
            self.players.draw(self.screen)
            self.bot_list.draw(self.screen)

        self.bullet_list.update()
        self.bullet_list.draw(self.screen)