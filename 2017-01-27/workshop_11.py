""" workshop 11 """
from pyplasm import *
import numpy as np
import sys, os

sys.setrecursionlimit(1500)

grassTexture = "texture/grass.jpg"
asphaltTexture = "texture/asphalt.jpg"

zero = CUBOID([.0,.0,.0])
initStruct = STRUCT([zero])
level_height = [30.0,30.0,20.0,30.0,30.0,20.0]
heights = [60.0,20.0,3.5,60.0,20.0]

def countFileDirectory(path):
  i = 0
  for name in os.listdir(path):
      if not name.startswith('.'):
        i = i + 1
  return i

def readSvg(l,reading_level,path):
  file = open("params/"+path+"/lines/level-"+str(l)+".lines","r")
  data = file.read()
  n = countFileDirectory("params/"+path+"/lines/")
  file.close()
  d = data.splitlines()
  reading_level = reading_level + [d]
  if l!=n-1:
    return readSvg(l+1,reading_level,path)
  else:
    return reading_level

levelBase = readSvg(0,[],"base")
levelStreet = readSvg(0,[],"street")
levelHouse = readSvg(0,[],"house")

def parseLines(l,i, params):
  string_line = params[l][i]
  split_line = string_line.split(",")
  array_line = np.array(split_line, dtype=float)
  return array_line

def buildGarden(i,s1):
  if i < len(levelBase[0]):
    params = parseLines(0,i,levelBase)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([4.0, 5.5, 5.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return buildGarden(i+1,s2)
  else:
    s1 = SOLIDIFY(SKEL_2(s1))
    s1 = TEXTURE([grassTexture, TRUE, FALSE, 1, 1, 0, 10, 1])(s1)
    return s1

def buildStreet(i,s1):
  if i < len(levelStreet[0]):
    params = parseLines(0,i,levelStreet)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([0.0, 0.0, 5.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return buildStreet(i+1,s2)
  else:
    #s1 = SOLIDIFY(SKEL_2(s1))
    s1=STRUCT([T(3)(5.0),s1])
    #s1 = TEXTURE([asphaltTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(s1)
    return s1

def buildHouseBase(i,s1):
  if i < len(levelHouse[0]):
    params = parseLines(0,i,levelHouse)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([0.0, 0.0, 5.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return buildHouseBase(i+1,s2)
  else:
    s1 = SOLIDIFY(SKEL_2(s1))
    s1 = TEXTURE([asphaltTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(s1)
    return s1

def buildHouse():
  garden_level = buildGarden(0,initStruct)
  street_level = buildStreet(0,initStruct)
  house_level = buildHouseBase(0,initStruct)
  house=STRUCT([initStruct,T(3)(0.0),garden_level])
  house=STRUCT([house,T(3)(5.0),street_level])
  house=STRUCT([house,T(3)(5.0),house_level])
  return house

def createCity(i,s1,d):
  if i < 1:
    print(i)
    h1=STRUCT([T(1)(d),buildHouse()])
    s1= STRUCT([h1, s1])
    return createCity(i+1,s1,d+4000.0)
  else:
    VIEW(s1)

createCity(0,initStruct,0.0)








