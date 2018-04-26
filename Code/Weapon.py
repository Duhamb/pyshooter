import Code.Sound as Sound
import Code.helpers as helpers

class Weapon:
    def __init__(self):

        self.type = 'handgun'
        self.fire_rate_list = {'rifle': 250, 'shotgun': 1200, 'handgun': 300, 'knife': 400}

        self.max_distance_list = {'rifle': 500, 'shotgun': 200, 'handgun': 300}
        self.ammo_limit_list = {'rifle': 15, 'shotgun': 10, 'handgun': 20}
        self.loaded_ammo_list = {'rifle': 0, 'shotgun': 0, 'handgun': 20}
        self.unloaded_ammo_list = {'rifle': 0, 'shotgun': 0, 'handgun': 20}
        self.weapon_list = {'rifle': False, 'shotgun': False, 'handgun': True, 'knife': True}
        self.damage_list = {'rifle': 1, 'shotgun': 3, 'handgun': 1, 'knife': 1}

        Sound.Weapon.load()

        self.player_reload_played = False
        self.player_out_of_ammo_played = False

    def change_weapon(self, new_weapon):
        if self.weapon_list[new_weapon]:
            self.type = new_weapon
            self.player_reload_played = False
            self.player_out_of_ammo_played = False

    def fire_rate(self):
        return self.fire_rate_list[self.type]

    def max_distance(self, weapon_type):
        return self.max_distance_list[weapon_type]

    def make_sound(self, sound_type):
        if sound_type == 'shoot':
            if self.type == 'rifle':
                helpers.get_free_channel().play(Sound.Weapon.rifle_shoot)
            elif self.type == 'shotgun':
                helpers.get_free_channel().play(Sound.Weapon.shotgun_shoot)
            elif self.type == 'handgun':
                helpers.get_free_channel().play(Sound.Weapon.rifle_shoot)
        elif sound_type == 'reload':
            if self.type == 'rifle':
                helpers.get_free_channel().play(Sound.Weapon.rifle_reload)
            elif self.type == 'shotgun':
                helpers.get_free_channel().play(Sound.Weapon.shotgun_reload)
            elif self.type == 'handgun':
                helpers.get_free_channel().play(Sound.Weapon.rifle_reload)
        elif sound_type == 'meleeattack':
            helpers.get_free_channel().play(Sound.Weapon.meleeattack)
        elif sound_type == 'empty':
            helpers.get_free_channel().play(Sound.Weapon.empty)
            if self.loaded_ammo_list[self.type] == 0:
                if self.unloaded_ammo_list[self.type] == 0 and not self.player_out_of_ammo_played:
                    helpers.get_free_channel().play(Sound.Weapon.player_out_of_ammo)
                    self.player_out_of_ammo_played = True
                elif not self.player_reload_played:
                    helpers.get_free_channel().play(Sound.Weapon.player_reload)
                    self.player_reload_played = True

        else:
            print('sound type invalid <Weapon class>')

    @classmethod
    def get_damage(cls, weapon_type):
        damage_list = {'rifle': 1, 'shotgun': 3, 'handgun': 1, 'knife': 1}
        return damage_list[weapon_type]


