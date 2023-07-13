import pygame
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()  # Llama al constructor de la clase padre (Sprite)
        self.image = image
        self.rect = self.image.get_rect()
        self.posicion_inicial = x
        self.rect.x = x
        self.rect.y = y

    def update(self, pantalla, desplazamiento_pantalla):
        self.rect.x += desplazamiento_pantalla
        self.draw(pantalla)

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)



