""" WORKSHOP 04 """
from pyplasm import *

roofTexture = "texture/roof.jpg"
pavTexture = "texture/pav.jpg"

par = 0.2

x = [
  1.0,  #0
  3.0,  #1
  9.0,  #2
  10.0, #3
  12.0, #4
  14.0, #5
  16.0, #6
  22.0, #7
  24.0, #8
  11.0  #9
]

y = [
  2.0,  #0
  3.0,  #1
  4.0,  #2
  6.0,  #3
  7.0,  #4
  9.0,  #5
  10.0, #6
  12.0, #7
  13.0, #8
  16.0, #9
  14.0  #10
]

z = [
  0.0,  #0
  2.0   #1
]

vertsStruct = [
  [x[0],y[1],z[0]], #1 ---> esterni
  [x[0],y[7],z[0]], #2
  [x[2],y[7],z[0]], #3
  [x[2],y[9],z[0]], #4
  [x[8],y[9],z[0]], #5
  [x[8],y[0],z[0]], #6
  [x[5],y[0],z[0]], #7
  [x[5],y[4],z[0]], #8
  [x[1],y[3],z[1]], #9 ---> interni
  [x[1],y[6],z[1]], #10
  [x[9],y[6],z[1]], #11
  [x[9],y[10],z[1]], #12
  [x[7],y[10],z[1]], #13
  [x[7],y[2],z[1]], #14
  [x[6],y[2],z[1]], #15
  [x[6],y[6],z[1]], #16
]

cellsStruct = [
  [1,2,10,9],
  [2,3,11,10],
  [3,4,12,11],
  [4,5,13,12],
  [5,6,14,13],
  [6,7,15,14],
  [7,8,16,15],
  [8,9,1 ,16]
]

cellsStructBorder = [
  [1,2],
  [2,3],
  [3,4],
  [4,5],
  [5,6],
  [6,7],
  [7,8],
  [8,1]
]


"""creazione primitiva del modello"""
roof = MKPOL([vertsStruct, cellsStruct,[1]])
roof = TEXTURE([roofTexture, TRUE, FALSE, 1, 1, 0, 6, 6])(OFFSET([par, par, par])(SKEL_2(roof)))

paviment = MKPOL([vertsStruct, [[9,10,16],[13,14,15,16],[11,12,13,16]],[1]])
paviment = TEXTURE([pavTexture, TRUE, FALSE, 1, 1, 0, 6, 6])(OFFSET([par, par, par])(SKEL_2(paviment)))

# """assemblo il telaio alla copertura"""
completeRoof = STRUCT([roof, paviment])

VIEW(completeRoof)

