import pygame
from settings import *
from pokemon import Pokemon
from support import Txt
import random
from os import path

#classe pour initialiser les pokémons lors du combat (affichage + paramètres)
class Entity(pygame.sprite.Sprite):
	def __init__(self,l, name, img, x, y, life):
		pygame.sprite.Sprite.__init__(self)

		img_folder = "../data/graphics/combat"
		self.pok = Pokemon
		self.image = pygame.Surface((150, 150))
		self.pok_img = pygame.image.load(path.join(img_folder, img)).convert_alpha()
		self.pok_img = pygame.transform.scale(self.pok_img, (150, 150))
		self.rect = self.image.get_rect()
		self.image.blit(self.pok_img, self.rect)
		self.image.set_colorkey(Colors.BLACK)

		self.rect.x = x
		self.rect.centery = y
		self.life = life
		self.largeur = l
		self.name = name



#classe pour initialiser les attaques du pokémon joueur (affichage + paramètres)
class Attaque(pygame.sprite.Sprite):
	def __init__(self,surf, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.name_pok = 'Pikachu'
		self.attribut = Pokemon
		self.text = Txt()
		self.text.draw_text(surf, self.attribut.attaque[self.name_pok][0], 70, x, y, Colors.BLACK)
		self.cadre = pygame.Rect.copy(self.text.text_rect)
		pygame.draw.rect(surf, Colors.BLACK, self.cadre, 2)
		self.text.draw_text(surf, self.attribut.attaque[self.name_pok][1], 70, x - 300, y, Colors.BLACK)
		self.cadre1 = pygame.Rect.copy(self.text.text_rect)
		pygame.draw.rect(surf, Colors.BLACK, self.cadre1, 2)