""" workshop 10 """
from pyplasm import *
import numpy as np
import sys, os

sys.setrecursionlimit(1500)
dirPath = '/Users/redpanda/Desktop/Grafica/ggpl/2017-01-13'

"""texture vari livelli della casa"""
pavTexture = dirPath+'/texture/pav2.png'
doorWindowsTexture = dirPath+'/texture/pav2.png'
wallTexture = dirPath+'/texture/wall2.jpg'
wallStone = dirPath+'/texture/wall5.jpg'
doorTexture = dirPath+'/texture/white_wood.jpg'
metalTexture = dirPath+'/texture/metal.jpg'
glassTexture = dirPath+'/texture/glass.jpg'
roofTexture = dirPath+'/texture/roof.jpg'
stairTexture = dirPath+'/texture/stair.jpg'

"""struttra iniziale di appoggio"""
zero = CUBOID([.0,.0,.0])
initStruct = STRUCT([zero])

"""misure per la costruzione dei vari livelli della casa"""
level_height = [30.0,30.0,20.0,30.0,30.0,20.0]
heights = [60.0,20.0,3.5,60.0,20.0]

"""funzione che conta i file contenuti in una directory"""
def countFileDirectory(path):
  i = 0
  for name in os.listdir(path):
      if not name.startswith('.'):
        i = i + 1
  return i

"""funzione che legge i file lines di tutti i livelli della casa"""
def readSvg(l,reading_level,path):
  file = open(dirPath+'/params/'+path+'/lines/level-'+str(l)+'.lines','r')
  data = file.read()
  n = countFileDirectory(dirPath+'/params/'+path+'/lines/')
  file.close()
  d = data.splitlines()
  reading_level = reading_level + [d]
  if l!=n-1:
    return readSvg(l+1,reading_level,path)
  else:
    return reading_level

levelBase = readSvg(0,[],"base")
levelExternal = readSvg(0,[],"external")
levelInternal = readSvg(0,[],"internal")
levelDoors = readSvg(0,[],"doors")
levelWindows = readSvg(0,[],"windows")
levelStair = readSvg(0,[],"stair")

"""funzioni che trasforma le stringhe di punto dei file lines in array"""
def parseLines(l,i, params):
  string_line = params[l][i]
  split_line = string_line.split(",")
  array_line = np.array(split_line, dtype=float)
  return array_line

"""funzione che dati i file lines contenuti nell cartella /params/base/lines"""
"""costuisce la base della casa"""
def buildFloor1(i,s1):
  if i < len(levelBase[0]):
    params = parseLines(0,i,levelBase)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([4.0, 5.5, 2.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return buildFloor1(i+1,s2)
  else:
    s1 = SOLIDIFY(SKEL_2(s1))
    s1 = TEXTURE([pavTexture, TRUE, FALSE, 1, 1, 0, 16, 1])(s1)
    return s1

"""funzione che dati i file lines contenuti nell cartella /params/external/lines"""
"""costuisce i muri esterni della casa"""
def buildExternal(l,i,h,s1):
  if l <= len(levelExternal)-1:
    if i < len(levelExternal[l]):
      params = parseLines(l,i,levelExternal)
      a_pol = MKPOL([[[params[0],params[1],0.0],[params[0],params[3],0.0],[params[2],params[1],0.0],[params[2],params[3],0.0]],[[1,2,3,4]],[1]])
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
      return buildExternal(l,i+1,h,s2)
    else:
      h = h + level_height[l]
      return buildExternal(l+1,0,h,s1)
  else:
    return s1

"""funzione che dati i file lines contenuti nell cartella /params/internal/lines"""
"""costuisce i muri interni della casa"""
def buildIntenal(l,i,h,s1):
  if l <= len(levelInternal)-1:
    if i < len(levelInternal[l]):
      params = parseLines(l,i,levelInternal)
      a_pol = MKPOL([[[params[0],params[1],0.0],[params[0],params[3],0.0],[params[2],params[1],0.0],[params[2],params[3],0.0]],[[1,2,3,4]],[1]])
      a_off = OFFSET([1.0, 1.0, level_height[l]])(a_pol)
      a_texture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 2, 1])(a_off)
      a_tras = STRUCT([T(3)(h), a_texture])
      s2 = STRUCT([a_tras, s1])
      return buildIntenal(l,i+1,h,s2)
    else:
      h = h + level_height[l]
      return buildIntenal(l+1,0,h,s1)
  else:
    return s1

