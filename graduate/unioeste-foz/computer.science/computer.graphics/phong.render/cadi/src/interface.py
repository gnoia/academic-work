#!/usr/bin/env python

'''
Created on 03/06/2010

@author: cadi
'''
import pygtk
pygtk.require('2.0')
import gtk.glade
from configuration import Configuration
from render import Render


#Classe que implementa a Interface Princiapl
class Gui():

    #Construtor da classe
    def __init__(self):
        #Nome do arquivo Glade
        self.__glade_file = "renderizador.glade"
        gui = gtk.glade.XML(self.__glade_file)
        self.gui = gui
        
        main_window = gui.get_widget("janela_principal")
        main_window.connect("destroy", gtk.main_quit)
        
        button_renderizar = gui.get_widget("button_renderizar")
        button_renderizar.connect("clicked", self.button_renderizar_clicked)
        
        button_sair = gui.get_widget("button_sair")
        button_sair.connect("clicked", gtk.main_quit)
        
        main_window.show_all()
        self.loop()


    #Acao do botao Renderizar
    def button_renderizar_clicked(self, *args):
        configuration = Configuration(self.gui)
        render = Render(configuration, self)
        render.renderiza()
    
    
    #Metodo da GTK
    def loop(self):
        gtk.main()
