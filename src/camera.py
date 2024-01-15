import pygame 
from settings import *

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def player_center(self, player):
		"""
			Cette caméra est centrée sur les déplacements du player
		"""
		#offset définis par les coordonnées centrales du player
		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2 
		self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

		#mise à jour de la caméra
		#lorsque le player va en bas, la map va en haut (pareil pour le sud, est, et ouest)
		for layer in LAYERS.values():
			for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)
	
	def zoom(self, screen, map, zoom_level):
		scaled_map_surf = pygame.Surface((int(map.width * map.tilewidth * zoom_level),
                                         int(map.height * map.tileheight * zoom_level)))
		#map.render(scaled_map_surf)
		screen.blit(scaled_map_surf, (0,0))
		pygame.display.update()
