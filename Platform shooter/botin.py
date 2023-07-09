
import pygame
from constantes import *
class ItemBox(pygame.sprite.Sprite):
    item_boxes = {
        'Health': pygame.image.load('img/tile/19.png'),
        'Ammo': pygame.image.load('img/tile/17.png'),
        'Exit': pygame.image.load('img/tile/20.png')
    }
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = ItemBox.item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TAMAÑO_BLOQUES // 2, y + (TAMAÑO_BLOQUES - self.image.get_height()))

    def update(self, screen_scroll, player):
        self.rect.x += screen_scroll

        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Health':
                player.salud += 10  # Increase player's health by 10 (adjust the value as needed)
            elif self.item_type == 'Ammo':
                player.municion += 10 
            elif self.item_type == 'Exit':
                
                pass
            self.kill()


    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)

