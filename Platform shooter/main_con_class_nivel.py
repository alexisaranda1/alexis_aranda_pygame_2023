import pygame,sys
from pygame.locals import *
from API_FORMS.GUI_formulario_prueba import*

# PANTALLA
TAMAÑO_PANTALLA = ()

# INICIAMOS PYGAME
pygame.init()
pygame.display.set_caption("Platform shooter")

# ---- ICONO ----
icono = pygame.image.load(r"img/icons/ammo_box.png")
pygame.display.set_icon(icono)

RELOG = pygame.time.Clock()
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA))
imagen_fondo = pygame.image.load(r"menu_1\fondo_menu.jpg")

imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))

form_prueba = FormPrueba(PANTALLA, 0, 0, ANCHO_PANTALLA, ALTO_PANTALLA, imagen_fondo, (171, 1, 1))

pausa = pygame.image.load(r"menu_1\8-bitpause.jpg")
pausa = pygame.transform.scale(pausa,(500,500))

is_paused = False
flag = True
while flag:
    RELOG.tick(FPS)
    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif evento.type == pygame.KEYDOWN:
           if evento.key == pygame.K_ESCAPE:
                is_paused = not is_paused
            
    PANTALLA.fill("Black")
    
    if not is_paused:
        form_prueba.update(lista_eventos)
    else:
        PANTALLA.blit(pausa, (200,100))   

    pygame.display.update()


