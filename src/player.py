import os
import pygame
from settings import *
from pokemon import Pokemon
from support import *
import math

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, all_sprites, collision_sprites, layer):
		super().__init__(all_sprites)
		#listes
		self.all_sprites = all_sprites
		self.collision_sprites = collision_sprites

		#initialisation des paramètres
		self.health = 'healthy'
		self.pv = 100
		
		#image
		self.import_assets()
		self.status = 'down_stop'
		self.frame_index = 0
		self.cpt = 0
		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		self.z = layer

		#paramètres des déplacements
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.speed = 300
		
		#collision
		self.hitbox = self.rect.copy().inflate((-100,-50))
		self.collision_pokemon = 0
		self.poke = None

	def import_assets(self):
		self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_stop':[],'left_stop':[],'up_stop':[],'down_stop':[]}

		for animation in self.animations.keys():
			full_path = '../data/graphics/character/' + animation
			self.animations[animation] = import_folder(full_path)

	#animation du joueur (marche)
	def animate(self,dt):
		self.frame_index += 6 * dt
		if self.frame_index >= len(self.animations[self.status]):
			self.frame_index = 0

		self.image = self.animations[self.status][int(self.frame_index)]	

	#déplacements avec flèches de direction
	def input(self):
		keys = pygame.key.get_pressed()
		self.direction.y = 0
		self.direction.x = 0
		self.cpt = 0

		if keys[pygame.K_UP]:
			self.cpt +=1
			self.direction.y = -1
			self.status = 'up'
		elif keys[pygame.K_DOWN]:
			self.direction.y = 1
			self.status = 'down'
		elif keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.status = 'right'
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.status = 'left'

	def get_status(self):
		
		#personnage immobile
		if self.direction.magnitude() == 0:
			self.status = self.status.split('_')[0] + '_stop'

	def collision(self, direction):
		for group in self.collision_sprites:
			for sprite in group.sprites():
				if hasattr(sprite, 'hitbox'):
					if sprite.hitbox.colliderect(self.hitbox):
						if direction == 'horizontal':
							if self.direction.x > 0: #à droite
								self.hitbox.right = sprite.hitbox.left
							if self.direction.x < 0: #à gauche
								self.hitbox.left = sprite.hitbox.right
							self.rect.centerx = self.hitbox.centerx
							self.pos.x = self.hitbox.centerx

						if direction == 'vertical':
							if self.direction.y > 0: #vers le bas
								self.hitbox.bottom = sprite.hitbox.top
							if self.direction.y < 0: #vers le haut
								self.hitbox.top = sprite.hitbox.bottom
							self.rect.centery = self.hitbox.centery
							self.pos.y = self.hitbox.centery

	#mofication de la position du joueur
	def move(self,dt):
 		
 		#normaliser le vecteur pour avoir un vecteur unitaire
		if self.direction.magnitude() > 0:
			self.direction = self.direction.normalize()

		#déplacement horizontal
		self.pos.x += self.direction.x * self.speed * dt
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		self.collision('horizontal')

		#déplacement vertical
		self.pos.y += self.direction.y * self.speed * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collision('vertical')
	
	#contamination par les pokémons poison (avec possibilités de mort ou guérison)
	def contamination(self):
		for pokemon in pokemon_list:
			if(Pokemon.type == 'poison'):
				distance = math.sqrt((Pokemon.pos.x - self.pos.x)**2 + (Pokemon.pos.y - self.pos.y)**2)
				if distance <= 2:
					if(self.health == 'healthy'):
						self.health = 'infected'
						self.pv -= 4
						if(random() > p_infection):
							self.health = 'cured'

	#Perte de vie à côté d'un feu de forêt
	def lose_pv(self, fire_trees):
		for fire_tree in fire_trees:
			if(math.sqrt((fire_tree.rect.x - self.rect.x)**2 + (fire_tree.rect.y - self.rect.y)**2) < DISTANCE_FEU):
				self.pv -= 4

	def poke_coll(self):
		for poke in Pokemon.pokemon_list :
			if self.rect.colliderect(poke.rect):
				self.collision_pokemon = 1
				self.poke = poke
				
	#mort du joueur
	def death(self):
		if(self.pv == 0):
			self.type = 'dead'
			self.all_sprites.remove(self)

	def update(self, dt):
		self.input()
		self.get_status()
		self.move(dt)
		self.animate(dt)
		self.poke_coll()
		self.death()
		
	
