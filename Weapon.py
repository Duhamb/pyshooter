class Weapon:
    def __init__(self):

        self.type = 'rifle'
        self.fire_rate_list = {'rifle': 250, 'shotgun': 700, 'handgun': 300, 'knife': 400}
        self.max_distance_list = {'rifle': 500, 'shotgun': 200, 'handgun': 300}
        self.ammo_limit_list = {'rifle': 15, 'shotgun': 10, 'handgun': 20}
        self.ammo_list = {'rifle': 15, 'shotgun': 10, 'handgun': 20}
        self.weapon_list = {'rifle': False, 'shotgun': False, 'handgun': True, 'knife': True}
        self.damage_list = {'rifle': 1, 'shotgun': 3, 'handgun': 1, 'knife': 1}

    def change_weapon(self, new_weapon):
        self.type = new_weapon

    def fire_rate(self):
        return self.fire_rate_list[self.type]

    def max_distance(self):
        return self.max_distance_list[self.type]