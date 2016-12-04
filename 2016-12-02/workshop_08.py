""" workshop 08 """
from pyplasm import *
import numpy as np

""" texture """
bricksTexture = "texture/bricks.jpg"
wallTexture = "texture/wall.jpg"

""" struttura iniziale """
zero = CUBOID([.0,.0,.0])
initStruct = STRUCT([zero])

""" funzione che legge file .lines per estrarre i punti """
def readFile(l):
	file = open("lines/level-"+str(l)+".lines","r")
	data = file.read()
	file.close()
	return data.splitlines()

""" contorno della piantina """
level1 = readFile(1)
""" piantina con porte """
level2 = readFile(2)
""" piantina con le finestre e le porte """
level3 = readFile(3)
""" piantina con stipiti delle porte """
level4 = readFile(4)

""" inserisco tutto in un array che andrò a scorrere per costruire un piano sull'altro"""
level = [level1,level2,level3,level4,level1]

""" altezza di ogni piano """
level_height = [0.0,30.0,30.0,20.0,0.0]		

""" funzione che legge i punti e costruisce tutti livelli della piantina """
def createHouse(l,i,h,s1):
	# ciclo i livelli
	if l <= len(level)-1:
		# ciclo i punti di ongni muro di un piano
		if i < len(level[l])-1:
			# prendo i punti di un muro
			a = level[l][i]
			# li inserisco in un array splittando la virgola
			a_split = a.split(",")
			# trasformo ogni elemento dell'array da string a float
			a_number = np.array(a_split, dtype=float)
			# creo il muro(1D) unendo i punti estratti dal lines nella sua posizione
			# a_number[0] --> x1
			# a_number[1] --> y1
			# a_number[2] --> x2
			# a_number[3] --> y2
			# [a_number[0],a_number[1]] --> x1,y1
			# [a_number[0],a_number[3]] --> x1,y2
			# [a_number[2],a_number[1]] --> x2,y1
			# [a_number[2],a_number[3]] --> x2,y1
			a_pol = MKPOL([[[a_number[0],a_number[1],0.0],[a_number[0],a_number[3],0.0],[a_number[2],a_number[1],0.0],[a_number[2],a_number[3],0.0]],[[1,2,3,4]],[1]])
			# do al muro l'altezza riferita al piano che sto creando
			a_off = OFFSET([1.5, 1.5, level_height[l]])(a_pol)
			# gli incollo una texture
			a_texture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(a_off)
			# traslo il piano per farlo posizionare sopra il piano precedente tramite h
			a_tras = STRUCT([T(3)(h), a_texture])
			s2 = STRUCT([a_tras, s1])
			# rieseguo la funzione per creare un nuovo muro
			return createHouse(l,i+1,h,s2)
		else:
			#calcolo l'altezza complessiva per posizionare il nuovo piano
			h = h + level_height[l]
			# rieseguo la funzione per creare un nuovo piano
			return createHouse(l+1,0,h,s1)
	else:
		VIEW(s1)

createHouse(0,0,0.0,initStruct)






