import Code.Sound as Sound
import Code.helpers as helpers

class Weapon:
    def __init__(self):
        self.type = 'rifle'
        self.fire_rate_list = {'rifle': 250, 'shotgun': 1200, 'handgun': 300, 'knife': 400}
        self.max_distance_list = {'rifle': 500, 'shotgun': 200, 'handgun': 300}
        self.ammo_limit_list = {'rifle': 15, 'shotgun': 10, 'handgun': 20}
        self.ammo_list = {'rifle': 15, 'shotgun': 10, 'handgun': 20}
        self.weapon_list = {'rifle': False, 'shotgun': False, 'handgun': True, 'knife': True}
        self.damage_list = {'rifle': 1, 'shotgun': 3, 'handgun': 1, 'knife': 1}

        Sound.Weapon.load()

    def change_weapon(self, new_weapon):
        self.type = new_weapon

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
        else:
            print('sound type invalid <Weapon class>')

    @classmethod
    def get_damage(cls, weapon_type):
        damage_list = {'rifle': 1, 'shotgun': 3, 'handgun': 1, 'knife': 1}
        return damage_list[weapon_type]


