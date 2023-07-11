import pygame
from constantes import *
class HealthBar():
    def __init__(self, x, y, salud, salud_maxima):
        self.x = x
        self.y = y
        self.salud = salud
        self.salud_maxima = salud_maxima

    def draw(self, salud, pantalla):
        self.salud = salud
        proporcion_salud = self.salud / self.salud_maxima
        pygame.draw.rect(pantalla, NEGRO, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(pantalla, ROJO, (self.x, self.y, 150, 20))
        pygame.draw.rect(pantalla, VERDE, (self.x, self.y, 150 * proporcion_salud, 20))
