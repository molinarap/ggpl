""" workshop 11 """
from pyplasm import *
import numpy as np
import sys, os

sys.path.append("house")
import house

sys.setrecursionlimit(1500)

grassTexture = "texture/grass.jpg"
asphaltTexture = "texture/asphalt.jpg"
pianoTexture = "texture/stair.jpg"

zero = CUBOID([.0,.0,.0])
initStruct = STRUCT([zero])
level_height = [30.0,30.0,20.0,30.0,30.0,20.0]
heights = [60.0,20.0,3.5,60.0,20.0]

def countFileDirectory(path):
  i = 0
  for name in os.listdir(path):
      if not name.startswith("."):
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
levelPiano = readSvg(0,[],"piano")
levelCurve = readSvg(0,[],"curve")

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

def buildCurve(l,i,s1):
  if l <= len(levelCurve)-1:
    if i < len(levelCurve[l]):
      params1 = parseLines(l,i,levelCurve)
      params2 = parseLines(l,i+1,levelCurve)
      c1 = MAP(BEZIER(S1)([[params1[2],params1[3]],[params1[0],params1[1]],[params2[0],params2[1]]]))(INTERVALS(1)(32))
      c1 = OFFSET([0.0, 0.0, 3.0])(c1)
      s1 = STRUCT([s1,c1])
      return buildCurve(l,i+2,s1)
    else:
      return buildCurve(l+1,0,s1)
  else:
    return s1

def buildStreet(i,s1):
  if i < len(levelStreet[0]):
    params = parseLines(0,i,levelStreet)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([0.0, 0.0, 3.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return buildStreet(i+1,s2)
  else:
    curve = buildCurve(0,0,initStruct)
    s1 = SOLIDIFY(s1)
    curve = SOLIDIFY(curve)
    s1 = UNION([s1,curve])
    #s1 = STRUCT([s1,curve])
    s1 = STRUCT([T(3)(5.0),s1])
    s1 = TEXTURE([asphaltTexture, TRUE, FALSE, 1, 1, 0, 1, 10])(s1)
    return s1

def buildStreetHouse(i,s1):
  if i < len(levelPiano[0]):
    params = parseLines(0,i,levelPiano)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([0.0, 0.0, 3.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return buildStreetHouse(i+1,s2)
  else:
    s1 = SOLIDIFY(SKEL_2(s1))
    s1=STRUCT([T(3)(5.0),s1])
    s1 = TEXTURE([pianoTexture, TRUE, FALSE, 1, 1, 0, 1, 10])(s1)
    return s1

def buildHouseBase(i,s1):
  if i < len(levelHouse[0]):
    params = parseLines(0,i,levelHouse)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([0.0, 0.0, 3.0])(a_pol)
    s1 = STRUCT([a_off, s1])
    return buildHouseBase(i+1,s1)
  else:
    s1 = SOLIDIFY(SKEL_2(s1))
    return s1

def buildHouseBase2(i,s1):
  if i < len(levelHouse[0]):
    params = parseLines(0,i,levelHouse)
    h2 = house.createMoreHouse(0,initStruct,0.0)
    if i==7 or i==15 or i==23:
      h2 = ROTATE([1,2])(-PI/2)(h2)
      h2 = STRUCT([T([1,2,3])([params[2]-10.0,params[3]+111.0,2.0]),h2])
    else:
      h2 = ROTATE([1,2])(PI/2)(h2)
      h2 = STRUCT([T([1,2,3])([params[0]+10.0,params[1]-111.0,2.0]),h2])
    s1 = STRUCT([h2, s1])
    return buildHouseBase2(i+4,s1)
  else:
    return s1

def buildHouse():
  garden_level = buildGarden(0,initStruct)
  street_level = buildStreet(0,initStruct)
  house_level = buildHouseBase(0,initStruct)
  house_level2 = buildHouseBase2(3,initStruct)
  streetHouse_level = buildStreetHouse(0,initStruct)
  house=STRUCT([initStruct,T(3)(0.0),garden_level])
  house=STRUCT([house,T(3)(2.0),street_level])
  house=STRUCT([house,T(3)(2.0),house_level])
  house=STRUCT([house,T(3)(2.0),house_level2])
  house=STRUCT([house,T(3)(2.0),streetHouse_level])
  return house

def createCity(i,s1,d):
  if i < 1:
    h = buildHouse()
    h1=STRUCT([T(1)(d),h])
    h2=STRUCT([T(1)(d+1900),h])
    h3=STRUCT([T(2)(d+2200),h])
    h4=STRUCT([T([1,+2])([d+1900,d+2200]),h])
    s1= STRUCT([h1,h2,h3,h4,s1])
    return createCity(i+1,s1,d+1900.0)
  else:
    VIEW(s1)

createCity(0,initStruct,0.0)





