""" workshop 11 """
from pyplasm import *
import numpy as np
import sys, os

"""importo workshop_10 per costuire la casa"""
sys.path.append("house")
import house

sys.setrecursionlimit(1500)

"""texture vari livelli della casa"""
grassTexture = "texture/grass.jpg"
asphaltTexture = "texture/asphalt.jpg"
landingTexture = "texture/landing.jpg"

"""struttra iniziale di appoggio"""
zero = CUBOID([.0,.0,.0])
initStruct = STRUCT([zero])

"""funzione che conta i file contenuti in una directory"""
def countFileDirectory(path):
  i = 0
  for name in os.listdir(path):
      if not name.startswith("."):
        i = i + 1
  return i

"""funzione che legge i file lines di tutti i livelli della casa"""
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
levelFoundation = readSvg(0,[],"foundation")
levelLanding = readSvg(0,[],"landing")
levelCurve = readSvg(0,[],"curve")

"""funzioni che trasforma le stringhe di punto dei file lines in array"""
def parseLines(l,i, params):
  string_line = params[l][i]
  split_line = string_line.split(",")
  array_line = np.array(split_line, dtype=float)
  return array_line

"""funzione che dati i file lines contenuti nell cartella /params/base/lines"""
"""costuisce la base del quartiere"""
def buildGarden(i,s1):
  if i < len(levelBase[0]):
    params = parseLines(0,i,levelBase)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([4.0, 5.5, 5.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return buildGarden(i+1,s2)
  else:
    s1 = SOLIDIFY(SKEL_2(s1))
    s1 = TEXTURE([grassTexture, TRUE, FALSE, 1, 1, 0, 16, 16])(s1)
    return s1

"""funzione che dati i file lines contenuti nell cartella /params/curve/lines"""
"""costuisce le curve utilizzando Bezier"""
def buildCurve(i,s1):
  if i < len(levelCurve[0]):
    curveExt1 = parseLines(0,i,levelCurve)
    curveExt2 = parseLines(0,i+1,levelCurve)
    curveInt1 = parseLines(1,i,levelCurve)
    curveInt2 = parseLines(1,i+1,levelCurve)
    ce = BEZIER(S1)([[curveExt1[2],curveExt1[3]],[curveExt1[0],curveExt1[1]],[curveExt2[0],curveExt2[1]]])
    ci = BEZIER(S1)([[curveInt1[2],curveInt1[3]],[curveInt1[0],curveInt1[1]],[curveInt2[0],curveInt2[1]]])
    c = MAP(BEZIER(S2)([ce,ci]))(PROD([INTERVALS(1)(10),INTERVALS(1)(10)]))
    c = OFFSET([0.0, 0.0, 3.0])(c)
    s1 = STRUCT([s1,c])
    return buildCurve(i+2,s1)
  else:
    return s1

"""funzione che dati i file lines contenuti nell cartella /params/street/lines"""
"""costuisce le strade del quartiere"""
def buildStreet(i,s1):
  if i < len(levelStreet[0]):
    params = parseLines(0,i,levelStreet)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([0.0, 0.0, 3.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return buildStreet(i+1,s2)
  else:
    curve = buildCurve(0,initStruct)
    s1 = SOLIDIFY(s1)
    s1 = STRUCT([s1,curve])
    s1 = STRUCT([T(3)(5.0),s1])
    s1 = TEXTURE([asphaltTexture, TRUE, FALSE, 1, 1, 0, 16, 16])(s1)
    return s1

"""funzione che dati i file lines contenuti nell cartella /params/landing/lines"""
"""costuisce i pianerottoli che si affacciano sulla strada"""
def buildLanding(i,s1):
  if i < len(levelLanding[0]):
    params = parseLines(0,i,levelLanding)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([0.0, 0.0, 3.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return buildLanding(i+1,s2)
  else:
    s1 = SOLIDIFY(SKEL_2(s1))
    s1=STRUCT([T(3)(5.0),s1])
    s1 = TEXTURE([landingTexture, TRUE, FALSE, 1, 1, 0, 1, 10])(s1)
    return s1

"""funzione che dati i file lines contenuti nell cartella /params/house/lines"""
"""costuisce le fondamenta per poi posizionare le case"""
def buildFoundation(i,s1):
  if i < len(levelFoundation[0]):
    params = parseLines(0,i,levelFoundation)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([0.0, 0.0, 3.0])(a_pol)
    s1 = STRUCT([a_off, s1])
    return buildFoundation(i+1,s1)
  else:
    s1 = SOLIDIFY(SKEL_2(s1))
    s1 = TEXTURE([landingTexture, TRUE, FALSE, 1, 1, 0, 1, 10])(s1)
    return s1

"""funzione che dati i file lines contenuti nell cartella /params/house/lines"""
"""richiama il workshop_10 per costruire le case sulle fondamenta creare prima"""
def buildHouse(i,s1):
  if i < len(levelFoundation[0]):
    params = parseLines(0,i,levelFoundation)
    h2 = house.createMoreHouse(0,initStruct,0.0)
    if i==7 or i==15 or i==23:
      h2 = ROTATE([1,2])(-PI/2)(h2)
      h2 = STRUCT([T([1,2,3])([params[2]-10.0,params[3]+111.0,2.0]),h2])
    else:
      h2 = ROTATE([1,2])(PI/2)(h2)
      h2 = STRUCT([T([1,2,3])([params[0]+10.0,params[1]-111.0,2.0]),h2])
    s1 = STRUCT([h2, s1])
    return buildHouse(i+4,s1)
  else:
    return s1

"""funzione che crea un quartiere assemblando tutti i livelli creati in precedenza"""
def buildDistrict():
  garden_level = buildGarden(0,initStruct)
  street_level = buildStreet(0,initStruct)
  house_level = buildFoundation(0,initStruct)
  house_level2 = buildHouse(3,initStruct)
  streetHouse_level = buildLanding(0,initStruct)
  house=STRUCT([initStruct,T(3)(0.0),garden_level])
  house=STRUCT([house,T(3)(2.0),street_level])
  house=STRUCT([house,T(3)(2.0),house_level])
  house=STRUCT([house,T(3)(2.0),house_level2])
  house=STRUCT([house,T(3)(2.0),streetHouse_level])
  return house

"""funzione che crea una citta assemblando piu' quartieri insieme"""
def createCity(i,s1,d1,d2):
  if i < 1:
    h = buildDistrict()
    h1=STRUCT([T(1)(d1),h])
    h2=STRUCT([T(1)(d1+1900),h])
    h3=STRUCT([T(2)(d2+2500),h])
    h4=STRUCT([T([1,2])([d1+1900,d2+2500]),h])
    s1= STRUCT([h1,h2,h3,h4,s1])
    s2=STRUCT([T(1)((d1+1900)*2),s1])
    s1= STRUCT([s1,s2])
    return createCity(i+1,s1,d1+1900.0,d2+2500)
  else:
    VIEW(s1)

createCity(0,initStruct,0.0,0.0)





