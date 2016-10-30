"""workshop_03"""

from pyplasm import *
"""
wall --> spessura del muro laterale di sostegno
ground --> pavimento sottostante la scala
footboard --> pedana antistante la scala
height --> altezza del muro
length --> lunghezza della scalinata (profondita' del muro)
steps --> numero di gradini
dx --> larghezza gradino (parametro formale X)
dy --> lunghezza gradino (parametro formale Y)
dz --> altezza gradino (parametro formale Z)
"""
wall=0.5
ground=0.20
footboard=1.0
height=3.0
length=6.0
steps=10.0
dx= 3.5
dy=length/steps
dz=height/steps
"""inizializzazione struttura vuota in cui verra' costruita la scala"""
elem0=CUBOID([0,0,0])
struct=STRUCT([elem0])


"""
buildStair --> funzione che ricorsivamente costruisce un gradino alla volta
Quando arriva a una profondita' compresa tra i 2/5 e i 4/5 della profondita' totale costruisce un pianerottolo lungo 3 volte un gradino normale
nella costruzione del muro di sostegno e della pedana sottostante si tiene conto della lunghezza dei gradini
della loro altezza e della lunghezza del pianerottolo
"""
def buildStair(x,y,z,tempWeight,tempHeight,tempStruct):
	if(2.0*length/5.0<tempWeight<4.0*length/5.0):
		step=COLOR(BROWN)(CUBOID([x, y*3, z]))
		traslation=STRUCT([T([1,2,3])([wall/3,tempWeight,tempHeight]),step])
		tempWeight=tempWeight + y*3.0
		tempHeight=tempHeight + z	
	else:
		step=COLOR(BROWN)(CUBOID([x, y, z]))
		traslation=STRUCT([T([1,2,3])([wall/3,tempWeight,tempHeight]),step])
		tempWeight=tempWeight + y
		tempHeight=tempHeight + z
	stair=STRUCT([traslation,tempStruct])
	if tempWeight < length+y:
		buildStair(x, y, z, tempWeight, tempHeight, stair)
	else:
		m=CUBOID([wall,length+footboard+y*2,height+ground])
		p=CUBOID([dx+wall/2,length+footboard+y*2,ground])
		stair=STRUCT([T([2,3])([footboard,ground]),stair])		
		finalStairs=STRUCT([m,p,stair])

		VIEW(finalStairs)

"""
ggpl_streight_stair_with_central_landing --> funzione che prende in input i 3 parametri formali relativi alle 3 dimesioni

"""
def ggpl_streight_stair_with_central_landing(x1,y1,z1):
	buildStair(x1,y1,z1,0,0,struct)

ggpl_streight_stair_with_central_landing(dx,dy,dz)