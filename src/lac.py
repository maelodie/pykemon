import random
from settings import *
from sprites import Generic

class Lac():
    def __init__(self, all_sprites, lac):
        self.all_sprites = all_sprites
        self.lac = lac

    def Flood(self):
        if random.random() <= P_INONDATION:
            for a in self.lac:
                random_number = random.randint(1, 4)

                if random_number == 1:  # gauche
                    pos = (a.rect.x - TILE_SIZE, a.rect.y)
                elif random_number == 2:  # haut
                    pos = (a.rect.x, a.rect.y - TILE_SIZE)
                elif random_number == 3:  # droite
                    pos = (a.rect.x + TILE_SIZE, a.rect.y)
                else:  # bas
                    pos = (a.rect.x, a.rect.y + TILE_SIZE)

                collision = False
                for sprite in self.lac:
                    if sprite.rect.collidepoint(pos):
                        collision = True
                        break

                if not collision:
                    Generic(pos, a.image, [self.all_sprites, self.lac], LAYERS['water'])

    def Drought(self):
        for a in self.lac:
            if random.random() <= P_SECHERESSE:
                self.lac.remove(a)
                self.all_sprites.remove(a)




