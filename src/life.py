import pygame
from settings import *

BAR_LENGTH = 50
BAR_HEIGHT = 10

class Life(pygame.sprite.Sprite):

	global BAR_LENGTH
	global BAR_HEIGHT
		
	def draw_life_bar(self, surf, x, y):
		self.outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
		self.fill_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
		pygame.draw.rect(surf, Colors.GREEN, self.fill_rect)
		pygame.draw.rect(surf, Colors.WHITE, self.outline_rect, 2)

	def update_life_bar(self, surf, x, y, global_pv, pv):
		bg_color = surf.get_at((x, y))
		self.fill_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
		pygame.draw.rect(surf, bg_color, self.fill_rect)
		if pv < 0:
			pv = 0
		pv = pv * 50 / global_pv
		self.fill = (pv/BAR_LENGTH)*BAR_LENGTH
		self.fill_rect = pygame.Rect(x, y, self.fill, BAR_HEIGHT)
		pygame.draw.rect(surf, Colors.GREEN, self.fill_rect)
		self.outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
		pygame.draw.rect(surf, Colors.WHITE, self.outline_rect, 2)
