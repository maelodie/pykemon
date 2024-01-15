import math
from sprites import FireTree, CutTree, Tree
import random
from settings import *
from support import import_folder

class Fire():
    def __init__(self, all_sprites, collisions_sprites, tree_sprites, healthy_trees, fire_trees, dead_trees):
        #Ce sont des listes de sprites (pas d'objets de type sprites)
        self.all_sprites = all_sprites
        self.collisions = collisions_sprites
        self.tree_sprites = tree_sprites
        self.healthy_trees = healthy_trees
        self.fire_trees = fire_trees
        self.dead_trees = dead_trees
        self.nb_healthy_tree = len(all_sprites)
        self.nb_fire_tree = len(self.fire_trees)
        self.nb_cut_tree = len(self.dead_trees)
        self.cpt = 0


    def burnForest(self, raining):
        if not raining:
            for i in self.healthy_trees:
                for j in self.fire_trees:
                    if((math.sqrt((i.rect.x - j.rect.x)**2+(i.rect.y - j.rect.y)**2)) < DISTANCE_FEU ):
                        if(random.random()<=P_BRULE):
                            burnTree(i, self.all_sprites, self.collisions, self.tree_sprites, self.healthy_trees, self.fire_trees)

    def cutForest(self):
        for i in self.fire_trees:
            if(random.random()<= P_CUT):
                CutTree((i.rect.x, i.rect.y), cut_tree_image, [self.all_sprites, self.collisions, self.tree_sprites, self.dead_trees], LAYERS['trees'],  "CutTree")
                self.all_sprites.remove(i)
                i.kill()
                self.tree_sprites.remove(i)
                self.fire_trees.remove(i)

    def growForest(self):
        for i in self.dead_trees:
            if(random.random()<= P_POUSSE):
                Tree((i.rect.x, i.rect.y), tree_image, [self.all_sprites, self.collisions, self.tree_sprites, self.healthy_trees], LAYERS['trees'], "Tree")
                self.all_sprites.remove(i)
                i.kill()
                self.tree_sprites.remove(i)
                self.dead_trees.remove(i)

    def afficher(self):
        #Affichages terminal
        a = len(self.healthy_trees)
        b = len(self.fire_trees)
        c = len(self.dead_trees)
        self.cpt += 1
        print(self.cpt, a/10, round(1/a*10000,1))

    def forest(self, raining):
        self.burnForest(raining)
        self.cutForest()
        self.growForest()

#globales
def burnTree(tree, all_sprites, collisions_sprites, tree_sprites, healthy_trees, fire_trees):
    FireTree((tree.rect.x, tree.rect.y), fire_tree_image, [all_sprites, collisions_sprites, tree_sprites, fire_trees], LAYERS['trees'], "FireTree")
    all_sprites.remove(tree)
    tree_sprites.remove(tree)
    healthy_trees.remove(tree)
    tree.kill()

#variables globales :)
tree_image = pygame.image.load("../data/graphics/objects/trees/tree.png")
fire_tree_image = pygame.image.load("../data/graphics/objects/trees/fire_tree.png")
cut_tree_image = pygame.image.load("../data/graphics/objects/trees/cut_tree.png")