"""funzione che dati i parametri costruisce una singola porta"""
def buildOneDoor(elem, j, h, door):
  if j < 13:
    build = MKPOL([[[elem[0],elem[1],0.0],[elem[2],elem[3],0.0]],[[1,2]],[1]])
    if not j%2:
      buildOffset = OFFSET([3.5, 3.5, 8.5])(build)
      buildTexture = TEXTURE([doorWindowsTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(buildOffset)
      buildTras = STRUCT([T([3])([h]), buildTexture])
      h = h + 8.5
    else:
      buildOffset = OFFSET([3.5, 3.5, 0.5])(build)
      buildTexture = TEXTURE([metalTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(buildOffset)
      buildTras = STRUCT([T([3])([h]), buildTexture])
      h = h + 0.5
    door = STRUCT([buildTras,door])
    return buildOneDoor(elem, j+1, h, door)
  else:
    return door

"""funzione che dati i parametri per la costruzione della porta crea una maniglia"""
"""posizionandola in maniera ottimale sulla porta"""
def createHandle(elem,s1):
  handle = MKPOL([[[elem[0],elem[1],0.0],[elem[2],elem[3],0.0]],[[1,2]],[1]])
  handle0 = OFFSET([8.0, 1.0, 1.0])(handle)
  if (elem[0]-elem[2]<1.0) & (elem[0]-elem[2]>-1.0):
    handle_0 = STRUCT([T([1,2,3])([-2.0,1.0,31.0]), handle0])
    handle_1 = STRUCT([T([1,2,3])([-2.0,3.0,31.0]), handle0])
    handle1 = OFFSET([1.0, 1.5, 1.0])(handle)
    handle_2 = STRUCT([T([1,2,3])([5.0,1.0,31.0]), handle1])
    handle_3 = STRUCT([T([1,2,3])([5.0,6.0,31.0]), handle1])
    handle_01 = DIFF([handle_0,handle_1])
    handle_23 = DIFF([handle_2,handle_3])
    handle_23_2 = STRUCT([T([1])([-8.0]), handle_23])
  else:
    handle = MKPOL([[[elem[0],elem[1],0.0],[elem[2],elem[3],0.0]],[[1,2]],[1]])
    handle0 = OFFSET([1.0, 8.0, 1.0])(handle)
    handle_0 = STRUCT([T([1,2,3])([1.0,-2.0,31.0]), handle0])
    handle_1 = STRUCT([T([1,2,3])([3.0,-2.0,31.0]), handle0])
    handle1 = OFFSET([1.0, 1.5, 1.0])(handle)
    handle_2 = STRUCT([T([1,2,3])([1.0,5.0,31.0]), handle1])
    handle_3 = STRUCT([T([1,2,3])([6.0,5.0,31.0]), handle1])
    handle_01 = DIFF([handle_0,handle_1])
    handle_23 = DIFF([handle_2,handle_3])
    handle_23_2 = STRUCT([T([2])([-8.0]), handle_23])
  handle_all = STRUCT([handle_01,handle_23,handle_23_2])
  handle_all = TEXTURE([metalTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(handle_all)
  s1 = STRUCT([s1,handle_all])
  return s1

"""funzione che dati i file lines contenuti nell cartella /params/doors/lines"""
"""costuisce le porte della casa su ogni piano"""
"""utilizza la funzione buildOneDoor(...) e createHandle(...)"""
def buildAllDoors(l,i,h,s1):
  if l <= len(levelDoors)-1:
    if i < len(levelDoors[l]):
      params = parseLines(l,i,levelDoors)
      d = buildOneDoor(params, 0, h, initStruct)
      hand = createHandle(params,initStruct)
      hand = STRUCT([T([3])([h]), hand])
      finalStruct = STRUCT([d, s1, hand])
      return buildAllDoors(l,i+1,h,finalStruct)
    else:
      h = h + 80.0 #se e' una porta tiro su di 60
      return buildAllDoors(l+1,0,h,s1)
  else:
    return s1

"""funzione che dati i parametri costruisce una singola finestra"""
def buildOneWindow(params,h):
  q1 = MKPOL([[[params[0],params[1],0.0],[params[2],params[3],0.0]],[[1,2]],[1]])
  q1 = OFFSET([3.5, 3.5, 30.0])(q1)
  #q1 = STRUCT([T(3)(5.0), q1])
  q1 = TEXTURE([glassTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(q1)
  q1 = MATERIAL([2.55,2.55,2.55,0.5,  0,1,0,0.5, 0,0,1,0, 0,0,0,0.5, 100])(q1)
  if (params[0]-params[2]<1.0) & (params[0]-params[2]>-1.0):
    if params[1]<params[3]:
      q2 = MKPOL([[[params[0],params[1]-2.0,0.0],[params[2],params[3]+2.0,0.0]],[[1,2]],[1]])
      q2 = OFFSET([3.5, 3.5, 40.0])(q2)
    else:
      q2 = MKPOL([[[params[0],params[1]+2.0,0.0],[params[2],params[3]-2.0,0.0]],[[1,2]],[1]])
      q2 = OFFSET([3.5, 3.5, 40.0])(q2)
  if (params[1]-params[3]<1.0) & (params[1]-params[3]>-1.0):
    if params[0]<params[2]:
      q2 = MKPOL([[[params[0]-2.0,params[1],0.0],[params[2]+2.0,params[3],0.0]],[[1,2]],[1]])
      q2 = OFFSET([3.5, 3.5, 40.0])(q2)
    else:
      q2 = MKPOL([[[params[0]+2.0,params[1],0.0],[params[2]-2.0,params[3],0.0]],[[1,2]],[1]])
      q2 = OFFSET([3.5, 3.5, 40.0])(q2)
  q2 = STRUCT([T(3)(-3.5), q2])
  q2 = TEXTURE([doorWindowsTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(q2)
  q = DIFFERENCE([q2,q1])
  q = TEXTURE([doorWindowsTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(q)
  allWindow = STRUCT([q,q1])
  allWindow = STRUCT([T(3)(h), allWindow])
  return allWindow

"""funzione che dati i file lines contenuti nell cartella /params/windows/lines"""
"""costuisce le finestre della casa su ogni piano"""
"""utilizza la funzione buildOneWindow(...)"""
def buildAllWindows(l,i,h,s1):
  if l <= len(levelWindows)-1:
    if i < len(levelWindows[l]):
      params = parseLines(l,i,levelWindows)
      w = buildOneWindow(params,h)
      finalStruct = STRUCT([w, s1])
      return buildAllWindows(l,i+1,h,finalStruct)
    else:
      h = h + 80.0
      return buildAllWindows(l+1,0,h,s1)
  else:
    return s1


"""funzione che dati i file lines contenuti nell cartella /params/base/lines"""
"""costruisce il tetto andando a costruite una travatura di appoggio"""
def buildRoof(i,s1):
  params = parseLines(0,i,levelBase)
  if i==0:
    truss = MKPOL([[[params[0],params[1],0.0],[params[2],params[3],0.0],[(params[2]+params[0])/2,(params[3]+params[1])/2,30.0]],[[1,2,3]],[1]])
    roof_frame = MKPOL([[[params[0],params[1]],[(params[2]+params[0])/2-30.0,(params[3]+params[1])/2]],[[1,2]],[1]])
    truss = OFFSET([-3.0, 0.0, 0.0])(truss)
  else:
      truss = MKPOL([[[params[0],params[1],0.0],[params[2],params[3],0.0],[(params[2]+params[0])/2,(params[3]+params[1])/2,30.0]],[[1,2,3]],[1]])
      roof_frame = MKPOL([[[params[2],params[3]],[(params[2]+params[0])/2-30.0,(params[3]+params[1])/2]],[[1,2]],[1]])
      truss = OFFSET([3.0, 0.0, 0.0])(truss)
  truss = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 2, 1])(truss)
  roof_height = levelBase[0][2]
  roof_height_split = roof_height.split(",")
  roof_height_number = np.array(roof_height_split, dtype=float)
  roof_height = roof_height_number[2] - roof_height_number[0]
  roof = STRUCT([T([1,3])([roof_height_number[0]-8,params[0]-1]),(ROTATE([1,3])(-PI/2)(PROD([roof_frame,Q(roof_height+10)])))])
  roof = OFFSET([3.0, 3.0, 3.0])(roof)
  roof = TEXTURE([roofTexture, TRUE, FALSE, 1, 1, 0, 2, 1])(roof)
  s2 = STRUCT([truss, s1])
  s2 = STRUCT([roof, s2])
  return s2

"""funzione che dati i file lines contenuti nell cartella /params/stair/lines"""
"""crea una nuova base con l'apertura per l'insermento delle scale"""
def buildFloor2(i,base,s1):
  if i < len(levelStair[0]):
    params = parseLines(0,i,levelStair)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([4.0, 5.5, 2.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return buildFloor2(i+1,base,s2)
  else:
    s1 = SOLIDIFY(SKEL_2(s1))
    s1 = DIFF([base,s1])
    s1 = TEXTURE([pavTexture, TRUE, FALSE, 1, 1, 0, 16, 1])(s1)
    return s1

def buildRail(i,z,s1):
  if i < 4:
    params = parseLines(0,i,levelStair)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([1.0, 1.0, z])(a_pol)
    s2 = STRUCT([a_off, s1])
    return buildRail(i+1,z,s2)
  else:
    s1 = TEXTURE([doorWindowsTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(s1)
    return s1

def rail1(params,z,i,s1):
  length = params[3]-params[1]
  if i < length:
    ct = MKPOL([[[params[0],params[1]],[params[2],params[3]-110.0]],[[1,2]],[1]])
    ct = OFFSET([1.0, 1.0, z])(ct)
    ct = STRUCT([T(2)(i),ct])
    ct = TEXTURE([doorWindowsTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(ct)
    s1 = STRUCT([s1, ct])
    return rail1(params,z,i+10,s1)
  else:
    return s1

def rail2(params,z,i,s1):
  length = params[2]-params[0]
  if i < length:
    ct = MKPOL([[[params[0],params[1]],[params[2]-60.0,params[3]]],[[1,2]],[1]])
    ct = OFFSET([1.0, 1.0, z])(ct)
    ct = STRUCT([T(1)(i),ct])
    ct = TEXTURE([doorWindowsTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(ct)
    s1 = STRUCT([s1, ct])
    return rail2(params,z,i+10,s1)
  else:
    return s1

"""funzione che dati i file lines contenuti nell cartella /params/stair/lines"""
"""crea una ringhiera posizionata al secondo piano della casa all'interno del corridoio"""
def buildAllRailing(i,z,s1):
  if i < 4:
    params = parseLines(0,i,levelStair)
    if i!=3:
      c = rail1(params,z,0,s1)
    else:
      c = rail2(params,z,0,s1)
    s1 = STRUCT([s1,c])
    return buildAllRailing(i+1,z,s1)
  else:
    rail = buildRail(1,1.0,initStruct)
    r1=STRUCT([T(3)(1.0),rail])
    r2=STRUCT([T(3)(22.0),rail])
    s1 = STRUCT([r1,s1,r2])
    s1=STRUCT([T(2)(5.0),s1])
    return s1

"""funzione che dati i file lines contenuti nell cartella /params/stair/lines"""
"""crea una scala che porta dal primo al secondo piano"""
def buildStair(tempLength,tempHeight,s1):
  params = parseLines(0,3,levelStair)
  params2 = parseLines(0,0,levelStair)
  height = 80.0
  height_step = 5.44
  steps=height/height_step
  steps=height/steps
  length_step = 13.0
  #length = steps*length_step
  length = (params2[2]-params2[0])
  build = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
  buildOffset = OFFSET([5.0, length_step, height_step])(build)
  traslation=STRUCT([T([1,2,3])([0.5,tempLength+length_step,tempHeight]),buildOffset])
  tempLength=tempLength + length_step/2
  tempHeight=tempHeight + height_step
  s1=STRUCT([traslation,s1])
  if tempHeight < height:
    return buildStair(tempLength, tempHeight, s1)
  else:
    s1 = TEXTURE([doorWindowsTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(s1)
    s1=STRUCT([traslation,s1])
    return s1

"""funzione che date le funzioni elencate sopra si occupa"""
"""della costruzione e assamblaggio di tutta la casa"""
def buildHouse():
  floor1_level = buildFloor1(0,initStruct)
  floor2_level = buildFloor2(0,floor1_level,initStruct)
  external_level = buildExternal(0,0,0.0,initStruct)
  internal_level = buildIntenal(0,0,0.0,initStruct)
  doors_level = buildAllDoors(0,0,0.0,initStruct)
  windows_level = buildAllWindows(0,0,30.0,initStruct)
  roof_level_1 = buildRoof(0,initStruct)
  roof_level_2 = buildRoof(3,initStruct)
  stairs_level = buildStair(0.0,0.0,initStruct)
  railing_level = buildAllRailing(0,21.0,initStruct)
  house=STRUCT([floor1_level,T(3)(3.0),external_level])
  house=STRUCT([house,T(3)(3.5),stairs_level])
  house=STRUCT([house,T(3)(83.0),railing_level])
  house=STRUCT([house,T(3)(3.5),internal_level])
  house=STRUCT([house,T(3)(83.0),floor2_level])
  house=STRUCT([house,T(3)(163.0),floor1_level])
  house=STRUCT([house,T(3)(3.0),doors_level])
  house=STRUCT([house,T(3)(3.0),windows_level])
  house=STRUCT([house,T(3)(163.0),roof_level_1])
  house=STRUCT([house,T(3)(163.0),roof_level_2])
  return house

"""funzione per la costruziones di una o piu' case"""
"""distanziate tra loro"""
def createMoreHouse(i,s1,d):
  if i < 1:
    print(i)
    h1=STRUCT([T([1,2,3])([d,0.0,0.0]),buildHouse()])
    s1= STRUCT([h1, s1])
    return createMoreHouse(i+1,s1,d+600.0)
  else:
    VIEW(s1)

createMoreHouse(0,initStruct,0.0)








