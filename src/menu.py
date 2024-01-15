import pygame
from settings import *
from support import Txt
from entity import Entity, Attaque
from life import Life
import random
from os import path
import math

class EC(pygame.sprite.Sprite):
	def __init__(self, level):
		pygame.sprite.Sprite.__init__(self)
		self.level = level

		#initialisation de la fenêtre de combat
		self.image = pygame.Surface((700,350))
		bg_combat = pygame.image.load('../data/graphics/combat/bg_combat.png')
		self.image.blit(bg_combat,(0,0))

		#cadre noir
		self.rect = self.image.get_rect()
		self.r = pygame.Rect.copy(self.rect)
		pygame.draw.rect(self.image, Colors.BLACK, self.r, 2)

		#positionné au centre
		self.rect.centerx = SCREEN_WIDTH/2
		self.rect.centery = SCREEN_HEIGHT/2

		#création du menu Attaque/Capture
		self.menu = Menu(self.image.get_width() / 2, self.image.get_height())

		#création du pokémon du joueur(largeur/nom/img/x/y/pv)
		self.player = Entity(50, 'Pikachu', 'pikachu.png', 32, 140, 50)
		#print('ec:'+str(self.player.life))

		#création du pokémon ennemi
		if self.level.player.collision_pokemon == 1:
			self.enm = Entity(self.level.player.poke.hp, self.level.player.poke.name, self.level.player.poke.name + '.png', 530, 140, self.level.player.poke.hp)
			self.poke_id = self.level.player.poke.id
		else:
			self.enm = None
				
		#self.enm = Entity(ennemi.hp, ennemi.name, ennemi.name + '.png', 530, 140, ennemi.hp)
		
		#création de l'objet Life pour dessiner les barres de vie
		self.life = Life()

		#initialisation des paramètres du combat
		if self.enm != None :
			self.selct_att = False
			self.selct_base = True
			self.choose_att = True
			self.att = 0
			self.start_tick = 1000000
			self.end_tick = 1000000
			self.kill_enm_tick = 1000000
			self.kill_pl_tick = 1000000
			self.enms = pygame.sprite.Group()
			self.enms.add(self.enm)
			self.end_enm = False
			self.end_pl = False
			self.suite_enm_0 = False
			self.enm_0 = True
			self.suite_player_0 = False
			self.player_0 = True
			self.type_att = 0

	
	def update(self):
		if self.enm != None :
			pygame.sprite.Sprite.update(self)
			keys_pressed = pygame.key.get_pressed()
			self.draw()
				
			#sélection de la case de gauche Attaque
			if keys_pressed[pygame.K_LEFT] and self.selct_base:
				pygame.draw.rect(self.menu.image, Colors.RED, self.menu.cadre, 2)
				pygame.draw.rect(self.menu.image, Colors.BLACK, self.menu.cadre1, 2)
				self.selct_att = True
				
			#sélection de la case de droite Capture
			if keys_pressed[pygame.K_RIGHT] and self.selct_base:
				pygame.draw.rect(self.menu.image, Colors.RED, self.menu.cadre1, 2)
				pygame.draw.rect(self.menu.image, Colors.BLACK, self.menu.cadre, 2)
				self.selct_att = False
				
			#si sélection Attaque + Touche Entrée : attaque du pokémon joueur
			if keys_pressed[pygame.K_RETURN] and self.selct_att == True:
				self.selct_base = False
				self.menu.image.fill(Colors.WHITE)
				pygame.draw.rect(self.menu.image, Colors.BLACK, self.menu.r, 2)
				self.attaque = Attaque(self.menu.image, self.menu.x+15, self.menu.y)
				
			#sélection de l'attaque de droite
			if keys_pressed[pygame.K_RIGHT] and self.selct_att == True:
				pygame.draw.rect(self.menu.image, Colors.RED, self.attaque.cadre, 2)
				pygame.draw.rect(self.menu.image, Colors.BLACK, self.attaque.cadre1, 2)
				self.att = 1
				self.type_att = 2
				
			#sélection de l'attaque de gauche
			elif keys_pressed[pygame.K_LEFT] and self.selct_att == True and self.selct_base == False:
				pygame.draw.rect(self.menu.image, Colors.RED, self.attaque.cadre1, 2)
				pygame.draw.rect(self.menu.image, Colors.BLACK, self.attaque.cadre, 2)
				self.att = 1
				self.type_att = 1

			#lancement de l'attaque avec la touche Entrée
			if keys_pressed[pygame.K_RETURN] and self.att == 1:
				if self.type_att == 1 :
					if random.random()>0.02:
						self.dmg = random.randint(5,10)
					else:
						self.dmg = 0
				if self.type_att == 2 :
					if random.random()>0.02:
						self.dmg = random.randint(10,20)
					else:
						self.dmg = 0
				self.menu.image.fill(Colors.WHITE)
				pygame.draw.rect(self.menu.image, Colors.BLACK, self.menu.r, 2)
			
				#dommages sur le pokemon ennemi
				self.enm.life = self.enm.life - self.dmg
				if self.enm.life < 0:
					self.enm.life = 0
				self.selct_att = False
				self.att = 0
				self.type_att = 0
				self.start_tick = pygame.time.get_ticks()
				#affichage dégats si l'ennemi n'est pas mort
				if self.enm.life > 0:
					if self.dmg != 0:
						self.menu.text.draw_text(self.menu.image, "Vous avez infligé " + str(self.dmg) + " points de dégâts !", 35, 120, self.menu.image.get_height() / 2, Colors.BLACK)
					else:
						self.menu.text.draw_text(self.menu.image, "Vous avez raté votre attaque, pas de dégâts !", 35, 120, self.menu.image.get_height() / 2, Colors.BLACK)
				
			#attaque de l'ennemi sur le pokémon joueur
			if (pygame.time.get_ticks()-self.start_tick)/1000>2 and self.enm.life > 0:
				if random.random()>0.02:
					self.enm_dmg = random.randint(5,21)
				else:
					self.enm_dmg = 0
				#dommage sur le pokémon joueur
				self.player.life = self.player.life - self.enm_dmg
				if self.player.life < 0:
					self.player.life = 0
				self.start_tick = 1000000
				#affichage dégats si le pokémon joueur n'est pas mort
				if self.player.life > 0:
					self.menu.image.fill(Colors.WHITE)
					pygame.draw.rect(self.menu.image, Colors.BLACK, self.menu.r, 2)
					if self.enm_dmg != 0:
						self.menu.text.draw_text(self.menu.image, "Vous avez subi " + str(self.enm_dmg) + " points de dégâts !", 35, 120, self.menu.image.get_height() / 2, Colors.BLACK)
					else:
						self.menu.text.draw_text(self.menu.image, "Vous n'avez subi pas points de dégâts !", 35, 120, self.menu.image.get_height() / 2, Colors.BLACK)
					self.end_tick = pygame.time.get_ticks()



			if (pygame.time.get_ticks()-self.end_tick)/1000>2:
				self.menu.image.fill(Colors.WHITE)
				pygame.draw.rect(self.menu.image, Colors.BLACK, self.menu.r, 2)
				self.menu.draw()
				self.selct_base = True
				self.end_tick = 1000000
				
			#mort de l'ennemi à la dernière attaque (dégats + KO)
			if self.enm.life <= 0 and self.enm_0:
				self.menu.text.draw_text(self.menu.image, "Vous avez infligé " + str(self.dmg)+ " points de dégats." , 35, 120, self.menu.image.get_height() / 2, Colors.BLACK)
				self.menu.text.draw_text(self.menu.image, self.enm.name + " est KO !", 35, 230, (self.menu.image.get_height() / 2)+30, Colors.BLACK)
				self.suite_enm_0 = True
				self.enm_0 = False

			#mofication des paramètres de fin de combat si ennemi meurt
			if self.suite_enm_0:
				self.suite_enm_0 = False
				self.kill_enm_tick = pygame.time.get_ticks()

			if (pygame.time.get_ticks()-self.kill_enm_tick)/1000 > 3:
				self.enm.kill()
				self.end_enm = True
				self.kill()
				self.kill_enm_tick = 100000



			#mort du pokémon joueur à la dernière attaque (dégats + KO)
			if self.player.life <= 0 and self.player_0:
				self.menu.image.fill(Colors.WHITE)
				pygame.draw.rect(self.menu.image, Colors.BLACK, self.menu.r, 2)
				self.menu.text.draw_text(self.menu.image, "Vous avez subi " + str(self.enm_dmg)+ " points de dégats." , 35, 120, self.menu.image.get_height() / 2, Colors.BLACK)
				self.menu.text.draw_text(self.menu.image, self.player.name + " est KO !", 35, 230, (self.menu.image.get_height() / 2)+30, Colors.BLACK)
				self.suite_player_0 = True
				self.player_0 = False

			#mofication des paramètres de fin de combat si pokémon joueur meurt
			if self.suite_player_0:
				self.suite_player_0 = False
				self.kill_pl_tick = pygame.time.get_ticks()

			if (pygame.time.get_ticks()-self.kill_pl_tick)/1000 > 3:
				self.end_pl = True
				self.kill_pl_tick = 100000
				self.kill()



	#affichage des paramètres écrits du combat (noms, pv, barres de vie)
	def draw(self):
		if self.enm != None :
			pygame.draw.rect(self.image, Colors.BLACK, self.r, 2)
			#paramètres du pokemon joueur
			if self.player.life == self.player.largeur:
				#barre de vie
				self.life.draw_life_bar(self.image, self.player.rect.x, self.player.rect.y - 15)
				#nom
				self.menu.text.draw_text(self.image, self.player.name, 30, self.player.rect.x, self.player.rect.y - 45, Colors.WHITE)
				#pv
				self.menu.text.erase_text(self.image, self.player.rect.x, self.player.rect.y - 32, 42, 15)
				self.menu.text.draw_text(self.image, str(self.player.life) + " / " + str(self.player.largeur), 20, self.player.rect.x, self.player.rect.y - 25, Colors.WHITE)

			if self.player.life >= 0 and self.player.life < self.player.largeur:
				#nom
				self.menu.text.draw_text(self.image, self.player.name, 30, self.player.rect.x, self.player.rect.y - 45, Colors.WHITE)
				#màj barre de vie
				self.life.update_life_bar(self.image, self.player.rect.x, self.player.rect.y - 15, self.player.largeur, self.player.life)
				#màj pv
				self.menu.text.erase_text(self.image, self.player.rect.x, self.player.rect.y - 32, 42, 15)
				self.menu.text.draw_text(self.image, str(self.player.life) + " / " + str(self.player.largeur), 20, self.player.rect.x, self.player.rect.y - 25, Colors.WHITE)
		
			#affichage pokemon joueur	
			self.image.blit(self.player.image, self.player.rect)

			#paramètres du pokemon ennemi	
			if self.enm.life == self.enm.largeur:
				#barre de vie
				self.life.draw_life_bar(self.image, self.enm.rect.x, self.enm.rect.y - 15)
				#nom
				self.menu.text.draw_text(self.image, self.enm.name, 30, self.enm.rect.x, self.enm.rect.y - 45, Colors.WHITE)
				#pv
				self.menu.text.erase_text(self.image, self.enm.rect.x, self.enm.rect.y - 31, 42, 14)
				self.menu.text.draw_text(self.image, str(self.enm.life) + " / " + str(self.enm.largeur), 20, self.enm.rect.x, self.enm.rect.y - 25, Colors.WHITE)

			if self.enm.life >= 0 and self.enm.life < self.enm.largeur:
				#màj barre de vie
				self.life.update_life_bar(self.image, self.enm.rect.x, self.enm.rect.y - 15, self.enm.largeur, self.enm.life)
				#màj pv
				self.menu.text.erase_text(self.image, self.enm.rect.x, self.enm.rect.y - 31, 42, 14)
				self.menu.text.draw_text(self.image, str(self.enm.life) + " / " + str(self.enm.largeur), 20, self.enm.rect.x, self.enm.rect.y - 25, Colors.WHITE)
		
			self.enms.draw(self.image)
			self.image.blit(self.menu.image, self.menu.rect)
			


class Menu(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.text = Txt()
				
		#paramètres du menu Attaque/Capture
		self.image = pygame.Surface((700, 125))
		self.image.fill(Colors.WHITE)
		self.rect = self.image.get_rect()
		self.r = pygame.Rect.copy(self.rect)
		pygame.draw.rect(self.image, Colors.BLACK, self.r, 2)
		self.rect.centerx = x
		self.rect.bottom = y

		self.x = self.image.get_rect().centerx
		self.y = self.image.get_rect().centery
		self.draw()
		
	#cadres et écriture des cases Attaque/Capture
	def draw(self):
		self.text.draw_text(self.image, "ATTAQUE", 70, self.x - 300, self.y, Colors.BLACK)
		self.cadre = pygame.Rect.copy(self.text.text_rect)
		self.text.draw_text(self.image, "CAPTURE", 70, self.x + 50, self.y, Colors.BLACK)
		self.cadre1 = pygame.Rect.copy(self.text.text_rect)
		pygame.draw.rect(self.image, Colors.BLACK, self.cadre, 2)
		pygame.draw.rect(self.image, Colors.BLACK, self.cadre1, 2)






