import pygame
from player import Player
from enemy import Enemy
from nivel import *
from constantes import *
from background import Background
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
background_image = "img/background/fondo_0.png"
background = Background(background_image)
bg_scroll = 0
#sonidos 
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.02)
shot_fx = pygame.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.02)
grenade_fx = pygame.mixer.Sound('audio/grenade.wav')
grenade_fx.set_volume(0.02)

#img
#bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
#grenade
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()

enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

level = 1
world = World()
world.load_level_data(level)
player_1, enemi_1 = world.process_data(image_dict)
enemy_group.add(enemi_1)

dx = 0
dy = 0
run = True

while run: 
    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player_1.handle_key_events(event,bullet_group,shot_fx)
    player_1.update()
    screen_scroll = background.update_scroll(player_1, world)
    background.draw(screen_scroll)
    player_1.update_position(screen_scroll)
    enemi_1.update(screen_scroll, player_1,bullet_group,shot_fx)  # Actualizar al enemigo antes de dibujarlo

    world.check_collision(player_1)
    world.check_collision(enemi_1)
    bullet_group.update(world, player_1, enemy_group, bullet_group,)  # Actualiza las balas con los argumentos requeridos
    bullet_group.draw(screen) 
    player_1.draw(screen) 
    enemi_1.draw(screen)  # Dibujar al enemigo después de actualizarlo

    # Dibujar las plataformas
    world.draw(screen,screen_scroll)
    pygame.display.flip()

    clock.tick(30)







