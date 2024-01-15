import os
import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups, z = LAYERS['main']):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = z
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class Tree(Generic):
	def __init__(self, pos, surf, groups, layer, name):
		super().__init__(pos, surf, groups, layer)
		self.name = name

class FireTree(Generic):
	def __init__(self, pos, surf, groups, layer, name):
		super().__init__(pos, surf, groups, layer)
		self.name = name

class CutTree(Generic):
	def __init__(self, pos, surf, groups, layer, name):
		super().__init__(pos, surf, groups, layer)
		self.name = name

class Flower(Generic):
	def __init__(self, pos, surf, groups, layer, name):
		super().__init__(pos, surf, groups, layer)
		self.name = name

class Mushroom(Generic):
	def __init__(self, pos, surf, groups, layer, name):
		super().__init__(pos, surf, groups, layer)
		self.name = name

class Plantation(Generic):
	def __init__(self, pos, surf, groups, layer, name):
		super().__init__(pos, surf, groups, layer)
		self.name = name

class Decoration(Generic):
	def __init__(self, pos, surf, groups, layer, name):
		super().__init__(pos, surf, groups, layer)
		self.name = name

class Batiment(Generic):
	def __init__(self, pos, surf, groups, layer, name):
		super().__init__(pos, surf, groups, layer)
		self.name = name
