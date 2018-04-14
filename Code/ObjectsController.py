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
import random

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
        self.bot_list = ExtendedGroup.ExtendedGroup()

        self.bullet_list = ExtendedGroup.ExtendedGroup()
        self.BULLET_IMAGE = pg.image.load("Assets/Images/bullets/bullet1.png")
        self.BULLET_IMAGE = pg.transform.scale(self.BULLET_IMAGE, (15, 3))

        self.delta_time = 0
        self.second_get_ticks = 0
        self.fire_rate_counter = 0
        self.can_render_bullet = False
        self.shooter_name = None
        self.spawn_rate = 0
        self.cant_spawn = True
        self.bot_spawn = None
        self.max_zombies = 50

    def handle_event(self):
        if self.player.weapon.type != 'knife' and not self.player.is_reloading and self.player.is_shooting and self.fire_rate_counter > self.player.weapon.fire_rate():
            if self.player.weapon.ammo_list[self.player.weapon.type] > 0:
                self.can_render_bullet = True
                mouse_position = self.aim.position
                player_name = None
                if self.multiplayer_on:
                    player_name = self.server_client.name
                bullet = Projectiles.Projectiles(self.player.position_on_scenario,
                                     self.BULLET_IMAGE,
                                     self.background,
                                     helpers.screen_to_scenario(mouse_position, self.background, False),
                                     player_name,
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
        self.delta_time = self.get_delta_time()
        self.fire_rate_counter += self.delta_time
        self.spawn_rate += self.delta_time
        for names in self.players_fire_rates:
            self.players_fire_rates[names] += self.delta_time

        # Collisions between zombies and bullets
        collisions_bullets = pg.sprite.groupcollide(self.bullet_list, self.bot_list, dokilla=False, dokillb=False)
        for bullet in collisions_bullets:
            self.shooter_name = bullet.shooter_name
        collisions_zombies = pg.sprite.groupcollide(self.bot_list, self.bullet_list, dokilla=False, dokillb=True)
        for zombie in collisions_zombies:
            zombie.gets_hit()
        
        # update for players
        self.update_player_group()

        # Spawn for zombies
        self.spawn_bots()
        self.bot_list.update(None,self.player_group)

        # Update for zombies
        for bot in self.bot_list:
            if bot.is_dead:
                bot.stop_grunt()
                self.bot_list.remove(bot)
                if self.shooter_name == None:
                    self.player.score = self.player.score + 100
                else:
                    self.server_client.add_points(self.shooter_name)

        # update server info for zombies
        #Zombie Syn
        #Host send zombie list
        if self.multiplayer_on:
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

        # Update for bullets
        for bullet in self.bullet_list:
            if bullet.distance > self.player.weapon.max_distance(bullet.weapon_type) or bullet.is_colliding:
                self.bullet_list.remove(bullet)

    def draw(self):
        if self.multiplayer_on:
            #Player Syn
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
                                         player_name,
                                         actual_player['weapon_type'])
                    self.bullet_list.add(bullet)

            zombie_list = self.server_client.zombies_info
            for zombie_id in zombie_list:
                self.bot_draw.draw_multiplayer(self.screen, zombie_list[zombie_id], player_list)
        else:
            self.bot_list.update(self.bot_list)
            self.players.draw(self.screen)
            self.bot_list.draw(self.screen)

        self.bullet_list.update()
        self.bullet_list.draw(self.screen)

    def get_delta_time(self):
        first_get_ticks = self.second_get_ticks
        self.second_get_ticks = pg.time.get_ticks()
        delta_time = self.second_get_ticks - first_get_ticks
        return delta_time

    def generate_random_location(self):
        return (int(random.uniform(-4500,4500)),int(random.uniform(-4500,4500)))

    def spawn_bots(self):
        # Spawn for zombies
        if self.spawn_rate > 1000 and len(self.bot_list) < self.max_zombies:
            while self.cant_spawn:
                self.bot_spawn = Bot.Bot(self.generate_random_location(),
                                          self.screen,
                                          self.background,
                                          self.player_group,
                                          self.zombie_animation)
                self.cant_spawn = pg.sprite.spritecollideany(self.bot_spawn, self.background.collider_group)
            self.cant_spawn = True
            self.bot_list.add(self.bot_spawn)
            self.spawn_rate = 0

    def update_player_group(self):
        # self.player_group can be a dict with players info from server or
        # self.player_group can be a only object of Player class
        if self.multiplayer_on:
            self.server_client.push_player(self.player, self.can_render_bullet)
            self.server_client.pull_players()
            self.player_group = self.server_client.players_info
        else:
            self.player_group = self.player