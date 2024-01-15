import pygame

class Temperature:
    def __init__(self):
        self.image_fond = pygame.image.load("../data/graphics/temperature/a.png")
        self.font = pygame.font.Font(None, 22)

    def display(self, nb, display):
        tmp = str(round(1/nb*10000,1)) + "°C"
        texte = self.font.render(tmp, True, "black")

        display.blit(self.image_fond, (9, 9))
        display.blit(texte, (14, 19))
