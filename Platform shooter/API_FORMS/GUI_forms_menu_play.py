import pygame
from pygame.locals import*

from API_FORMS.GUI_button_image import*
from API_FORMS.GUI_form import*
from API_FORMS.GUI_form_contenedor_nivel import*
from Manejador_niveles import Manejador_niveles
from banderas import*


class FormMenuPlay(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border, active, path_image):
        super().__init__(screen, x, y, w, h, color_background, color_border,active)

        self.manejador_niveles = Manejador_niveles(self._master)
        aux_image = pygame.image.load(path_image)
        aux_image = pygame.transform.scale(aux_image,(w,h))
        self._slave = aux_image

        self._btn_level_1 = Button_Image(screen=self._slave,x=100,y=140,master_x=x,master_y=y,
                                         w=100,h=150,onclick=self.entrar_nivel_1,
                                         onclick_param="nivel_uno",path_image=r"images\gui\set_gui_01\Pixel_Border\Buttons\1.png")

        self._btn_level_2 = Button_Image(screen=self._slave,x=260,y=140,master_x=x,master_y=y,
                                         w=100,h=150,onclick=self.entrar_nivel_2,
                                         onclick_param="nivel_dos",path_image=r"images\gui\set_gui_01\Pixel_Border\Buttons\2.png")
        
        self._btn_level_3 = Button_Image(screen=self._slave,x=190,y=300,master_x=x,master_y=y,
                                         w=100,h=150,onclick=self.entrar_nivel_3,
                                         onclick_param="nivel_tres",path_image=r"images\gui\set_gui_01\Pixel_Border\Buttons\3.png")
        
        self._btn_home = Button_Image(screen=self._slave,x=400,y=400,master_x=x,master_y=y,
                                         w=50,h=50,onclick=self.btn_home_click,
                                         onclick_param="",path_image=r"API_FORMS\Moneda_vida\2.png")
    
    
        self.lista_widgets.append(self._btn_level_1)
        self.lista_widgets.append(self._btn_level_2)
        self.lista_widgets.append(self._btn_level_3)
        self.lista_widgets.append(self._btn_home)
       
    def on(self,parametro):
        print("hola", parametro)

    def update(self, lista_eventos):
        if self.verificar_dialog_result():
            for widget in self.lista_widgets:
                widget.update(lista_eventos)
            self.draw()
        else:
            self.hijo.update(lista_eventos)

    def entrar_nivel_1(self,nombre_nivel):
        print("entre nivel")
        nivel = self.manejador_niveles.get_nivel_1()
        form_contenedor_nivel = FormContenedorNivel(self._master,nivel)
        self.show_dialog(form_contenedor_nivel)

    def entrar_nivel_2(self,nombre_nivel):
        bandera_1 = leer_bandera("bandera_1")
        if bandera_1[0] == "true":
            print("entre nivel 2")
            nivel_2 = self.manejador_niveles.get_nivel_2()
            form_contenedor_nivel = FormContenedorNivel(self._master,nivel_2)
            self.show_dialog(form_contenedor_nivel)

    def entrar_nivel_3(self,nombre_nivel):
        bandera_1 = leer_bandera("bandera_1")
        bandera_2 = leer_bandera("bandera_2")
        if bandera_1[0] == "true" and bandera_2[0] == "true" :
            print("entre nivel 3")
            nivel_3 = self.manejador_niveles.get_nivel_3()
            form_contenedor_nivel = FormContenedorNivel(self._master,nivel_3)
            self.show_dialog(form_contenedor_nivel)

    def btn_home_click(self,param):
        print("sali del nivel ")
        self.end_dialog()

        