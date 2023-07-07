import pygame
from constantes import *
from nivel import World

class Background:
    def __init__(self, background_image):
        self.image = pygame.image.load(background_image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_position = 0
        self.speed_factor = SPEED_FACTOR

    def draw(self, screen_scroll):
        self.move_background(screen_scroll)
        screen = pygame.display.get_surface()
        screen.fill(BG)
        screen.blit(self.image, (self.background_position, 0))

    def update_scroll(self, player, world):
        screen_scroll = 0
        dx = player.vel_x  # Actualizar dx con la velocidad horizontal del jugador

        if player.rect.right > SCREEN_WIDTH - SCROLL_THRESH and self.background_position < (world.level_length * TILE_SIZE) - SCREEN_WIDTH:
            screen_scroll = -dx
        elif player.rect.left < SCROLL_THRESH and self.background_position > abs(dx):
            screen_scroll = -dx

        return screen_scroll

    def move_background(self, screen_scroll):
        self.speed_factor = screen_scroll * SPEED_FACTOR
        self.background_position +=self.speed_factor


    # def update_scroll(self, player, world):
    #     screen_scroll = 0
    #     dx = player.vel_x  # Actualizar dx con la velocidad horizontal del jugador
        
    #     if player.rect.right > SCREEN_WIDTH - SCROLL_THRESH and self.background_position < (world.level_length * TILE_SIZE) - SCREEN_WIDTH:
    #         player.rect.x -= dx
    #         screen_scroll = -dx
    #     elif player.rect.left < SCROLL_THRESH and self.background_position > abs(dx):
    #         player.rect.x -= dx
    #         screen_scroll = -dx
        
    #     return screen_scroll