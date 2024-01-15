from pygame.math import Vector2
import pygame
#screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64
FPS = 60

#map
LAYERS = {
    'collisions': 0,
	'ground': 1,
	'water': 2,
    'rain floor': 3,
	'hills': 4,
	'barrières': 5,
	'ilot': 6,
	'path': 6,
	'main': 7,
	'trees': 8,
    'vegetation': 9,
    'rain drops': 10,
}

#couleurs
class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GREENBG = (20, 140, 60)


#ecosystem settings
#distance arbre en feu
DISTANCE_FEU = 110

#probabilités
#feu de foret
P_BRULE = 0.1
P_POUSSE = 0.001
P_CUT = 0.05
P_INCENDIE = 0.5

#pluie et inondation
P_RAINING = 0.05
P_INONDATION = 0.01
P_SECHERESSE = 0.001

#reproduction pokémon + infection
P_REPRODUCTION = 0.002
P_INFECTION = 0.001
