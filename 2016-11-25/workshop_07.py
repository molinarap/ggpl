""" workshop 07 """
from pyplasm import *

# texture
darkWoodTexture = "texture/dark_wood.jpg"
whiteWoodTexture = "texture/white_wood.jpg"
glassTexture = "texture/glass.jpg"
metalTexture = "texture/metal.jpg"

# window 1
xWindow1 = [0.0,0.1,0.6,0.7,1.2,1.3]
yWindow1 = [0.0,0.1,1.2,1.3,1.8,1.9]
occWindow1 = [[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1]]

# window 2
xWindow2 = [0.0,0.1,0.6,0.7,2.0,2.1,2.5,2.6]
yWindow2 = [0.0,0.1,1.5,1.6,2.0,2.1]
occWindow2 = [[1,1,1,1,1,1,1],[1,0,1,0,1,0,1],[1,1,1,1,1,1,1],[1,0,1,0,1,0,1],[1,1,1,1,1,1,1]]

# door 1
xDoor1 = [0.0, 1.0]
yDoor1 = [0.0,0.37,0.4,0.78,0.8,1.18,1.2,1.58,1.6,2.0]
occDoor1 = [[1],[0],[1],[0],[1],[0],[1],[0],[1]]

# door 2
xDoor2 = [0.0,0.2,0.4,0.6,0.8,1.0]
yDoor2 = [0.0,0.2,0.9,1.0,1.6,1.8]
occDoor2 = [[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1]]

# struttura iniziale
zero = QUOTE([.0,.0])
initStruct = STRUCT([zero])

# funzione che costruisce una finestra
def windows(i, j, s):
	if j != len(yWindow1)-1:
		if  i != len(xWindow1)-1:
			if occWindow1[j][i]==0:
				piece = TEXTURE([glassTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(CUBOID([xWindow1[i+1]-xWindow1[i],yWindow1[j+1]-yWindow1[j],0.01]))
				pieceTras = STRUCT([T([1,2,3])([xWindow1[i],yWindow1[j],0.1/3]), piece])
			else:
				piece = TEXTURE([darkWoodTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(CUBOID([xWindow1[i+1]-xWindow1[i],yWindow1[j+1]-yWindow1[j],0.1]))
				pieceTras = STRUCT([T([1,2])([xWindow1[i],yWindow1[j]]), piece])
			s = STRUCT([s,pieceTras])
			return windows(i+1, j, s)
		else:
			return windows(0, j+1, s)
	else:
		VIEW(s)

windows(0, 0, initStruct)

# funzione che costruisce una porta
def doors(i, j, s):
	if j != len(yDoor1)-1:
		if  i != len(xDoor1)-1:
			if occDoor1[j][i]==0:
				piece = TEXTURE([metalTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(CUBOID([xDoor1[i+1]-xDoor1[i],yDoor1[j+1]-yDoor1[j],0.1]))
				pieceTras = STRUCT([T([1,2,3])([xDoor1[i],yDoor1[j],0.0]), piece])
			else:
				piece = TEXTURE([whiteWoodTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(CUBOID([xDoor1[i+1]-xDoor1[i],yDoor1[j+1]-yDoor1[j],0.1]))
				pieceTras = STRUCT([T([1,2])([xDoor1[i],yDoor1[j]]), piece])
			s = STRUCT([s,pieceTras])
			return doors(i+1, j, s)
		else:
			return doors(0, j+1, s)
	else:
		handle = TEXTURE([metalTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(CUBOID([0.2,0.05,0.05]))
		handle = STRUCT([T([1,2,3])([0.0,0.0,0.15]), handle])
		handle_1 = TEXTURE([metalTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(CUBOID([0.05,0.05,0.05]))
		handle_1 = STRUCT([T([1,2,3])([0.0,0.0,0.1]), handle_1])
		handle_tras = STRUCT([handle,handle_1])
		handle_tras = STRUCT([T([1,2,3])([xDoor1[i]+0.1,yDoor1[j]/2,0.0]), handle_tras])
		s = STRUCT([s,handle_tras])
		VIEW(s)

doors(0, 0, initStruct)

