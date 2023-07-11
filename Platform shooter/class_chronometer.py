import pygame

BLANCO = "White"
NEGRO = "Black"

class Chronometer:
    def __init__(self, tiempo_inicial) -> None:
        self.tiempo_desendente = tiempo_inicial
        self.minutos = 0
        self.fuente = pygame.font.SysFont("Forte", 40)
        self.tiempo_actual = pygame.time.get_ticks()
        self.detenido = False
        self.color = BLANCO

    def actualizar(self):
        if self.detenido == False:
            tiempo_transcurrido = pygame.time.get_ticks() - self.tiempo_actual
            if tiempo_transcurrido >= 1000:
                self.tiempo_actual = pygame.time.get_ticks()
                self.tiempo_desendente -= 1  # Resta 1 segundo en lugar de sumar 1


    def mostrar_tiempo(self, pantalla):
        cronometro = self.fuente.render(f"0{self.minutos} : {str(self.tiempo_desendente).zfill(2)}", False, self.color)
        pantalla.blit(cronometro, (870, 6))

    def get_tiempo(self)-> int:
        return self.tiempo_desendente
