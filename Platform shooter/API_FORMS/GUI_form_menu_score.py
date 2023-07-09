import pygame
from pygame.locals import*

from API_FORMS.GUI_form import*
from API_FORMS.GUI_label import*
from API_FORMS.GUI_button_image import*

class FormMenuScore(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border, active,path_image,score,margen_y,margen_x,espacio):
        super().__init__(screen, x, y, w, h, color_background, color_border,active)

        aux_image = pygame.image.load(path_image)
        aux_image = pygame.transform.scale(aux_image,(w,h))

        self._slave = aux_image
        self._score = score

        self._margen_y = margen_y
        
        lbl_jugador = Label(self._slave, x=margen_x + 10, y=20 , w= w/2-margen_x-10, h=50, text="Jugador", font="Verdana", font_size=30, font_color="White", path_image=r"Segundo-Parcail-Laboratorio\Menu\6.png")
        lbl_puntaje = Label(self._slave, x=margen_x + 10 + w/2-margen_x-10, y=20 , w= w/2-margen_x-10, h=50, text="Puntaje", font="Verdana", font_size=30, font_color="White", path_image=r"Segundo-Parcail-Laboratorio\Menu\6.png")
        
        self.lista_widgets.append(lbl_jugador)
        self.lista_widgets.append(lbl_puntaje)

        pos_inicial_y = margen_y

        for j in self._score:
            pos_inicial_x = margen_x
            for n,s in j.items():
                cadena = ""
                cadena = f"{s}"
                jugador = Label(self._slave,pos_inicial_x,pos_inicial_y,w/2-margen_x,100,cadena,"verdana",30,"White",r"Segundo-Parcail-Laboratorio\Menu\0.png")
                self.lista_widgets.append(jugador)
                pos_inicial_x += w/2 - margen_x #corremos la x para excribir el proximo Label

            pos_inicial_y += 100 + espacio #corremos la y  para excribir el proximo Label

        self._btn_home = Button_Image(screen=self._slave, x=w-70, y=h-70, master_x=x, master_y=y, w=50, h=50,
                                       color_background=(255,0,255), onclick=self._bnt_home_click,#Metodos_Estaticos.entrar_nivel_1,
                                       onclick_param="",#{"Clave1": "valor1","Clave2":"valor2"},
                                       text="", font="Verdana", font_size=15, font_color=(0,255,0), path_image=r"Segundo-Parcail-Laboratorio\Moneda_vida\2.png")
        self.lista_widgets.append(self._btn_home)


    def _bnt_home_click(self,param):
        self.end_dialog()

    def update(self, lista_eventos):
        if self.active:
            for wid in self.lista_widgets:
                wid.update(lista_eventos)
            self.draw()