""" WORKSHOP 04 """
from pyplasm import *

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
  24.0  #8
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
  16.0  #9
]

z = [
  0.0,  #0
  2.0   #1
]

vertsStruct = [
  [x[0],y[1],z[0]], #1 ---> esterni
  [x[0],y[7],z[0]], #2
  [x[2],y[7],z[0]], #3
  [x[4],y[9],z[0]], #4
  [x[8],y[5],z[0]], #5
  [x[8],y[0],z[0]], #6
  [x[5],y[0],z[0]], #7
  [x[5],y[4],z[0]], #8
  [x[1],y[3],z[1]], #9 ---> interni
  [x[1],y[6],z[1]], #10
  [x[3],y[6],z[1]], #11
  [x[4],y[8],z[1]], #12
  [x[7],y[4],z[1]], #13
  [x[7],y[2],z[1]], #14
  [x[6],y[2],z[1]], #15
  [x[6],y[6],z[1]], #16
]

cellsStruct = [
  [1,2],
  [2,3],
  [3,4],
  [4,5],
  [5,6],
  [6,7],
  [7,8],
  [8,1],
  [9,10],
  [10,11],
  [11,12],
  [12,13],
  [13,14],
  [14,15],
  [15,16],
  [16,9],
  [1,9],
  [2,10],
  [3,11],
  [4,12],
  [5,13],
  [6,14],
  [7,15],
  [8,16]

]

"""creazione primitiva del modello"""
primitiveRoof = MKPOL([vertsStruct, cellsStruct,[1]])

# """creo il telaio del tetto verificandone la planarieta'"""
# structRoof = OFFSET([par, par, par])(SKEL_1(primitiveRoof))

# """creo una primitiva copertura del tetto adagiata sul telaio che dovra' essere adattata"""
# primitiveRoof_t = STRUCT([T([3])([par*2])(primitiveRoof)])

# """estraggo dalle travi del telaio i nuovi punti per adattare la copertura"""
# coords = UKPOL(primitiveRoof_t)
# vertsRoof = coords[0]
# cellsRoof = coords[1]

# """adatto la copertura in modo da coprire tutto il telaio"""
# vertsRoof = [[x[0],y[2],z[1]+par*2],[x[4],y[3]+par,z[0]+par],[x[4],y[2],z[1]+par*2],[x[0],y[3]+par,z[0]+par],[x[0],y[1]-par,z[0]+par],[x[2],y[2],z[1]+par*2],[x[1]-par,y[1]-par,z[0]+par],[x[0],y[2],z[1]+par*2],[x[4],y[1]-par,z[0]+par],[x[2],y[2],z[1]+par*2],[x[3]+par,y[1]-par,z[0]+par],[x[4],y[2],z[1]+par*2],[x[2],y[0],z[1]+par*2],[x[1]-par,y[1]-par,z[0]+par],[x[1]-par,y[0],z[0]+par],[x[2],y[2],z[1]+par*2],[x[2],y[2],z[1]+par*2],[x[3]+par,y[0],z[0]+par],[x[3]+par,y[1]-par,z[0]+par],[x[2],y[0],z[1]+par*2],[x[0],y[3]+par,z[0]+par],[x[0],y[1]-par,z[0]+par],[x[4],y[3]+par,z[0]+par],[x[4],y[1]-par,z[0]+par],[x[0],y[2],z[1]+par*2],[x[0],y[2],z[0]+par],[x[4],y[2],z[1]+par*2],[x[4],y[2],z[0]+par],[x[3]+par,y[0],z[0]+par],[x[1]-par,y[0],z[0]+par],[x[2],y[2],z[1]+par*2],[x[2],y[2],z[0]+par],[x[2],y[3]+par,z[0]+par],[x[2],y[2],z[1]+par*2],[x[4],y[2],z[0]+par],[x[0],y[2],z[0]+par],[x[2],y[0],z[1]+par*2],[x[2],y[0],z[0]+par]]

# """creo la copertura adattata al telaio in modo che lo ricopra completamente"""
# panelRoof = MKPOL([vertsRoof, cellsRoof,[1]])
# panelRoof = COLOR(BROWN)(OFFSET([par, par, par])(SKEL_2(panelRoof)))

# """assemblo il telaio alla copertura"""
# completeRoof = STRUCT([structRoof, panelRoof])

VIEW(primitiveRoof)

