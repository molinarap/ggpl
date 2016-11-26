""" workshop 05 """
from pyplasm import *

xArray = [0.0,0.1,0.6,0.7,1.2,1.3]
yArray = [0.0,0.1,1.2,1.3]
occ = [[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1]]

zero = QUOTE([.0,.0])
initStruct = STRUCT([zero])

# OFFSET([par,par,par])

def window(i, j, s):
	if j != len(yArray)-1:
		if  i != len(xArray)-1:
			if occ[j][i]==0:
				x = COLOR(BLUE)(CUBOID([xArray[i+1]-xArray[i],yArray[j+1]-yArray[j],0.01]))
				x_tras = STRUCT([T([1,2,3])([xArray[i],yArray[j],0.1/3]), x])
			else:
				x = COLOR(WHITE)(CUBOID([xArray[i+1]-xArray[i],yArray[j+1]-yArray[j],0.1]))
				x_tras = STRUCT([T([1,2])([xArray[i],yArray[j]]), x])
			s = STRUCT([s,x_tras])
			return window(i+1, j, s)
		else:
			return window(0, j+1, s)
	else:
		s = STRUCT([T([1,2])([xArray[i],yArray[j]]), x])
		VIEW(s)

window(0, 0, initStruct)
