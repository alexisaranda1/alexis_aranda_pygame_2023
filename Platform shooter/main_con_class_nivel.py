import pygame,sys
from pygame.locals import *
from API_FORMS.GUI_formulario_prueba import*



# PANTALLA
W, H = 1900,900
#TAMAÑO_PANTALLA = (W,H)
TAMAÑO_PANTALLA = ()

# INICIAMOS PYGAME
pygame.init()
pygame.display.set_caption("Platform shooter")

# ---- ICONO ----
icono = pygame.image.load(r"img/icons/ammo_box.png")
pygame.display.set_icon(icono)

RELOG = pygame.time.Clock()
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA))

# Crea el formulario con los valores calculados
form_prueba = FormPrueba(PANTALLA, FROM_X, FROM_Y, FROM_ANCHO, FROM_ALTO, (70, 6, 6), (171, 1, 1), 5, True)

pausa = pygame.image.load(r"img\start_btn.png")
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
            if evento.key == pygame.K_c:
                is_paused = not is_paused
            
    PANTALLA.fill("Black")
    
    if not is_paused:
        form_prueba.update(lista_eventos)
    else:
        # Mostrar mensaje de pausa
        PANTALLA.blit(pausa, (700,200))
    
    pygame.display.update()


