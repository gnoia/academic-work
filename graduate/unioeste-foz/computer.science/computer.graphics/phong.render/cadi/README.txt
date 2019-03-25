==============================================================
Stonehenge Render (2010)
==============================================================

	Stonehenge Render é um renderizedor de imagens.

	Nele é implementado o modelo de iluminação de Phong,
tendo como entradas os seguintes dados:

	Iluminação
		Fonte de Luz
			Posição Fonte de Luz - XYZ
			Cor Fonte de Luz - RGB
			Cor do Ambiente - RGB
		Coeficientes
			Difusão - RGB
			Especular - RGB
			Ambiente - RGB
		Expoente Especular

	Camera
		Exterior
			Posição - XYZ
			Orientação - XYZ
		Interior
			Largura
			Altura
			Pixel X
			Pixel Y
			Distancia Focal
		
	Superficie
		A, B, C, D, E, F, G, H, J, K.

	Todos esses parametros acima são os dados de entrada da
interface e a saida será uma imagem gerada, que dependerá dos
dados tidos como entrada.

Desenvolvedor:

	Claudinei Callegari
	Matheus Cristiano Barreto

Plataformas de Desenvolvimentos:

	Linux - Ubuntu 9.10.

IDE de Desenvolvimento:

	Eclipse Galileo
	Glade (Interface)

Linguagem de Desenvolvimento:

	Python
