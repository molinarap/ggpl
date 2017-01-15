""" workshop 08 """
from pyplasm import *
import numpy as np
import sys

sys.setrecursionlimit(1500)

bricksTexture = "texture/bricks.jpg"
wallTexture = "texture/wall.jpg"

zero = CUBOID([.0,.0,.0])
initStruct = STRUCT([zero])
level_height = [0.0,30.0,30.0,20.0,0.0,30.0,30.0,20.0,0.0]

def readFile(l,reading_level,i):
  file = open("lines/level-"+str(l)+".lines","r")
  data = file.read()
  file.close()
  d = data.splitlines()
  reading_level = reading_level + [d]
  if i==8:
    return reading_level
  else:
    return readFile(l+1, reading_level, i+1)

level = readFile(1, [], 0)

def createBase(i,s1,level):
  if i < len(level[0])-1:
    a = level[0][i]
    a_split = a.split(",")
    a_number = np.array(a_split, dtype=float)
    a_pol = POLYLINE([[a_number[0],a_number[1]],[a_number[0],a_number[3]],[a_number[2],a_number[1]],[a_number[2],a_number[3]]])
    a_off = OFFSET([1.0, 1.0, 1.0])(a_pol)
    a_texture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(a_off)
    s2 = STRUCT([a_texture, s1])
    return createBase(i+1,s2,level)
  else:
    s1 = SOLIDIFY(SKEL_2(s1))
    return s1

def createFirstFloor(l,i,h,s1,level):
  if l <= 3:
    if i < len(level[l])-1:
      a = level[l][i]
      a_split = a.split(",")
      a_number = np.array(a_split, dtype=float)
      a_pol = MKPOL([[[a_number[0],a_number[1],0.0],[a_number[0],a_number[3],0.0],[a_number[2],a_number[1],0.0],[a_number[2],a_number[3],0.0]],[[1,2,3,4]],[1]])
      a_off = OFFSET([1.5, 1.5, level_height[l]])(a_pol)
      a_texture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(a_off)
      a_tras = STRUCT([T(3)(h), a_texture])
      s2 = STRUCT([a_tras, s1])
      return createFirstFloor(l,i+1,h,s2,level)
    else:
      h = h + level_height[l]
      return createFirstFloor(l+1,0,h,s1,level)
  else:
    return s1

def createSecondFloor(l,i,h,s1,level):
  if l <= 8:
    if i < len(level[l])-1:
      a = level[l][i]
      a_split = a.split(",")
      a_number = np.array(a_split, dtype=float)
      a_pol = MKPOL([[[a_number[0],a_number[1],0.0],[a_number[0],a_number[3],0.0],[a_number[2],a_number[1],0.0],[a_number[2],a_number[3],0.0]],[[1,2,3,4]],[1]])
      a_off = OFFSET([1.5, 1.5, level_height[l]])(a_pol)
      a_texture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(a_off)
      a_tras = STRUCT([T(3)(h), a_texture])
      s2 = STRUCT([a_tras, s1])
      return createSecondFloor(l,i+1,h,s2,level)
    else:
      h = h + level_height[l]
      return createSecondFloor(l+1,0,h,s1,level)
  else:
    return s1


def createHouse():
  a = createBase(0,initStruct,level)
  b = createFirstFloor(1,0,0.0,initStruct,level)
  c = createSecondFloor(5,0,0.0,initStruct,level)
  house=STRUCT([a,T(3)(1.0),b])
  house=STRUCT([house,T(3)(81.0),a])
  house=STRUCT([house,T(3)(82.0),c])
  house=STRUCT([house,T(3)(162.0),a])
  VIEW(house)

createHouse()
