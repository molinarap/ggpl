""" workshop 10 """
from pyplasm import *
import numpy as np
import sys, os

sys.setrecursionlimit(1500)

pavTexture = "texture/pav2.png"
wallTexture = "texture/wall1.jpg"
wallStone = "texture/wall5.jpg"
doorTexture = "texture/white_wood.jpg"
metalTexture = "texture/metal.jpg"
glassTexture = "texture/glass.jpg"
roofTexture = "texture/roof.jpg"

zero = CUBOID([.0,.0,.0])
initStruct = STRUCT([zero])
level_height = [30.0,30.0,20.0,30.0,30.0,20.0]
heights = [60.0,20.0,3.5,60.0,20.0]

def readSvg(l,reading_level,path):
  file = open("params/"+path+"/lines/level-"+str(l)+".lines","r")
  data = file.read()
  n = len([name for name in os.listdir("params/"+path+"/lines/")])-2
  file.close()
  d = data.splitlines()
  reading_level = reading_level + [d]
  if l<n:
    return readSvg(l+1,reading_level,path)
  else:
    return reading_level

levelBase = readSvg(0,[],"base")
levelExternal = readSvg(0,[],"external")
levelInternal = readSvg(0,[],"internal")
levelDoors = readSvg(0,[],"doors")
levelWindows = readSvg(0,[],"windows")

