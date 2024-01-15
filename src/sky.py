import pygame
from random import randint, choice
from support import import_folder
from sprites import Generic
from settings import *

class Sky:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_color = [255, 255, 255]
        self.start_color1 = [255, 255, 255]
        self.end_color = (38, 101, 189)
        self.is_night = False

    def display(self, dt):
        if self.is_night:
            # Transition from night to day
            for index, value in enumerate(self.start_color):
                if self.start_color1[index] > value:
                    self.start_color[index] += 2 * dt
            if (self.start_color[0]>253 and self.start_color[1]>253  and self.start_color[2]>253):
                self.is_night = False
        else:
            # Transition from day to night
            for index, value in enumerate(self.end_color):
                if self.start_color[index] > value:
                    self.start_color[index] -= 2 * dt
            if (self.start_color[0]<=self.end_color[0] and self.start_color[1]<=self.end_color[1] and self.start_color[2]<=self.end_color[2]):
                self.is_night = True

        self.full_surface.fill(self.start_color)
        self.display_surface.blit(self.full_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def setTime(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.start_color = [255, 255, 255]
        if keys[pygame.K_n]:
            self.start_color = [38, 101, 189]

class Drop(Generic):
    def __init__(self, pos, surf, moving,  groups, z):
        #setup
        super().__init__(pos, surf, groups, z)
        self.lifetime = 20
        self.start_time = pygame.time.get_ticks()

        #déplacement
        self.moving = moving
        if self.moving == True:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2,4)
            self.speed = randint(200,250)
    
    def update(self, dt):
        #mouvement
        if self.moving:
            self.pos += self.direction * self.speed * dt 
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        #timer
        #Ce timer est détruit lorsque le lifetime se termine
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill() 

        
class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites 
        self.rain_drops = import_folder('../data/graphics/rain/drops')
        self.rain_floor = import_folder('../data/graphics/rain/floor')
        self.floor_w, self.floor_h = pygame.image.load('../data/tmx/map.png').get_size()
        self.raining = False

    def create_floor(self):
        Drop(pos = (randint(0, self.floor_w), randint(0, self.floor_h)), 
             surf = choice(self.rain_floor), 
             moving = False,  
             groups = self.all_sprites, 
             z = LAYERS['rain floor'])

    def create_drops(self):
        Drop(pos = (randint(0, self.floor_w), randint(0, self.floor_h)), 
             surf = choice(self.rain_drops), 
             moving = True,  
             groups = self.all_sprites, 
             z = LAYERS['rain drops'])
    
    def update(self):
        for i in range(1,400):
            self.create_drops()
        for i in range(1,100):
            self.create_floor()

    def setRain(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            self.raining = True
        if keys[pygame.K_t]:
            self.raining = False

        