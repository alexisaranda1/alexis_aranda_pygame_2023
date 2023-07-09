import pygame
from pygame.locals import*
from API_FORMS.GUI_form import*
from API_FORMS.GUI_button_image import*

from API_FORMS.GUI_form_fin import*
from Manejador_niveles import*


class FormContenedorNivel(Form):
    def __init__(self,pantalla:pygame.Surface,nivel):
        super().__init__(pantalla,0,0,pantalla.get_width(),pantalla.get_height(),color_background="Black")
        self._slave = pantalla
        nivel._slave = self._slave
        self.nivel = nivel

        self._btn_home = Button_Image(screen=self._slave,
                                      master_x=self._x,
                                      master_y=self._y,
                                      x=self._w - 100,
                                      y=self._h - 100,
                                      w=50,
                                      h=50,
                                      onclick=self.btn_home_click,
                                      onclick_param="",
                                      path_image=r"API_FORMS\Moneda_vida\2.png")
        
        dic = [{"clave": "pepe","punot":"cdcd"}]


        self.form_jugar = FormFin(self._master,690,205,500,550,(220,0,220),
                                 "white",True,r"API_FORMS\Menu\0.png",
                                 dic,100,10,10)
        
        self.lista_widgets.append(self._btn_home)

        
    def update(self,lista_eventos):
        self.nivel.update(lista_eventos)     
        for widget in self.lista_widgets:
            widget.update(lista_eventos)
        self.draw()
    def draw(self):
        self.nivel.draw(self._slave)
        #if self.nivel.vidas_jugador == 0:

            # print("murio") 
            # self.show_dialog(self.form_jugar)
            # self.end_dialog()
         #   pass
        # if self.nivel.bandera_1 == True:
        #     print("TRueeeeeee")    
            

    def btn_home_click(self,param):
        self.end_dialog()