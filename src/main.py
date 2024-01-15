import pygame, sys
from settings import *
from level import Level


class Game:
	#initialisation 
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption('Pallet Town')
		self.clock = pygame.time.Clock()
		self.level = Level()
		self.game_over = False
		self.fight_mode = False
		
	#écran de démarrage
	def start_screen(self):
		bg = pygame.image.load('../data/graphics/accueil/starter_2.png')
		self.screen.blit(bg,(0,0))
		pygame.display.flip()
		self.wait_for_key()
		self.debut = pygame.time.get_ticks()
	
	def end_game(self):
		#image
		bg = pygame.image.load('../data/graphics/end/gameover.png')
		self.screen.blit(bg,(0,0))
		pygame.display.flip()

		#attente d'une touche avant de disparaitre
		pygame.event.wait()
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.KEYUP:
				pygame.quit()
				sys.exit()

	#cliquer pour lancer	
	def wait_for_key(self):
		pygame.event.wait()
		waiting = True
		while waiting:
			self.clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				if event.type == pygame.KEYUP:
					waiting = False
					
	#lancement
	def run(self):
		self.start_screen()
		while not self.game_over:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			if self.level.player_alive():
				self.game_over = True
			
			if self.game_over == True:
				self.end_game()

			dt = self.clock.tick() / 1000
			self.level.run(dt)
			pygame.display.update()


if __name__ == '__main__':
	game = Game()
	game.run()

