import pygame
import math
import abc
from random import *
from settings import*
from support import *
from fire import burnTree

class Pokemon(pygame.sprite.Sprite, metaclass = abc.ABCMeta ):
    #classe abstraite
    #attributs statiques : listes pokémons
    pokemon_list = []
    pok_fire_list = []
    pok_water_list = []
    pok_poison_list = []
    dico_poke = {}
    attaque = {'Pikachu':["Vive-Attaque", "Tonnerre"]}
    cpt = 0 #pour l'affichage

    #constructeur
    def __init__(self, type, names, pos, all_sprites, collision_sprites, path):
        super().__init__(all_sprites)

        #groupes
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.path = path

        #attributs
        self.id = randint(1,1000000)
        self.type = type
        self.name = choice(names)
        self.level = 8
        self.hp = 50
        self.gender = choice(['F','M'])
        self.health = 'healthy'

        #image
        self.import_assets()
        self.status = 'down_stop'
        self.frame_index = 0
        self.cpt = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS['main']

        #paramètres déplacement
        self.direction = pygame.math.Vector2(0,0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 50

        #collision
        self.hitbox = self.rect.copy().inflate((-126,-70))

    #images pas dossier
    def import_assets(self):
        self.animations = {'up': [],'down': [],'left': [],'right': [], 'right_stop':[],'left_stop':[],'up_stop':[],'down_stop':[]}
        for animation in self.animations.keys():
            full_path = self.path + self.name + '/' + animation
            self.animations[animation] = import_folder(full_path)

    #ajout aux liste statique
    def add_to_list(self):
        Pokemon.pokemon_list.append(self)
        if self.type == 'fire':
            Pokemon.pok_fire_list.append(self)
        elif self.type == 'water':
            Pokemon.pok_water_list.append(self)
        elif self.type == 'poison':
            Pokemon.pok_poison_list.append(self)

    #animation lors du déplacement
    def animate(self, dt):
        self.frame_index += 6 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    #personnage immobile
    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_stop'

    #collision
    def collision(self, direction):
        for group in self.collision_sprites:
            for sprite in group.sprites():
                if hasattr(sprite, 'hitbox'):
                    if sprite.hitbox.colliderect(self.hitbox):
                        if direction == 'horizontal':
                            if self.direction.x > 0: #droite
                                self.hitbox.right = sprite.hitbox.left
                            if self.direction.x < 0: #gauche
                                self.hitbox.left = sprite.hitbox.right
                            self.rect.centerx = self.hitbox.centerx
                            self.pos.x = self.hitbox.centerx

                        if direction == 'vertical':
                            if self.direction.y > 0: #bas
                                self.hitbox.bottom = sprite.hitbox.top
                            if self.direction.y < 0: #haut
                                self.hitbox.top = sprite.hitbox.bottom
                            self.rect.centery = self.hitbox.centery
                            self.pos.y = self.hitbox.centery

    #déplacement aléatoire
    def move(self,dt):
        self.cpt += dt
        if self.cpt > 2:
            self.direction.x = self.direction.y = 0
            self.direction.x = choice([-1,1,0])
            if self.direction.x == 1:
                self.status = 'right'
            if self.direction.x == -1:
                self.status = 'left'
            if self.direction.x == 0:
                self.direction.y = choice([-1,1,0])
                if self.direction.y == 1:
                    self.status = 'down'
                if self.direction.x == -1:
                    self.status = 'up'
                if self.direction.y == 0:
                    self.status = 'down'
            self.cpt = 0

        #normaliser le vecteur pour avoir un vecteur unitaire
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

            #mouvement horizontal
            self.pos.x += self.direction.x * self.speed * dt
            self.hitbox.centerx = round(self.pos.x)
            self.rect.centerx = self.hitbox.centerx
            self.collision('horizontal')

            #mouvement vertical
            self.pos.y += self.direction.y * self.speed * dt
            self.hitbox.centery = round(self.pos.y)
            self.rect.centery = self.hitbox.centery
            self.collision('vertical')

    def death(self):
        if(self.hp == 0):
            self.type = 'dead'
            Pokemon.pokemon_list.remove(self)
            self.kill()

    @abc.abstractmethod
    def reproduction(self):
        pass

    @abc.abstractmethod
    def evolution(self):
        pass

    def update(self, dt):
        self.get_status()
        self.move(dt)
        self.animate(dt)
        self.death()
        self.evolution()
        self.reproduction()

    def afficher(self):
        a = len(Pokemon.pok_fire_list)
        b = len(Pokemon.pok_water_list)
        c = len(Pokemon.pok_poison_list)
        Pokemon.cpt += 1
        print(Pokemon.cpt, a, b, c)

#pokémon feu
class PokemonFire(Pokemon):
    def __init__(self, pos, all_sprites, collision_sprites):
        super().__init__('fire', ['Ponyta','Chimchar','Charmander'], pos, all_sprites, collision_sprites, '../data/graphics/pokemon/fire/')

    def reproduction(self):
        if(self.status != 'dead'):
            if random()<P_REPRODUCTION:
                for poke in Pokemon.pokemon_list:
                    #même nom/collision/genre opposé
                    if(self.name == poke.name) and self.rect.colliderect(poke.rect) and (((self.gender == 'F') and (poke.gender == 'M')) or ((self.gender == 'M') and (poke.gender == 'F'))):
                        new = PokemonFire((self.pos.x,self.pos.y), self.all_sprites, self.collision_sprites)
                        if(self.name == 'Ponyta') or (self.name == 'Rapidash'):
                            new.name == 'Ponyta'
                        elif(self.name == 'Chimchar') or (self.name == 'Monferno') or (self.name == 'Infernape'):
                            new.name == 'Chimchar'
                        elif(self.name == 'Charmander') or (self.name == 'Charmeleon') or (self.name == 'Charizard'):
                            new.name == 'Charmander'
                        new.add_to_list()
                        new.import_assets()

    #évolution de niveau du pokémon
    def evolution(self):
        if(self.status != 'dead'):
            self.level = (self.level + 0.01)
            if(round(self.level) == 15):
                if(self.name == 'Chimchar'):
                    self.name = 'Monferno'
                    self.hp = 70
                elif(self.name == 'Charmander'):
                    self.name = 'Charmeleon'
                    self.hp = 80

            elif(round(self.level) == 36):
                if(self.name == 'Monferno'):
                    self.name = 'Infernape'
                    self.hp = 110
                elif(self.name == 'Charmeleon'):
                    self.name = 'Charizard'
                    self.hp = 130

            elif(round(self.level) == 40):
                if(self.name == 'Ponyta'):
                    self.name = 'Rapidash'
                    self.hp = 90
        self.import_assets()
    
    #contamination par les pokémons poison
    def contamination(self):
        if(self.status != 'dead'):
            if self.health == 'infected':
                self.hp -= 2
            for poke in Pokemon.pok_poison_list:
                if self.rect.colliderect(poke.rect):
                    if(self.health == 'healthy'):
                        self.health = 'infected'
                        self.hp -= 4
                        if(random() > P_INFECTION):
                            self.health = 'cured'
    
    #fuite des pokémons poison
    def escape(self,dt):
      for poke in Pokemon.pok_poison_list:
        if self.rect.colliderect(poke.rect):
          if self.rect.x < poke.rect.x:
            self.pos.x -= self.speed * dt
          elif self.rect.x > poke.rect.x:
            self.pos.x += self.speed * dt
          if self.rect.y < poke.rect.y:
            self.pos.y -= self.speed * dt
          elif self.rect.y > poke.rect.y:
            self.pos.y += self.speed * dt

    #incendie       
    def fire_tree(self, all_sprites, collisions_sprites, tree_sprites, healthy_trees, fire_trees):
        for t in healthy_trees:
            d = math.sqrt((t.rect.x - self.pos.x)**2 + (t.rect.y - self.pos.y)**2)
            if(d<DISTANCE_FEU):
                if(random() > P_INCENDIE):
                    burnTree(t, all_sprites, collisions_sprites, tree_sprites, healthy_trees, fire_trees)

#polémon eau
class PokemonWater(Pokemon):
    def __init__(self, pos, all_sprites, collision_sprites):
        super().__init__('water', ['Piplup', 'Omanyte', 'Spheal'], pos, all_sprites, collision_sprites, '../data/graphics/pokemon/water/')

    def reproduction(self):
        if(self.status != 'dead'):
            if random()<P_REPRODUCTION:
                for poke in Pokemon.pokemon_list:
                    #même nom/collision/genre opposé
                    if(self.name == poke.name) and self.rect.colliderect(poke.rect) and (((self.gender == 'F') and (poke.gender == 'M')) or ((self.gender == 'M') and (poke.gender == 'F'))):
                        new = PokemonWater((self.pos.x,self.pos.y), self.all_sprites, self.collision_sprites)
                        if(self.name == 'Omanyte') or (self.name == 'Omastar'):
                            new.name == 'Omanyte'
                        elif(self.name == 'Piplup') or (self.name == 'Prinplup') or (self.name == 'Empoleon'):
                            new.name == 'Piplup'
                        elif(self.name == 'Spheal') or (self.name == 'Sealeo') or (self.name == 'Walrein'):
                            new.name == 'Spheal'
                        new.add_to_list()
                        new.import_assets()

    #évolution du niveau du pokémon
    def evolution(self):
        if(self.status != 'dead'):
            self.level = (self.level + 0.01)
            if(round(self.level) == 15):
                if(self.name == 'Piplup'):
                    self.name = 'Prinplup'
                    self.hp = 70
                elif(self.name == 'Spheal'):
                    self.name = 'Sealeo'
                    self.hp = 80

            elif(round(self.level) == 36):
                if(self.name == 'Prinplup'):
                    self.name = 'Empoleon'
                    self.hp = 110
                elif(self.name == 'Sealeo'):
                    self.name = 'Walrein'
                    self.hp = 130

            elif(round(self.level) == 40):
                if(self.name == 'Omanyte'):
                    self.name = 'Omastar'
                    self.hp = 90
        self.import_assets()
    
    #contamination par les pokémons poison
    def contamination(self):
        if(self.status != 'dead'):
            if self.health == 'infected':
                self.hp -= 2
            for poke in Pokemon.pok_poison_list:
                if self.rect.colliderect(poke.rect):
                    if(self.health == 'healthy'):
                        self.health = 'infected'
                        self.hp -= 4
                        if(random() > P_INFECTION):
                            self.health = 'cured'

    #fuite des pokémons poison
    def escape(self, dt):
      for poke in Pokemon.pok_poison_list:
        if self.rect.colliderect(poke.rect):
          if self.rect.x < poke.rect.x:
            self.pos.x -= self.speed * dt
          elif self.rect.x > poke.rect.x:
            self.pos.x += self.speed * dt
          if self.rect.y < poke.rect.y:
            self.pos.y -= self.speed * dt
          elif self.rect.y > poke.rect.y:
            self.pos.y += self.speed * dt

#pokémon poison
class PokemonPoison(Pokemon):
    def __init__(self, pos, all_sprites, collision_sprites):
        super().__init__('poison', ['Skorupi','Stunky','Gastly'], pos, all_sprites, collision_sprites, '../data/graphics/pokemon/poison/')
    
    def reproduction(self):
        if(self.status != 'dead'):
            if random()<P_REPRODUCTION:
                for poke in Pokemon.pokemon_list:
                    #même nom/collision/genre opposé
                    if(self.name == poke.name) and self.rect.colliderect(poke.rect) and (((self.gender == 'F') and (poke.gender == 'M')) or ((self.gender == 'M') and (poke.gender == 'F'))):
                        new = PokemonPoison((self.pos.x,self.pos.y), self.all_sprites, self.collision_sprites)
                        if(self.name == 'Skorupi') or (self.name == 'Drapion'):
                            new.name == 'Skorupi'
                        elif(self.name == 'Stunky') or (self.name == 'Skuntank'):
                            new.name == 'Stunky'
                        elif(self.name == 'Gastly') or (self.name == 'Haunter') or (self.name == 'Gengar'):
                            new.name == 'Gastly'
                        new.add_to_list()
                        new.import_assets()
    
    #évolution du niveau du pokémon
    def evolution(self):
        if(self.status != 'dead'):
            self.level = (self.level + 0.01)
            if(round(self.level) == 15):
                if(self.name == 'Gastly'):
                    self.name = 'Haunter'
                    self.hp = 70
                
            elif(round(self.level) == 36):
                if(self.name == 'Haunter'):
                    self.name = 'Gengar'
                    self.hp = 110
        
            elif(round(self.level) == 40):
                if(self.name == 'Skorupi'):
                    self.name = 'Drapion'
                    self.hp = 90
                elif(self.name == 'Stunky'):
                    self.name = 'Skuntank'
                    self.hp = 90
        self.import_assets()
    
    #chasse des pokémons
    def hunt(self, dt):
        for poke in Pokemon.pokemon_list:
            if poke.type != 'poison':
                if self.rect.colliderect(poke.rect):
                    if self.rect.x < poke.rect.x:
                        self.pos.x -= self.speed * dt
                    elif self.rect.x > poke.rect.x:
                        self.pos.x += self.speed * dt
                    if self.rect.y < poke.rect.y:
                        self.pos.y -= self.speed * dt
                    elif self.rect.y > poke.rect.y:
                        self.pos.y += self.speed * dt
