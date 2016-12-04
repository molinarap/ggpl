""" workshop 08 """
from pyplasm import *
import numpy as np

# a_number[0] --> x1
# a_number[1] --> y1
# a_number[2] --> x2
# a_number[3] --> y2
# [a_number[0],a_number[1]] --> x1,y1
# [a_number[0],a_number[3]] --> x1,y2
# [a_number[2],a_number[1]] --> x2,y1
# [a_number[2],a_number[3]] --> x2,y1

bricksTexture = "texture/bricks.jpg"
wallTexture = "texture/wall.jpg"

# struttura iniziale
zero = CUBOID([.0,.0,.0])
initStruct = STRUCT([zero])

level_height = [0.0,30.0,30.0,20.0,0.0]		

def readFile(l):
	file = open("lines/level-"+str(l)+".lines","r")
	data = file.read()
	file.close()
	return data.splitlines()

level1 = readFile(1)
level2 = readFile(2)
level3 = readFile(3)
level4 = readFile(4)
level = [level1,level2,level3,level4,level1]

def createPol(l,i,h,s1):
	if l <= len(level)-1:
		if i < len(level[l])-1:
			a = level[l][i]
			a_split = a.split(",")
			a_number = np.array(a_split, dtype=float)
			a_pol = MKPOL([[[a_number[0],a_number[1],0.0],[a_number[0],a_number[3],0.0],[a_number[2],a_number[1],0.0],[a_number[2],a_number[3],0.0]],[[1,2,3,4]],[1]])
			a_off = OFFSET([1.5, 1.5, level_height[l]])(a_pol)
			a_texture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(a_off)
			a_tras = STRUCT([T(3)(h), a_texture])
			s2 = STRUCT([a_tras, s1])
			return createPol(l,i+1,h,s2)
		else:
			h = h + level_height[l]
			return createPol(l+1,0,h,s1)
	else:
		VIEW(s1)

createPol(0,0,0.0,initStruct)