def buildBase(i,s1):
  if i < len(levelBase[0]):
    a = levelBase[0][i]
    a_split = a.split(",")
    a_number = np.array(a_split, dtype=float)
    a_pol = POLYLINE([[a_number[0],a_number[1]],[a_number[2],a_number[3]]])
    a_off = OFFSET([4.0, 5.5, 2.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return buildBase(i+1,s2)
  else:
    s1 = SOLIDIFY(SKEL_2(s1))
    s1 = TEXTURE([pavTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(s1)
    return s1

def buildExternal(l,i,h,s1):
  if l <= len(levelExternal)-1:
    if i < len(levelExternal[l]):
      a = levelExternal[l][i]
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
      return buildExternal(l,i+1,h,s2)
    else:
      h = h + level_height[l]
      return buildExternal(l+1,0,h,s1)
  else:
    return s1

def buildIntenal(l,i,h,s1):
  if l <= len(levelInternal)-1:
    if i < len(levelInternal[l]):
      a = levelInternal[l][i]
      a_split = a.split(",")
      a_number = np.array(a_split, dtype=float)
      a_pol = MKPOL([[[a_number[0],a_number[1],0.0],[a_number[0],a_number[3],0.0],[a_number[2],a_number[1],0.0],[a_number[2],a_number[3],0.0]],[[1,2,3,4]],[1]])
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

# funzione che costruisce una porta
def buildOneDoor(elem, j, h, door):
  if j < 13:
    build = MKPOL([[[elem[0],elem[1],0.0],[elem[2],elem[3],0.0]],[[1,2]],[1]])
    if not j%2:
      buildOffset = OFFSET([3.5, 3.5, 8.5])(build)
      buildTexture = TEXTURE([pavTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(buildOffset)
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

def buildAllDoors(l,i,h,s1):
  if l <= len(levelDoors)-1:
    if i < len(levelDoors[l]):
      coords = levelDoors[l][i]
      arrayCoords = coords.split(",")
      elem = np.array(arrayCoords, dtype=float)
      d = buildOneDoor(elem, 0, h, initStruct)
      hand = createHandle(elem,initStruct)
      hand = STRUCT([T([3])([h]), hand])
      finalStruct = STRUCT([d, s1, hand])
      return buildAllDoors(l,i+1,h,finalStruct)
    else:
      h = h + 80.0 #se e' una porta tiro su di 60
      return buildAllDoors(l+1,0,h,s1)
  else:
    return s1

def buildOneWindow(elem,h):
  q1 = MKPOL([[[elem[0],elem[1],0.0],[elem[2],elem[3],0.0]],[[1,2]],[1]])
  q1 = OFFSET([3.5, 3.5, 30.0])(q1)
  q1 = TEXTURE([glassTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(q1)
  q1 = STRUCT([T([3])([5.0]), q1])
  if (elem[0]-elem[2]<1.0) & (elem[0]-elem[2]>-1.0):
    if elem[1]<elem[3]:
      q2 = MKPOL([[[elem[0],elem[1]-2,0.0],[elem[2],elem[3]+2,0.0]],[[1,2]],[1]])
    else:
      q2 = MKPOL([[[elem[0],elem[1]+2,0.0],[elem[2],elem[3]-2,0.0]],[[1,2]],[1]])
  if (elem[1]-elem[3]<1.0) & (elem[1]-elem[3]>-1.0):
    if elem[0]<elem[2]:
      q2 = MKPOL([[[elem[0]-2,elem[1],0.0],[elem[2]+2,elem[3],0.0]],[[1,2]],[1]])
    else:
      q2 = MKPOL([[[elem[0]+2,elem[1],0.0],[elem[2]-2,elem[3],0.0]],[[1,2]],[1]])
  q2 = OFFSET([3.5, 3.5, 40.0])(q2)
  q = DIFF([q2,q1])
  q = TEXTURE([pavTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(q2)
  allWindow = STRUCT([q, q1])
  allWindow = STRUCT([T(3)(h), allWindow])
  # if (elem[0]-elem[2]<1.0) & (elem[0]-elem[2]>-1.0):
  #   if elem[1]<elem[3]:
  #     allWindow = STRUCT([T(1)(1.0),allWindow])
  #   else:
  #     allWindow = STRUCT([T(1)(0.0),allWindow])
  # if (elem[1]-elem[3]<1.0) & (elem[1]-elem[3]>-1.0):
  #   if elem[0]<elem[2]:
  #     allWindow = STRUCT([T(2)(1.0),allWindow])
  #   else:
  #     allWindow = STRUCT([T(2)(-1.0),allWindow])
  return allWindow

def buildAllWindows(l,i,h,s1):
  if l <= len(levelWindows)-1:
    if i < len(levelWindows[l]):
      coords = levelWindows[l][i]
      arrayCoords = coords.split(",")
      elem = np.array(arrayCoords, dtype=float)
      w = buildOneWindow(elem,h)
      finalStruct = STRUCT([w, s1])
      return buildAllWindows(l,i+1,h,finalStruct)
    else:
      h = h + 80.0
      return buildAllWindows(l+1,0,h,s1)
  else:
    return s1

def createRoof(n,s1):
  base = levelBase[0][n]
  base_split = base.split(",")
  base_number = np.array(base_split, dtype=float)
  if n==0:
    truss = MKPOL([[[base_number[0],base_number[1],0.0],[base_number[2],base_number[3],0.0],[(base_number[2]+base_number[0])/2,(base_number[3]+base_number[1])/2,30.0]],[[1,2,3]],[1]])
    roof_frame = MKPOL([[[base_number[0],base_number[1]],[(base_number[2]+base_number[0])/2-30.0,(base_number[3]+base_number[1])/2]],[[1,2]],[1]])
    truss = OFFSET([-3.0, 0.0, 0.0])(truss)
  else:
      truss = MKPOL([[[base_number[0],base_number[1],0.0],[base_number[2],base_number[3],0.0],[(base_number[2]+base_number[0])/2,(base_number[3]+base_number[1])/2,30.0]],[[1,2,3]],[1]])
      roof_frame = MKPOL([[[base_number[2],base_number[3]],[(base_number[2]+base_number[0])/2-30.0,(base_number[3]+base_number[1])/2]],[[1,2]],[1]])
      truss = OFFSET([3.0, 0.0, 0.0])(truss)
  truss = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 2, 1])(truss)
  roof_height = levelBase[0][2]
  roof_height_split = roof_height.split(",")
  roof_height_number = np.array(roof_height_split, dtype=float)
  roof_height = roof_height_number[2] - roof_height_number[0]
  roof = STRUCT([T([1,3])([roof_height_number[0]-8,base_number[0]-1]),(ROTATE([1,3])(-PI/2)(PROD([roof_frame,Q(roof_height+10)])))])
  roof = OFFSET([3.0, 3.0, 3.0])(roof)
  roof = TEXTURE([roofTexture, TRUE, FALSE, 1, 1, 0, 2, 1])(roof)
  s2 = STRUCT([truss, s1])
  s2 = STRUCT([roof, s2])
  return s2

def buildHouse():
  a = buildBase(0,initStruct)
  b = buildExternal(0,0,0.0,initStruct)
  c = buildIntenal(0,0,0.0,initStruct)
  d = buildAllDoors(0,0,0.0,initStruct)
  e = buildAllWindows(0,0,30.0,initStruct)
  f = createRoof(0,initStruct)
  g = createRoof(3,initStruct)
  house=STRUCT([a,T(3)(3.0),b])
  house=STRUCT([house,T(3)(3.5),c])
  house=STRUCT([house,T(3)(83.0),a])
  house=STRUCT([house,T(3)(163.0),a])
  house=STRUCT([house,T(3)(3.0),d])
  house=STRUCT([house,T(3)(3.0),e])
  house=STRUCT([house,T(3)(163.0),f])
  house=STRUCT([house,T(3)(163.0),g])
  VIEW(house)

buildHouse()
