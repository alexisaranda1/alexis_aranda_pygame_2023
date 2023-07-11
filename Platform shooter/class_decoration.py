import pygame 
from constantes import *


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TAMAÑO_BLOQUES // 2, y + (TAMAÑO_BLOQUES - self.image.get_height()))

    def update(self, screen_scroll):
        self.rect.x += int(screen_scroll)

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)
