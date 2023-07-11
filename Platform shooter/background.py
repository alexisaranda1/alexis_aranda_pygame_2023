import pygame
from constantes import *


class Background:
    def __init__(self, background_image):
        self.image = pygame.image.load(background_image).convert_alpha()
        #self.image = pygame.transform.scale(self.image, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.posicion_x = 0
        self.factor_velocidad = FACTOR_VELOCIDAD
        self.pantalla= pygame.display.get_surface()

    def draw(self,pantalla ,screen_scroll):
        self.move_background(screen_scroll)
        pantalla.fill(VERDE)
        pantalla.blit(self.image, (self.posicion_x, 0))

    def update_scroll(self,nivel_actual):
        screen_scroll = 0
        dx = nivel_actual.player.vel_x  # Actualizar dx con la velocidad horizontal del jugador
        if nivel_actual.player.rect.right > ANCHO_PANTALLA - LIMITE_DESPLAZAMIENTO and self.posicion_x < (nivel_actual.nivel_len * TAMAÑO_BLOQUES) - ANCHO_PANTALLA:
            screen_scroll = -dx
         
        elif nivel_actual.player.rect.left < LIMITE_DESPLAZAMIENTO and self.posicion_x > abs(dx):
            screen_scroll = -dx 
        return screen_scroll 
    
    def move_background(self, screen_scroll):
        self.factor_velocidad = screen_scroll *FACTOR_VELOCIDAD
        self.posicion_x +=self.factor_velocidad

