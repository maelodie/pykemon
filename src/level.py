import os
import pygame
from settings import *
from camera import CameraGroup
from support import *
from player import Player
from pokemon import *
from sprites import Generic, Tree, FireTree, CutTree, Flower, Mushroom, Plantation, Decoration, Batiment
from fire import Fire
from temperature import Temperature
from sky import *
from lac import Lac
from pytmx.util_pygame import load_pygame
from menu import EC



class Level:
	def __init__(self):
		#surface d'affichage
		self.display_surface = pygame.display.get_surface()
		self.display_surface.fill((192,212,112))
		self.tmx_data = load_pygame('../data/tmx/map.tmx')

		#groupes de sprite
		self.all_sprites = CameraGroup()

		#collisions
		self.collision_sprites = pygame.sprite.Group()
		self.collision_terre = pygame.sprite.Group()

		#trees
		self.tree_sprites = pygame.sprite.Group()
		self.healthy_trees = pygame.sprite.Group()
		self.fire_trees = pygame.sprite.Group()
		self.dead_trees = pygame.sprite.Group()

		#fight
		self.fight = pygame.sprite.Group()

		#lac
		self.lac = pygame.sprite.Group()
		#self.pok_fire = pygame.sprite.Group()

		self.pokemon_collide = None

		#Création feu de forêt
		self.feu = Fire(self.all_sprites, self.collision_sprites, self.tree_sprites, self.healthy_trees, self.fire_trees, self.dead_trees)
		self.setup()

		#Sky
		self.sky = Sky()
		self.rain = Rain(self.all_sprites)
		#self.raining = random_proba(0)

		#Temperature
		self.temperature = Temperature()

		#lac
		self.lacs = Lac(self.all_sprites, self.lac)

	def add_to_list(self, pokemon):
		Pokemon.pokemon_list.append(pokemon)
		if pokemon.type == 'fire':
			Pokemon.pok_fire_list.append(pokemon)
		elif pokemon.type == 'water':
			Pokemon.pok_water_list.append(pokemon)
		elif pokemon.type == 'poison':
			Pokemon.pok_poison_list.append(pokemon)

	#création de la carte
	def setup(self):
		#Map upload
		tmx_data = self.tmx_data
		map_width, map_height = pygame.image.load('../data/tmx/map.png').get_size()

		#LAYERS
		for layer in ['Ground']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, LAYERS['ground'])

		for layer in ['Water']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites, self.lac], LAYERS['water'])

		for layer in ['Hills']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, LAYERS['hills'])

		for layer in ['Path']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, LAYERS['path'])

		for layer in ['Ilot']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, LAYERS['ilot'])

		for layer in ['Barrières']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, LAYERS['barrières'])

		#cases de collision
		for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
			Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_terre, LAYERS['collisions'])

		#OBJETS
		#Arbres
		for obj in tmx_data.get_layer_by_name('Trees'):
			Tree((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.tree_sprites, self.healthy_trees], LAYERS['trees'],  obj.name)

		for obj in tmx_data.get_layer_by_name('FireTree'):
			FireTree((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.tree_sprites, self.fire_trees], LAYERS['trees'], obj.name)

		for obj in tmx_data.get_layer_by_name('Arbres coupés'):
			CutTree((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.tree_sprites, self.dead_trees], LAYERS['trees'], obj.name)

		#Fleurs
		for obj in tmx_data.get_layer_by_name('Flowers'):
			Flower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites], LAYERS['vegetation'], obj.name)

		#Champignons
		for obj in tmx_data.get_layer_by_name('Mushrooms'):
			Mushroom((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites], LAYERS['vegetation'], obj.name)

		#Plantations
		for obj in tmx_data.get_layer_by_name('Plantations'):
			Plantation((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites], LAYERS['vegetation'], obj.name)

		#Decoration eau
		for obj in tmx_data.get_layer_by_name('Deco Water'):
			Decoration((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites], LAYERS['vegetation'], obj.name)

		#Batiments
		for obj in tmx_data.get_layer_by_name('Batiments'):
			if obj.image!= None:
				Batiment((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites], LAYERS['main'], obj.name)

		#joueur
		for obj in tmx_data.get_layer_by_name('Player'):
			if obj.name == 'Start':
				self.player = Player((obj.x,obj.y), self.all_sprites, [self.collision_sprites, self.collision_terre], LAYERS['main'])

		#pokemons
		#ajout aléatoire
		"""for i in range(50):
			self.add_to_list(PokemonFire((randint(0,map_width),randint(0,map_height)), self.all_sprites, [self.collision_sprites, self.collision_terre]))
			self.add_to_list(PokemonWater((randint(0,map_width),randint(0,map_height)), self.all_sprites, [self.collision_sprites]))
			self.add_to_list(PokemonPoison((randint(0,map_width),randint(0,map_height)), self.all_sprites, [self.collision_sprites]))"""


		self.add_to_list(PokemonFire((5375,2461), self.all_sprites, [self.collision_sprites, self.collision_terre]))
		self.add_to_list(PokemonFire((5375,2461), self.all_sprites, [self.collision_sprites, self.collision_terre]))
		self.add_to_list(PokemonFire((5343,2465), self.all_sprites, [self.collision_sprites, self.collision_terre]))
		self.add_to_list(PokemonFire((5343,2465), self.all_sprites, [self.collision_sprites, self.collision_terre]))
		self.add_to_list(PokemonFire((5327,2448), self.all_sprites, [self.collision_sprites, self.collision_terre]))
		self.add_to_list(PokemonFire((5327,2448), self.all_sprites, [self.collision_sprites, self.collision_terre]))
		self.add_to_list(PokemonWater((4411,2237), self.all_sprites, [self.collision_sprites]))
		self.add_to_list(PokemonWater((4411,2237), self.all_sprites, [self.collision_sprites]))
		self.add_to_list(PokemonWater((4223,2228), self.all_sprites, [self.collision_sprites]))
		self.add_to_list(PokemonWater((4223,2228), self.all_sprites, [self.collision_sprites]))
		self.add_to_list(PokemonWater((4364,2254), self.all_sprites, [self.collision_sprites]))
		self.add_to_list(PokemonWater((4364,2254), self.all_sprites, [self.collision_sprites, self.collision_terre]))
		self.add_to_list(PokemonPoison((4815,2283), self.all_sprites, [self.collision_sprites, self.collision_terre]))
		self.add_to_list(PokemonPoison((4815,2283), self.all_sprites, [self.collision_sprites, self.collision_terre]))
		self.add_to_list(PokemonPoison((4908,2471), self.all_sprites, [self.collision_sprites, self.collision_terre]))
		self.add_to_list(PokemonPoison((4908,2471), self.all_sprites, [self.collision_sprites, self.collision_terre]))
		self.add_to_list(PokemonPoison((4668,2631), self.all_sprites, [self.collision_sprites, self.collision_terre]))
		self.add_to_list(PokemonPoison((4668,2631), self.all_sprites, [self.collision_sprites, self.collision_terre]))


		Generic(
			pos = (0,0),
			surf = pygame.image.load('../data/tmx/map.png').convert_alpha(),
			groups = self.all_sprites,
			z = LAYERS['ground'])

		#interface combat
		self.EC = EC(self)
		self.fight.add(self.EC)

	def combat(self):
		if self.EC.enm == None :
				self.EC = EC(self)
				self.fight.add(self.EC)
		else :
			self.fight.draw(self.display_surface)
			self.EC.update()

			#si le pokemon ennemi est mort
			if self.EC.end_enm :
				for poke in Pokemon.pokemon_list :
					if self.player.rect.colliderect(poke.rect) and self.EC.poke_id == poke.id:
						poke.hp = 0
						poke.death()
				self.player.collision_pokemon = 0

				if Pokemon.pokemon_list:
					#self.life_pika = self.EC.player.life
					self.EC = EC(self)
					self.fight.add(self.EC)
					self.EC.end_enm = False

			#si le pokemon joueur est mort
			elif self.EC.end_pl :
				self.player.collision_pokemon = 0
				if Pokemon.pokemon_list:
					self.EC = EC(self)
					self.fight.add(self.EC)
					self.EC.end_pl = False

	def player_alive(self):
		if self.player.pv <= 0:
			return True
		else:
			return False

	def run(self,dt):
		#rain
		self.rain.setRain()
		if self.rain.raining:
			self.rain.update()
			self.lacs.Flood()
		else:
			self.lacs.Drought()

		#collision avec un pokemon
		#if self.player.collision_pokemon != 0:
		#self.combat()

		#else:
		#pas de collision
		self.all_sprites.player_center(self.player)

		#mise à jour du player
		self.player_alive()
		self.player.lose_pv(self.fire_trees)

		#feu de forêt
		self.feu.forest(self.rain.raining)
		for pk in Pokemon.pok_fire_list:
			pk.fire_tree(self.all_sprites, self.collision_sprites, self.tree_sprites, self.healthy_trees, self.fire_trees)

		#cycle jour/nuit
		self.sky.display(dt)
		self.sky.setTime()

		#temperature
		self.temperature.display(len(self.healthy_trees), self.display_surface)

		#mise à jour de tous les sprites
		self.all_sprites.update(dt)

		#chasse des pokémons poison
		for poke in Pokemon.pok_poison_list:
			poke.hunt(dt)

		#contamination et fuite
		for poke in Pokemon.pok_fire_list:
			poke.contamination()
			poke.escape(dt)
		for poke in Pokemon.pok_water_list:
			poke.contamination()
			poke.escape(dt)

		#Graphes (au choix)
		#Pokemon.afficher(self)
		#self.feu.afficher()
