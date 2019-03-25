#!/usr/bin/env python

'''
Created on 03/06/2010

@author: cadi and matheus
'''

#Classe Superficie com os parametros da Superficie
class Superficie():
    
    def __init__(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None
        self.j = None
        self.k = None

#Classe Camera com os parametros da Camera
class Camera():
    
    def __init__(self):
        self.posicao_x = None
        self.posicao_y = None
        self.posicao_z = None
        self.orientacao_x = None
        self.orientacao_y = None
        self.orientacao_z = None
        self.distancia_focal = None
        self.altura = None
        self.largura = None
        self.pixel_x = None
        self.pixel_y = None

#Classe Iluminacao com os parametros da Iluminacao
class Iluminacao():

    def __init__(self):
        self.posicao_x = None
        self.posicao_y = None
        self.posicao_z = None
        self.cor_r = None
        self.cor_g = None
        self.cor_b = None
        self.cor_ambiente_r = None
        self.cor_ambiente_g = None
        self.cor_ambiente_b = None
        self.difusao_r = None
        self.difusao_g = None
        self.difusao_b = None
        self.especular_r = None
        self.especular_g = None
        self.especular_b = None
        self.ambiente_r = None
        self.ambiente_g = None
        self.ambiente_b = None
        self.expoente_especular = None

#Classe Configuracao que le os parametros da Interface
class Configuration():

    #Construtor da classe
    def __init__(self, config):
        self.gui = config
        self.__load_param()
    
    #Metodo que faz a leitura dos parametros da Interface
    def __load_param(self):
        
        #Le parametros ILUMINACAO
        #Fonte de Luz
        self.iluminacao = Iluminacao()
        self.iluminacao.posicao_x = float(self.gui.get_widget("spinbutton_iluminacao_posicao_x").get_text())
        self.iluminacao.posicao_y = float(self.gui.get_widget("spinbutton_iluminacao_posicao_y").get_text())
        self.iluminacao.posicao_z = float(self.gui.get_widget("spinbutton_iluminacao_posicao_z").get_text())
        
        self.iluminacao.cor_r = float(self.gui.get_widget("spinbutton_iluminacao_cor_r").get_text())
        self.iluminacao.cor_g = float(self.gui.get_widget("spinbutton_iluminacao_cor_g").get_text())
        self.iluminacao.cor_b = float(self.gui.get_widget("spinbutton_iluminacao_cor_b").get_text())
        
        self.iluminacao.cor_ambiente_r = float(self.gui.get_widget("spinbutton_iluminacao_cor_ambiente_r").get_text())
        self.iluminacao.cor_ambiente_g = float(self.gui.get_widget("spinbutton_iluminacao_cor_ambiente_g").get_text())
        self.iluminacao.cor_ambiente_b = float(self.gui.get_widget("spinbutton_iluminacao_cor_ambiente_b").get_text())
        
        #Coeficientes
        temp = self.gui.get_widget("spinbutton_iluminacao_difusao_r").get_text()
        temp = temp.replace(',', '.')
        self.iluminacao.difusao_r = float(temp)
        
        temp = self.gui.get_widget("spinbutton_iluminacao_difusao_g").get_text()
        temp = temp.replace(',', '.')
        self.iluminacao.difusao_g = float(temp)
        
        temp = self.gui.get_widget("spinbutton_iluminacao_difusao_b").get_text()
        temp = temp.replace(',', '.')
        self.iluminacao.difusao_b = float(temp)
        
        temp = self.gui.get_widget("spinbutton_iluminacao_especular_r").get_text()
        temp = temp.replace(',', '.')
        self.iluminacao.especular_r = float(temp)
        
        temp = self.gui.get_widget("spinbutton_iluminacao_especular_g").get_text()
        temp = temp.replace(',', '.')
        self.iluminacao.especular_g = float(temp)
        
        temp = self.gui.get_widget("spinbutton_iluminacao_especular_b").get_text()
        temp = temp.replace(',', '.')
        self.iluminacao.especular_b = float(temp)
        
        temp = self.gui.get_widget("spinbutton_iluminacao_ambiente_r").get_text()
        temp = temp.replace(',', '.')
        self.iluminacao.ambiente_r = float(temp)
        
        temp = self.gui.get_widget("spinbutton_iluminacao_ambiente_g").get_text()
        temp = temp.replace(',', '.')
        self.iluminacao.ambiente_g = float(temp)
        
        temp = self.gui.get_widget("spinbutton_iluminacao_ambiente_b").get_text()
        temp = temp.replace(',', '.')
        self.iluminacao.ambiente_b = float(temp)
        
        temp = self.gui.get_widget("spinbutton_iluminacao_expoente_especular").get_text()
        temp = temp.replace(',', '.')
        self.iluminacao.expoente_especular = float(temp)
        
        #Le parametros da CAMERA
        #Exterior
        self.camera = Camera()
        self.camera.posicao_x = float(self.gui.get_widget("spinbutton_camera_posicao_x").get_text())
        self.camera.posicao_y = float(self.gui.get_widget("spinbutton_camera_posicao_y").get_text())
        self.camera.posicao_z = float(self.gui.get_widget("spinbutton_camera_posicao_z").get_text())

        self.camera.orientacao_x = float(self.gui.get_widget("spinbutton_camera_orientacao_x").get_text())
        self.camera.orientacao_y = float(self.gui.get_widget("spinbutton_camera_orientacao_y").get_text())
        self.camera.orientacao_z = float(self.gui.get_widget("spinbutton_camera_orientacao_z").get_text())
        
        #Interior
        self.camera.largura = float(self.gui.get_widget("spinbutton_camera_largura").get_text())
        self.camera.altura = float(self.gui.get_widget("spinbutton_camera_altura").get_text())
        self.camera.pixel_x = float(self.gui.get_widget("spinbutton_camera_pixel_x").get_text())
        self.camera.pixel_y = float(self.gui.get_widget("spinbutton_camera_pixel_y").get_text())
        self.camera.distancia_focal = float(self.gui.get_widget("spinbutton_camera_distancia_focal").get_text())

        #Le parametros da SUPERFICIE
        self.superficie = Superficie()
        self.superficie.a = float(self.gui.get_widget("spinbutton_superficie_a").get_text())
        self.superficie.b = float(self.gui.get_widget("spinbutton_superficie_b").get_text())
        self.superficie.c = float(self.gui.get_widget("spinbutton_superficie_c").get_text())
        self.superficie.d = float(self.gui.get_widget("spinbutton_superficie_d").get_text())
        self.superficie.e = float(self.gui.get_widget("spinbutton_superficie_e").get_text())
        self.superficie.f = float(self.gui.get_widget("spinbutton_superficie_f").get_text())
        self.superficie.g = float(self.gui.get_widget("spinbutton_superficie_g").get_text())
        self.superficie.h = float(self.gui.get_widget("spinbutton_superficie_h").get_text())
        self.superficie.j = float(self.gui.get_widget("spinbutton_superficie_j").get_text())
        self.superficie.k = float(self.gui.get_widget("spinbutton_superficie_k").get_text())
