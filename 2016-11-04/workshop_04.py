""" WORKSHOP 04 """
from pyplasm import *

par = 0.2

x = [1.0,7.0,11.0,15.0,21.0]
y = [2.0,7.0,12.0,17.0]
z = [0.0, 5.0]

"""rappresentazione sul piano cartesiano del modello da ricreare"""
vertsStruct = [[x[1],y[0],z[0]],[x[2],y[0],z[1]],[x[3],y[0],z[0]],[x[3],y[1],z[0]],[x[4],y[1],z[0]],[x[4],y[2],z[1]],[x[4],y[3],z[0]],[x[0],y[3],z[0]],[x[0],y[2],z[1]],[x[0],y[1],z[0]],[x[1],y[1],z[0]],[x[2],y[2],z[1]],[x[4],y[2],z[0]],[x[0],y[2],z[0]],[x[2],y[2],z[0]],[x[2],y[3],z[0]],[x[2],y[0],z[0]]]
cellsStruct = [[8,7,9,6],[9,10,11,12],[12,4,5,6],[12,11,1,2],[12,2,3,4],[10,8],[7,5],[14,9],[13,6],[1,3],[12,15],[12,16],[13,14],[2,17]]

"""creazione primitiva del modello"""
primitiveRoof = MKPOL([vertsStruct, cellsStruct,[1]])

"""creo il telaio del tetto verificandone la planarieta'"""
structRoof = OFFSET([par, par, par])(SKEL_1(primitiveRoof))

"""creo una primitiva copertura del tetto adagiata sul telaio che dovra' essere adattata"""
primitiveRoof_t = STRUCT([T([3])([par*2])(primitiveRoof)])

"""estraggo dalle travi del telaio i nuovi punti per adattare la copertura"""
coords = UKPOL(primitiveRoof_t)
vertsRoof = coords[0]
cellsRoof = coords[1]

"""adatto la copertura in modo da coprire tutto il telaio"""
vertsRoof = [[x[0],y[2],z[1]+par*2],[x[4],y[3]+par,z[0]+par],[x[4],y[2],z[1]+par*2],[x[0],y[3]+par,z[0]+par],[x[0],y[1]-par,z[0]+par],[x[2],y[2],z[1]+par*2],[x[1]-par,y[1]-par,z[0]+par],[x[0],y[2],z[1]+par*2],[x[4],y[1]-par,z[0]+par],[x[2],y[2],z[1]+par*2],[x[3]+par,y[1]-par,z[0]+par],[x[4],y[2],z[1]+par*2],[x[2],y[0],z[1]+par*2],[x[1]-par,y[1]-par,z[0]+par],[x[1]-par,y[0],z[0]+par],[x[2],y[2],z[1]+par*2],[x[2],y[2],z[1]+par*2],[x[3]+par,y[0],z[0]+par],[x[3]+par,y[1]-par,z[0]+par],[x[2],y[0],z[1]+par*2],[x[0],y[3]+par,z[0]+par],[x[0],y[1]-par,z[0]+par],[x[4],y[3]+par,z[0]+par],[x[4],y[1]-par,z[0]+par],[x[0],y[2],z[1]+par*2],[x[0],y[2],z[0]+par],[x[4],y[2],z[1]+par*2],[x[4],y[2],z[0]+par],[x[3]+par,y[0],z[0]+par],[x[1]-par,y[0],z[0]+par],[x[2],y[2],z[1]+par*2],[x[2],y[2],z[0]+par],[x[2],y[3]+par,z[0]+par],[x[2],y[2],z[1]+par*2],[x[4],y[2],z[0]+par],[x[0],y[2],z[0]+par],[x[2],y[0],z[1]+par*2],[x[2],y[0],z[0]+par]]

"""creo la copertura adattata al telaio in modo che lo ricopra completamente"""
panelRoof = MKPOL([vertsRoof, cellsRoof,[1]])
panelRoof = COLOR(BROWN)(OFFSET([par, par, par])(SKEL_2(panelRoof)))

"""assemblo il telaio alla copertura"""
completeRoof = STRUCT([structRoof, panelRoof])

VIEW(completeRoof)

