""" workshop 08 """
from pyplasm import *
import numpy as np
import sys, os

sys.setrecursionlimit(1500)

pavTexture = "texture/pav2.png"
wallTexture = "texture/wall1.jpg"
wallStone = "texture/wall5.jpg"

zero = CUBOID([.0,.0,.0])
initStruct = STRUCT([zero])
level_height = [30.0,30.0,20.0,30.0,30.0,20.0]

def readSvg(l,reading_level,path):
  file = open("all/"+path+"/lines/level-"+str(l)+".lines","r")
  data = file.read()
  n = len([name for name in os.listdir("all/"+path+"/lines/")])-2
  file.close()
  d = data.splitlines()
  reading_level = reading_level + [d]
  if l<n:
    return readSvg(l+1,reading_level,path)
  else:
    return reading_level

levelBase = readSvg(0,[],"base")
levelEst = readSvg(0,[],"esterno")

def createBase(i,s1):
  if i < len(levelBase[0]):
    a = levelBase[0][i]
    a_split = a.split(",")
    a_number = np.array(a_split, dtype=float)
    a_pol = POLYLINE([[a_number[0],a_number[1]],[a_number[2],a_number[3]]])
    a_off = OFFSET([4.0, 5.5, 2.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return createBase(i+1,s2)
  else:
    s1 = SOLIDIFY(SKEL_2(s1))
    s1 = TEXTURE([pavTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(s1)
    return s1

def createEst(l,i,h,s1):
  if l <= len(levelEst)-1:
    if i < len(levelEst[l])-1:
      a = levelEst[l][i]
      a_split = a.split(",")
      a_number = np.array(a_split, dtype=float)
      a_pol = MKPOL([[[a_number[0],a_number[1],0.0],[a_number[0],a_number[3],0.0],[a_number[2],a_number[1],0.0],[a_number[2],a_number[3],0.0]],[[1,2,3,4]],[1]])
      a_off = OFFSET([3.0, 3.0, level_height[l]])(a_pol)
      if l==0:
        a_texture = TEXTURE([wallStone, TRUE, FALSE, 1, 1, 0, 2, 1])(a_off)
      else:
        if l==3:
          a_texture = TEXTURE([wallStone, TRUE, FALSE, 1, 1, 0, 6, 1])(a_off)
        else:
          a_texture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(a_off)
      a_tras = STRUCT([T(3)(h), a_texture])
      s2 = STRUCT([a_tras, s1])
      return createEst(l,i+1,h,s2)
    else:
      h = h + level_height[l]
      return createEst(l+1,0,h,s1)
  else:
    return s1

# def createInt(l,i,h,s1,level):
#   if l <= len(levelInt)-1:
#     if i < len(levelInt[l])-1:
#       a = levelInt[l][i]
#       a_split = a.split(",")
#       a_number = np.array(a_split, dtype=float)
#       a_pol = MKPOL([[[a_number[0],a_number[1],0.0],[a_number[0],a_number[3],0.0],[a_number[2],a_number[1],0.0],[a_number[2],a_number[3],0.0]],[[1,2,3,4]],[1]])
#       a_off = OFFSET([1.0, 1.0, level_height[l]])(a_pol)
#       a_texture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 2, 1])(a_off)
#       a_tras = STRUCT([T(3)(h), a_texture])
#       s2 = STRUCT([a_tras, s1])
#       return createInt(l,i+1,h,s2,level)
#     else:
#       h = h + level_height[l]
#       return createInt(l+1,0,h,s1,level)
#   else:
#     return s1

def createHouse():
  a = createBase(0,initStruct)
  b = createEst(0,0,0.0,initStruct)
  # c = createInt(1,0,0.0,initStruct,levelInt)
  house=STRUCT([a,T(3)(3.0),b])
  house=STRUCT([house,T(3)(83.0),a])
  house=STRUCT([house,T(3)(163.0),a])
  #house = SKEL_3(house)
  VIEW(house)

createHouse()
