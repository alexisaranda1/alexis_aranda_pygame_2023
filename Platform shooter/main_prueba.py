import pygame
from player import Player
from enemy import Enemy
from nivel import *
from constantes import *
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')
# set framerate
clock = pygame.time.Clock()

#carga de rutas
image_dict = {
    "image_dict_playe": {
        "idle": "img/player/Idle/{0}.png",
        "run": "img/player/Run/{0}.png",
        "jum": "img/player/Jump/{0}.png"
    },
    "image_dict_enemi": {
        "idle": "img/enemy/Idle/{0}.png",
        "run": "img/enemy/Run/{0}.png",
        "jum": "img/enemy/Jump/{0}.png",
        "death": "img/enemy/Death/{0}.png"
    }
}

# backgroup configuration
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()
bg_scroll = 0

def draw_bg():
	screen.fill(BG)
	width = sky_img.get_width()
        
	for x in range(5):
		screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
		screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
		screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
		screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))


level = 2
world = World()
world.load_level_data(level)
player_1, enemi_1 = world.process_data(image_dict)


dx = 0
dy = 0
run = True
while run:
    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player_1.handle_key_events(event)

    draw_bg()
    enemi_1.update(bg_scroll, player_1)  # Actualizar al enemigo antes de dibujarlo
    player_1.update()
    world.check_collision(player_1)

    player_1.draw(screen)
    enemi_1.draw(screen)  # Dibujar al enemigo después de actualizarlo
    world.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)
