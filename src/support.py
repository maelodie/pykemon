import os
import pygame
from os import walk
from random import random

#liste des fichiers d'un dossier (à partir de son chemin)
def import_folder(path):
	surface_list = []

	for _, __, img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

#fonction permettant d'écrire et afficher le contenu
class Txt(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font_name = pygame.font.match_font('pokemon')

    def draw_text(self, surface, text, size, x, y, colors):
        self.font = pygame.font.Font(self.font_name, size)
        self.text_surface = self.font.render(text, True, colors)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.midleft = (x, y)
        surface.blit(self.text_surface, self.text_rect)
    
    def erase_text(self, surface, x, y, w, h):
        bg_color = surface.get_at((x, y))
        surface.fill(bg_color, (x, y, w, h))

def random_proba(proba):
	return random() <= proba
