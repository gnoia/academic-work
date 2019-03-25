#!/usr/bin/env python

'''
Created on 03/06/2010

@author: cadi and matheus
'''
from ImageDraw import ImageDraw
from math import *
import Image

#constantes maximo e minimo de cinza
MinGray = 0
MaxGray = 255


#Classe que faz as operacoes do Renderizador
class Render():

    #Construtor da classe
    def __init__(self, config, interface):
        self.parametros = config
        self.interface = interface
        #Inicia os valores de maior e menor para a normalizacao dos pixeis
        self.Maior = 0
        self.Menor = 1



    #Metodo que inicializa a matriz Imagem
    def inicializa_matriz_imagem(self):
        self.matriz_imagem = []
        
        for i in range(int (self.parametros.camera.largura)):
            self.matriz_imagem.append([])
            for j in range(int (self.parametros.camera.altura)):
                self.matriz_imagem[i].append([])
                self.matriz_imagem[i][j].append([])
                self.matriz_imagem[i][j].append([])
                self.matriz_imagem[i][j].append([])
                
                

    #Metodo que inicializa a matriz Rotacao
    def inicializa_matriz_rotacao(self):
        self.matriz_rotacao = []
        
        self.parametros.camera.orientacao_x = (self.parametros.camera.orientacao_x * pi) /180
        self.parametros.camera.orientacao_y = (self.parametros.camera.orientacao_y * pi) /180
        self.parametros.camera.orientacao_z = (self.parametros.camera.orientacao_z * pi) /180
       
        #Obtem o valor dos cossenos
        cos_orientacao_x = cos(self.parametros.camera.orientacao_x)
        cos_orientacao_y = cos(self.parametros.camera.orientacao_y)
        cos_orientacao_z = cos(self.parametros.camera.orientacao_z)
        #Obtem o valor dos senos
        sen_orientacao_x = sin(self.parametros.camera.orientacao_x)
        sen_orientacao_y = sin(self.parametros.camera.orientacao_y)
        sen_orientacao_z = sin(self.parametros.camera.orientacao_z)
        
        self.matriz_rotacao.append([cos_orientacao_y * cos_orientacao_z,  
                                    cos_orientacao_y * sen_orientacao_z, 
                                    -sen_orientacao_y])
        
        self.matriz_rotacao.append([cos_orientacao_z * sen_orientacao_x * sen_orientacao_y - cos_orientacao_x * sen_orientacao_z,
                                    sen_orientacao_x * sen_orientacao_y * sen_orientacao_z + cos_orientacao_x * cos_orientacao_z, 
                                    cos_orientacao_y * sen_orientacao_x])
        
        self.matriz_rotacao.append([cos_orientacao_x * sen_orientacao_y * cos_orientacao_z + sen_orientacao_x * sen_orientacao_z,
                                    cos_orientacao_x * sen_orientacao_y * sen_orientacao_z - sen_orientacao_x * cos_orientacao_z,
                                    cos_orientacao_x * cos_orientacao_y])
        

        
    #Metodo que executa o algoritmo phonger
    def algoritmo_phonger(self):
        #Variaveis de conversao do sistema de tela para o sistema espaco-imagem (pag 7)
        meia_largura = self.parametros.camera.largura / 2
        meia_altura = self.parametros.camera.altura / 2
        x_lambda = 1 / self.parametros.camera.pixel_x
        y_lambda = 1 / self.parametros.camera.pixel_y
        
        for i in range(int(self.parametros.camera.largura)):
            for j in range(int(self.parametros.camera.altura)):
                
                #Conversao do sistema de tela para o sistema espaco-imagem (pag 7)
                x = x_lambda * (i - meia_largura)
                y = - (y_lambda * (j - meia_altura))
                
                #Calculo dos valores de A e B (pag 4)
                a = self.matriz_rotacao[0][0] * x + self.matriz_rotacao[1][0] * y + self.matriz_rotacao[2][0] * self.parametros.camera.distancia_focal
                a = a / (self.matriz_rotacao[0][2] * x + self.matriz_rotacao[1][2] * y + self.matriz_rotacao[2][2] * self.parametros.camera.distancia_focal)
                
                b = self.matriz_rotacao[0][1] * x + self.matriz_rotacao[1][1] * y + self.matriz_rotacao[2][1] * self.parametros.camera.distancia_focal
                b = b / (self.matriz_rotacao[0][2] * x + self.matriz_rotacao[1][2] * y + self.matriz_rotacao[2][2] * self.parametros.camera.distancia_focal)
             
                #Calculo de z1 e z2 (pag 3)
                denominador = self.__calcula_denominador(a, b)
                
                if denominador != 0:
                    
                    numerador = self.__calcula_numerador_parte_2(a, b)
                    
                    if numerador > -1:
                    
                        z1 = z2 = self.__calcula_numerador_parte_1(a, b)
                        
                        z1 = 0.5 * (z1 + 2 * numerador) / denominador
                        z2 = 0.5 * (z2 - 2 * numerador) / denominador
                        
                        #Calculo da intersecao do raio oriundo da camera com a superficie dada (pag 3)
                        intersecao_x1 = self.parametros.camera.posicao_x + (z1 - self.parametros.camera.posicao_z) * a
                        intersecao_y1 = self.parametros.camera.posicao_y + (z1 - self.parametros.camera.posicao_z) * b
                        
                        intersecao_x2 = self.parametros.camera.posicao_x + (z2 - self.parametros.camera.posicao_z) * a
                        intersecao_y2 = self.parametros.camera.posicao_y + (z2 - self.parametros.camera.posicao_z) * b
                        
                        #Calculo da distancia entre o CP e o ponto (x2, y2, z2) ou (x2, y2, z2) (pag 5)
                        distancia1 = sqrt(pow(self.parametros.camera.posicao_x - intersecao_x1, 2) + pow(self.parametros.camera.posicao_y - intersecao_y1, 2) + pow(self.parametros.camera.posicao_z - z1, 2))
                        distancia2 = sqrt(pow(self.parametros.camera.posicao_x - intersecao_x2, 2) + pow(self.parametros.camera.posicao_y - intersecao_y2, 2) + pow(self.parametros.camera.posicao_z - z2, 2))
                        
                        #print intersecao_x1, intersecao_y1, distancia1, a, b
                        
                        vetor = []
                        #Decide sobre qual o menor
                        if distancia1 < distancia2:
                            vetor.append(intersecao_x1)
                            vetor.append(intersecao_y1)
                            vetor.append(z1)
                        else:
                            vetor.append(intersecao_x2)
                            vetor.append(intersecao_y2)
                            vetor.append(z2)

                        #Calcula vetor Normal (pag 2) 
                        vetor_normal = []
                        vetor_normal.append(2 * self.parametros.superficie.a * vetor[0] + 2 * self.parametros.superficie.d * vetor[1] + 2 * self.parametros.superficie.f * vetor[2] + 2 * self.parametros.superficie.g)
                        vetor_normal.append(2 * self.parametros.superficie.b * vetor[1] + 2 * self.parametros.superficie.d * vetor[0] + 2 * self.parametros.superficie.e * vetor[2] + 2 * self.parametros.superficie.h)
                        vetor_normal.append(2 * self.parametros.superficie.c * vetor[2] + 2 * self.parametros.superficie.e * vetor[1] + 2 * self.parametros.superficie.f * vetor[0] + 2 * self.parametros.superficie.j)
                        
                        #Calcula vetor Direcao da Fonte de Luz (pag 6)
                        vetor_fonte_luz = []
                        vetor_fonte_luz.append(self.parametros.iluminacao.posicao_x - vetor[0])
                        vetor_fonte_luz.append(self.parametros.iluminacao.posicao_y - vetor[1])
                        vetor_fonte_luz.append(self.parametros.iluminacao.posicao_z - vetor[2])
                        
                        #Calcula vetor Direcao do Observador (pag 6)
                        vetor_observador = []
                        vetor_observador.append(self.parametros.camera.posicao_x - vetor[0])
                        vetor_observador.append(self.parametros.camera.posicao_y - vetor[1])
                        vetor_observador.append(self.parametros.camera.posicao_z - vetor[2])
                        
                        #Calcula vetor Reflexao (pag 6)
                        produto_escalar = self.__calcula_produto_escalar(vetor_normal, vetor_fonte_luz)
                        vetor_reflexao = []
                        vetor_reflexao.append(2 * produto_escalar * vetor_normal[0] - vetor_fonte_luz[0])
                        vetor_reflexao.append(2 * produto_escalar * vetor_normal[1] - vetor_fonte_luz[1])
                        vetor_reflexao.append(2 * produto_escalar * vetor_normal[2] - vetor_fonte_luz[2])
                        
                        #Calculo do angulo teta
                        cosseno_teta = self.__calcula_cosseno(vetor_fonte_luz, vetor_normal) 
                        
                        #Calculo do angulo alfa
                        cosseno_alfa = self.__calcula_cosseno(vetor_reflexao, vetor_observador)
                        
                        #Calcula o angulo elevado necessario para o calculo da iluminacao
                        angulo_elevado = pow(cosseno_alfa, self.parametros.iluminacao.expoente_especular)
                        
                        #Aplicando o modelo de Iluminacao de Phong para a banda R, G e B (pag 07)
                        self.matriz_imagem[i][j][0] = (self.parametros.iluminacao.cor_ambiente_r * self.parametros.iluminacao.ambiente_r
                            + self.parametros.iluminacao.cor_r
                            * (self.parametros.iluminacao.difusao_r * cosseno_teta 
                               + self.parametros.iluminacao.especular_r * angulo_elevado))
                        
                        self.matriz_imagem[i][j][1] = (self.parametros.iluminacao.cor_ambiente_g * self.parametros.iluminacao.ambiente_g
                            + self.parametros.iluminacao.cor_g 
                            * (self.parametros.iluminacao.difusao_g * cosseno_teta
                               + self.parametros.iluminacao.especular_g * angulo_elevado))
                        
                        self.matriz_imagem[i][j][2] = (self.parametros.iluminacao.cor_ambiente_b * self.parametros.iluminacao.ambiente_b
                            + self.parametros.iluminacao.cor_b 
                            * (self.parametros.iluminacao.difusao_b * cosseno_teta
                               + self.parametros.iluminacao.especular_b * angulo_elevado))
                        
                        
                        self.Menor = min(self.matriz_imagem[i][j][0], self.matriz_imagem[i][j][1], self.matriz_imagem[i][j][2], self.Menor)
                        self.Maior = max(self.matriz_imagem[i][j][0], self.matriz_imagem[i][j][1], self.matriz_imagem[i][j][2], self.Maior)
                    
                    # Caso numerador_parte_2 < 0
                    else:  
                        self.matriz_imagem[i][j][0] = 0
                        self.matriz_imagem[i][j][1] = 0
                        self.matriz_imagem[i][j][2] = 0
                # Caso divisor == 0
                else:
                    self.matriz_imagem[i][j][0] = 0
                    self.matriz_imagem[i][j][1] = 0
                    self.matriz_imagem[i][j][2] = 0



    #Metodo que calcula o cosseno
    def __calcula_cosseno(self, vetor_1, vetor_2):
        produto_escalar = self.__calcula_produto_escalar(vetor_1, vetor_2)
        if produto_escalar < 0:
            return 0
         
        modulo = (self.__calcula_modulo(vetor_1) * self.__calcula_modulo(vetor_2))
        if modulo == 0:
            return 0
        
        resultado = produto_escalar / modulo
        if resultado < 0:
            return 0
        else:
            return resultado


        
    #Metodo que calcula o numerdador parte 1 dos valores de z
    def __calcula_numerador_parte_1(self, a, b):
        return  (- 2 * self.parametros.superficie.d * self.parametros.camera.posicao_x * b - 2 * self.parametros.superficie.b * self.parametros.camera.posicao_y * b 
          - 2 * self.parametros.superficie.j 
          + 2 * self.parametros.superficie.a * a * a * self.parametros.camera.posicao_z
          - 2 * self.parametros.superficie.a * self.parametros.camera.posicao_x * a 
          - 2 * self.parametros.superficie.h * b 
          + 2 * self.parametros.superficie.f * a * self.parametros.camera.posicao_z
          - 2 * self.parametros.superficie.e * self.parametros.camera.posicao_y
          - 2 * self.parametros.superficie.g * a 
          + 2 * self.parametros.superficie.e * b * self.parametros.camera.posicao_z
          + 2 * self.parametros.superficie.b * b * b * self.parametros.camera.posicao_z
          - 2 * self.parametros.superficie.f * self.parametros.camera.posicao_x
          - 2 * self.parametros.superficie.d * a * self.parametros.camera.posicao_y)



    #Metodo que calcula o numerador parte 2 dos valores de z
    def __calcula_numerador_parte_2(self, a, b):
        result = (- 2 * self.parametros.superficie.c * self.parametros.superficie.g * self.parametros.camera.posicao_x
             + self.parametros.superficie.d * self.parametros.superficie.d * self.parametros.camera.posicao_x * self.parametros.camera.posicao_x * b * b
             + 2 * self.parametros.superficie.j * self.parametros.superficie.h * b 
             - 2 * self.parametros.superficie.e * b * self.parametros.superficie.k 
             + self.parametros.superficie.j * self.parametros.superficie.j
             - self.parametros.superficie.c * self.parametros.superficie.k 
             + self.parametros.superficie.f * self.parametros.superficie.f * a * a * self.parametros.camera.posicao_z * self.parametros.camera.posicao_z
             + self.parametros.superficie.e * self.parametros.superficie.e * b * b * self.parametros.camera.posicao_z * self.parametros.camera.posicao_z
             + self.parametros.superficie.d * self.parametros.superficie.d * a * a * self.parametros.camera.posicao_y * self.parametros.camera.posicao_y
             + 2 * self.parametros.superficie.j * self.parametros.superficie.e * self.parametros.camera.posicao_y
             + 2 * self.parametros.superficie.j * self.parametros.superficie.g * a 
             + 2 * self.parametros.superficie.j * self.parametros.superficie.f * self.parametros.camera.posicao_x
             - 2 * self.parametros.superficie.f * a * self.parametros.superficie.k
             - self.parametros.superficie.b * b * b * self.parametros.superficie.k 
             - 2 * self.parametros.superficie.c * self.parametros.superficie.h * self.parametros.camera.posicao_y
             - self.parametros.superficie.c * self.parametros.superficie.a * self.parametros.camera.posicao_x * self.parametros.camera.posicao_x
             - self.parametros.superficie.c * self.parametros.superficie.b * self.parametros.camera.posicao_y * self.parametros.camera.posicao_y
             - self.parametros.superficie.a * a * a * self.parametros.superficie.k 
             + 2 * self.parametros.superficie.d * self.parametros.camera.posicao_x * b * b * self.parametros.superficie.h
             - 2 * self.parametros.superficie.d * self.parametros.camera.posicao_x * b * self.parametros.superficie.f * a * self.parametros.camera.posicao_z
             - 2 * self.parametros.superficie.d * self.parametros.camera.posicao_x * b * self.parametros.superficie.e * self.parametros.camera.posicao_y
             - 2 * self.parametros.superficie.d * self.parametros.camera.posicao_x * b * self.parametros.superficie.g * a
             + 2 * self.parametros.superficie.d * self.parametros.camera.posicao_x * b * b * self.parametros.superficie.e * self.parametros.camera.posicao_z
             + 2 * self.parametros.superficie.d * self.parametros.camera.posicao_x * self.parametros.camera.posicao_x * b * self.parametros.superficie.f
             - 2 * self.parametros.superficie.d * self.parametros.superficie.d * self.parametros.camera.posicao_x * b * a * self.parametros.camera.posicao_y
             + 2 * self.parametros.superficie.b * self.parametros.camera.posicao_y * b * self.parametros.superficie.a * self.parametros.camera.posicao_x * a
             + 2 * self.parametros.superficie.b * self.parametros.camera.posicao_y * b * self.parametros.superficie.f * a * self.parametros.camera.posicao_z
             + 2 * self.parametros.superficie.b * self.parametros.camera.posicao_y * b * self.parametros.superficie.g * a
             + 2 * self.parametros.superficie.b * self.parametros.camera.posicao_y * b * self.parametros.superficie.f * self.parametros.camera.posicao_x
             + self.parametros.superficie.h * self.parametros.superficie.h * b * b
             + self.parametros.superficie.e * self.parametros.superficie.e * self.parametros.camera.posicao_y * self.parametros.camera.posicao_y 
             + self.parametros.superficie.g * self.parametros.superficie.g * a * a 
             + self.parametros.superficie.f * self.parametros.superficie.f * self.parametros.camera.posicao_x * self.parametros.camera.posicao_x 
             - 2 * self.parametros.superficie.a * a * a * self.parametros.camera.posicao_z * self.parametros.superficie.e * self.parametros.camera.posicao_y
             + 2 * self.parametros.superficie.a * self.parametros.camera.posicao_x * a * self.parametros.superficie.h * b 
             + 2 * self.parametros.superficie.a * self.parametros.camera.posicao_x * a * self.parametros.superficie.e * self.parametros.camera.posicao_y 
             + 2 * self.parametros.superficie.a * self.parametros.camera.posicao_x * a * self.parametros.superficie.e * b * self.parametros.camera.posicao_z
             + 2 * self.parametros.superficie.h * b * self.parametros.superficie.f * a * self.parametros.camera.posicao_z
             - 2 * self.parametros.superficie.h * b * self.parametros.superficie.e * self.parametros.camera.posicao_y
             + 2 * self.parametros.superficie.h * b * self.parametros.superficie.g * a 
             + 2 * self.parametros.superficie.h * b * b * self.parametros.superficie.e * self.parametros.camera.posicao_z
             + 2 * self.parametros.superficie.h * b * self.parametros.superficie.f * self.parametros.camera.posicao_x 
             - 2 * self.parametros.superficie.h * b * self.parametros.superficie.d * a * self.parametros.camera.posicao_y
             - 2 * self.parametros.superficie.f * a * self.parametros.camera.posicao_z * self.parametros.superficie.e * self.parametros.camera.posicao_y
             + 2 * self.parametros.superficie.f * a * a * self.parametros.camera.posicao_z * self.parametros.superficie.g 
             + 2 * self.parametros.superficie.f * a * self.parametros.camera.posicao_z * self.parametros.camera.posicao_z * self.parametros.superficie.e * b 
             - 2 * self.parametros.superficie.f * self.parametros.superficie.f * a * self.parametros.camera.posicao_z * self.parametros.camera.posicao_x
             + 2 * self.parametros.superficie.f * a * a * self.parametros.camera.posicao_z * self.parametros.superficie.d * self.parametros.camera.posicao_y
             + 2 * self.parametros.superficie.e * self.parametros.camera.posicao_y * self.parametros.superficie.g * a 
             - 2 * self.parametros.superficie.e * self.parametros.superficie.e * self.parametros.camera.posicao_y * b * self.parametros.camera.posicao_z 
             + 2 * self.parametros.superficie.e * self.parametros.camera.posicao_y * self.parametros.superficie.f * self.parametros.camera.posicao_x
             + 2 * self.parametros.superficie.e * self.parametros.camera.posicao_y * self.parametros.camera.posicao_y * self.parametros.superficie.d * a 
             - 2 * self.parametros.superficie.e * self.parametros.camera.posicao_y * self.parametros.superficie.d * a * b * self.parametros.camera.posicao_z
             + 2 * self.parametros.superficie.g * a * self.parametros.superficie.e * b * self.parametros.camera.posicao_z 
             - 2 * self.parametros.superficie.g * a * self.parametros.superficie.f * self.parametros.camera.posicao_x 
             + 2 * self.parametros.superficie.g * a * a * self.parametros.superficie.d * self.parametros.camera.posicao_y
             - 2 * self.parametros.superficie.e * b * self.parametros.camera.posicao_z * self.parametros.superficie.f * self.parametros.camera.posicao_x 
             - 2 * self.parametros.superficie.b * b * b * self.parametros.camera.posicao_z * self.parametros.superficie.f * self.parametros.camera.posicao_x
             - 2 * self.parametros.superficie.f * self.parametros.camera.posicao_x * self.parametros.superficie.d * a * self.parametros.camera.posicao_y
             + 2 * self.parametros.superficie.d * self.parametros.camera.posicao_x * b * self.parametros.superficie.j 
             + 2 * self.parametros.superficie.b * self.parametros.camera.posicao_y * b * self.parametros.superficie.j 
             - 2 * self.parametros.superficie.j * self.parametros.superficie.a * a * a * self.parametros.camera.posicao_z 
             + 2 * self.parametros.superficie.j * self.parametros.superficie.a * self.parametros.camera.posicao_x * a 
             - 2 * self.parametros.superficie.j * self.parametros.superficie.f * a * self.parametros.camera.posicao_z 
             - 2 * self.parametros.superficie.j * self.parametros.superficie.e * b * self.parametros.camera.posicao_z 
             - 2 * self.parametros.superficie.j * self.parametros.superficie.b * b * b * self.parametros.camera.posicao_z 
             + 2 * self.parametros.superficie.j * self.parametros.superficie.d * a * self.parametros.camera.posicao_y
             - 4 * self.parametros.superficie.j * self.parametros.superficie.d * a * b * self.parametros.camera.posicao_z 
             - 4 * self.parametros.superficie.f * a * self.parametros.superficie.h * self.parametros.camera.posicao_y
             - 2 * self.parametros.superficie.f * a * self.parametros.superficie.b * self.parametros.camera.posicao_y * self.parametros.camera.posicao_y
             - 2 * self.parametros.superficie.b * b * b * self.parametros.superficie.g * self.parametros.camera.posicao_x
             - self.parametros.superficie.b * b * b * a * self.parametros.camera.posicao_x * self.parametros.camera.posicao_x
             - 4 * self.parametros.superficie.e * b * self.parametros.superficie.g * self.parametros.camera.posicao_x
             - 2 * self.parametros.superficie.e * b * a * self.parametros.camera.posicao_x * self.parametros.camera.posicao_x
             - 2 * self.parametros.superficie.a * a * a * self.parametros.superficie.h * self.parametros.camera.posicao_y
             - self.parametros.superficie.a * a * a * b * self.parametros.camera.posicao_y * self.parametros.camera.posicao_y
             - 2 * self.parametros.superficie.c * self.parametros.superficie.d * self.parametros.camera.posicao_x * self.parametros.camera.posicao_y
             - self.parametros.superficie.c * self.parametros.superficie.b * b * b * self.parametros.camera.posicao_z * self.parametros.camera.posicao_z 
             - self.parametros.superficie.c * self.parametros.superficie.a * a * a * self.parametros.camera.posicao_z * self.parametros.camera.posicao_z 
             + 2 * self.parametros.superficie.c * self.parametros.superficie.a * self.parametros.camera.posicao_x * a * self.parametros.camera.posicao_z 
             + 2 * self.parametros.superficie.c * self.parametros.superficie.h * b * self.parametros.camera.posicao_z 
             - 2 * self.parametros.superficie.c * self.parametros.superficie.d * a * self.parametros.camera.posicao_z * self.parametros.camera.posicao_z * b 
             + 2 * self.parametros.superficie.c * self.parametros.superficie.b * self.parametros.camera.posicao_y * b * self.parametros.camera.posicao_z
             + 2 * self.parametros.superficie.c * self.parametros.superficie.d * self.parametros.camera.posicao_x * b * self.parametros.camera.posicao_z 
             + 2 * self.parametros.superficie.c * self.parametros.superficie.g * a * self.parametros.camera.posicao_z 
             + 2 * self.parametros.superficie.c * self.parametros.superficie.d * a * self.parametros.camera.posicao_z * self.parametros.camera.posicao_y
             - 2 * self.parametros.superficie.d * a * b * self.parametros.superficie.k)
        #verificar o que retorna se for negativo
        if result >= 0:
            return sqrt(result)
        
        return -1        



        
    #Metodo que calcula o denominador dos valores de Z 
    def __calcula_denominador(self, a, b):
        return (2 * self.parametros.superficie.f * a 
                + self.parametros.superficie.b * b * b 
                + self.parametros.superficie.c 
                + 2 * self.parametros.superficie.e * b 
                + 2 * self.parametros.superficie.d * a * b 
                + self.parametros.superficie.a * a * a)



    #Metodo que calcula o produto escalar de dois vetores
    def __calcula_produto_escalar(self, vetor1, vetor2):
        return vetor1[0] * vetor2[0] + vetor1[1] * vetor2[1] + vetor1[2] * vetor2[2] 



    #Metodo que calcula o modulo de um vetor
    def __calcula_modulo(self, vetor1):
        return sqrt(vetor1[0]*vetor1[0] + vetor1[1]*vetor1[1] + vetor1[2]*vetor1[2])



    #Metodo que normaliza (pag 07)
    def __normaliza(self, i, j):
        a = self.Maior - self.Menor
        if a <= 0:
            a = 1
        else:
            a = (MaxGray - MinGray) / a
            
        b = MinGray - (self.Menor * a)
        
        result = [round (self.matriz_imagem[i][j][0] * a + b), round (self.matriz_imagem[i][j][1] * a + b), round (self.matriz_imagem[i][j][2] * a + b)]
        return result




    #Metodo responsavel por toda a acao de criar a imagem
    def renderiza(self):
        
        print "ACAO:", "Iniciando matriz da imagem"
        #Inicializando a matriz Imagem
        
        self.inicializa_matriz_imagem()
        
        #Inicializando a matriz Rotacao
        print "ACAO:", "Iniciando matriz de rotacao"
        self.inicializa_matriz_rotacao()
        
        #Chama o algoritmo de Phonger
        print "ACAO:", "Executando algoritmo de phong..."
        self.algoritmo_phonger()
        
        #Normaliza
        print "ACAO:", "Normalizando imagem"
        
        #Gera imagem de saida
        print "ACAO:", "Gerando saida"
        
        imagem = Image.new("RGB", ( int(self.parametros.camera.largura), int(self.parametros.camera.altura)))
        imagem_desenhavel = ImageDraw(imagem)
        
        for x in range (int(self.parametros.camera.largura)):
            for y in range (int(self.parametros.camera.altura)):
                vetor_rgb = self.__normaliza(x, y)
                imagem_desenhavel.point((x, y), (int(vetor_rgb[0]), int(vetor_rgb[1]), int(vetor_rgb[2])))
                
        imagem.show()
        imagem.save("imagem.jpg")
        
        print "ACAO:", "Pronto!"
