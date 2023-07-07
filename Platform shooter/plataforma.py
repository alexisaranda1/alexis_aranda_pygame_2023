from constantes import SPEED_FACTOR
# class Platform:
#     def __init__(self, x, y, image):
#         self.image = image
#         self.rect = self.image.get_rect()
#         self.initial_position_x = x
#         self.rect.x = x
#         self.rect.y = y

#     def update(self, screen, background_position):
#         self.move(background_position)
#         self.draw(screen)

#     def move(self, background_position):
#         displacement = background_position - self.initial_position_x
#         self.rect.x = self.initial_position_x + displacement * SPEED_FACTOR

#     def draw(self, screen):
#         screen.blit(self.image, self.rect)

class Platform:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.initial_position_x = x
        self.rect.x = x
        self.rect.y = y

    def update(self, screen, screen_scroll):
        self.rect.x += screen_scroll
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

