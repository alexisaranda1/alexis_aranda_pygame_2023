import pygame
from constantes import *
class Background:
    def __init__(self, background_image):
        self.image = pygame.image.load(background_image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_position = 0
        self.target_position = 0
        self.speed_factor = SPEED_FACTOR  # Ajusta este valor para controlar la suavidad del movimiento del fondo

    def draw(self, player):
        window = pygame.display.get_surface()

        self.update_target_position(player)

        self.move()

        relative_background_position = self.background_position % self.image.get_rect().width
        window.blit(self.image, (relative_background_position - self.image.get_rect().width, 0))
        if relative_background_position < SCREEN_WIDTH:
            window.blit(self.image, (relative_background_position, 0))

    def update_target_position(self, player):
        target_x = player.rect.x - SCREEN_WIDTH // 2  # Posición objetivo centrada en el jugador
        self.target_position = target_x
        self.background_position = target_x  # Establecer la posición inicial del fondo igual a la posición inicial del jugador


    def move(self):
        displacement = self.target_position - self.background_position
        self.background_position -= displacement * self.speed_factor
    def get_movement(self):
        return self.background_position