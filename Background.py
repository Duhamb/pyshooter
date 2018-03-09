import pygame as pg

# acho melhor essa ficar sem herança da sprite enquanto não resolver a colisão

def get_list_points(list_masks):
    answer = []
    for mask in list_masks:
        olist_reduced = []
        eliminar = []
        olist = mask.outline(40)
        max_size = len(olist)
        print(max_size, end=" ")
        ind1 = 0
        ind2 = 1
        ind3 = 2
        while ind3 < max_size:
            vet1 = (pg.math.Vector2(olist[ind2]) - pg.math.Vector2(olist[ind1])).normalize()
            vet2 = (pg.math.Vector2(olist[ind3]) - pg.math.Vector2(olist[ind2])).normalize()
            if abs(vet1.cross(vet2)) < 0.4:
                eliminar.append(ind2)
                ind2 += 1
                ind3 += 1
            else:
                ind1 = ind2 
                ind2 += 1
                ind3 += 1

        for i in range(0,max_size):
            if i not in eliminar:
                olist_reduced.append(olist[i])
        answer.append(olist_reduced)
        print(len(olist_reduced), end=", ")
        olist_reduced = []
        eliminar = []

    return answer

class Background():
    def __init__(self, back, front):
        self.front = front
        self.back = back
        self.rect = self.front.get_rect()
        self.mask = pg.mask.from_surface(self.back)

        # self.array = pg.surfarray.array2d(self.back)

        self.list_masks = self.mask.connected_components(200)

        self.list_points = get_list_points(self.list_masks)

        # print(self.front.get_size())
        # print(self.back.get_size())

    def draw(self, surface, player):
        self.update_position(player)
        surface.blit(self.front, self.rect)
        # surface.blit(self.back, self.rect)

        for olist in self.list_points:
            pg.draw.lines(surface,(200,150,150), 1, olist, 3)

    def update_position(self, player):
        self.rect.center = player.position_on_screen - player.position_on_scenario