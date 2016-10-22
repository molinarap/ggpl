"""workshop_02"""
from larlib import *

"""
beams_weights ---> lunghezza delle travi tra i pilastri dell'edificio
pilars_heights ---> lunghezza dei pilastri dell'edificio
plan_distance ---> distanza tra un piano e l'altro all'interno dell'edificio
pilar_weight ---> larghezza di un pilastro
beam_weight ---> larghezza delle travi, sempre la metà dei pilastri in modo 
				 che una trave possa sempre poggiare su un pilastro
"""
beams_weights = [4.0, 4.0]
pilars_heights = [5.0, 2.5, 2.5]
plan_distance = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0 ,3.0, 3.0, 3.0, 3.0]
pilar_weight = 0.5 
beam_weight = pilar_weight/2.0

"""
inizializzo una struttura vuota in cui verrà costruito il telaio
"""p0 = CUBOID([0,0,0])
arc = STRUCT([p0])

"""
funzione ricorsiva che crea l'intera struttura andando a creare un piano sull'altro
"""
def createFloor(pilar_height_tot, beam_weight_tot, plan_distance_tot, x, z, y, arc_all):
	if  z < len(pilars_heights): #1
		p1 = COLOR(GREEN)(CUBOID([pilar_weight,pilar_weight,pilars_heights[z]]))
		p1_t = STRUCT([T(1)(plan_distance_tot),T(2)(beam_weight_tot),T(3)(pilar_height_tot), p1])
		t1 = COLOR(RED)(CUBOID([beam_weight,beams_weights[y],beam_weight]))
		t1_t = STRUCT([T([1,2,3])([beam_weight/2.0+plan_distance_tot, (3.0*pilar_weight/4.0)+beam_weight_tot, pilar_height_tot+pilars_heights[z]]), t1])
		if  x < len(plan_distance): #0
			arc_all = STRUCT([arc_all,p1_t,t1_t])
			t2 = COLOR(RED)(CUBOID([plan_distance[x],beam_weight,beam_weight]))
			t2_t = STRUCT([T([1,2,3])([beam_weight/2.0+plan_distance_tot, (pilar_weight/4.0)+beam_weight_tot, pilar_height_tot+pilars_heights[z]]), t2])
			beam_weight_tot=beam_weight_tot+beams_weights[y]+(pilar_weight/2.0)
			if y < len(beams_weights) - 1: #0
				y=y+1
				arc_all = STRUCT([arc_all,t2_t])
				return createFloor(pilar_height_tot, beam_weight_tot, plan_distance_tot, x, z, y, arc_all)
			else:
				p1_next_t = STRUCT([T(1)(plan_distance_tot),T(2)(beam_weight_tot),T(3)(pilar_height_tot), p1])
				t2_next_t = STRUCT([T([1,2,3])([beam_weight/2.0+plan_distance_tot, (pilar_weight/4.0)+beam_weight_tot,pilar_height_tot+pilars_heights[z]]), t2])
				arc_all = STRUCT([arc_all,t2_t,p1_next_t,t2_next_t])
				plan_distance_tot = plan_distance_tot + plan_distance[x]
				x=x+1
				return createFloor(pilar_height_tot, 0, plan_distance_tot, x, z, 0, arc_all)
		else:
			pilar_height_tot = pilar_height_tot + pilars_heights[z] + beam_weight
			z=z+1
			return createFloor(pilar_height_tot, 0, 0, 0, z, 0, arc_all)
	else:
		dist = 0
		for p in plan_distance:
			dist = dist + p
		return createLast(dist, 0, 0, 0, 0, arc_all)

"""
funzione ricorsiva che crea il telaio di chiusura della struttura
"""
def createLastFrame(dist, pilar_height_tot, beam_weight_tot, i, y, arc_all):
	p1 = COLOR(GREEN)(CUBOID([pilar_weight,pilar_weight,pilars_heights[y]]))
	p1_t = STRUCT([T(1)(dist),T(2)(beam_weight_tot),T(3)(pilar_height_tot), p1])
	t1 = COLOR(RED)(CUBOID([beam_weight,beams_weights[i],beam_weight]))
	t1_t = STRUCT([T([1,2,3])([beam_weight/2.0+dist, (3.0*pilar_weight/4.0)+beam_weight_tot,pilar_height_tot+pilars_heights[y]]), t1])
	beam_weight_tot=beam_weight_tot+beams_weights[i]+(pilar_weight/2.0)
	if i == len(beams_weights) - 1:
		p1_next_t = STRUCT([T(1)(dist),T(2)(beam_weight_tot),T(3)(pilar_height_tot), p1])
		pilar_height_tot = pilar_height_tot + pilars_heights[y] + beam_weight
		arc_all = STRUCT([arc_all,p1_t,t1_t,p1_next_t])
		if y != len(pilars_heights) - 1:
			y=y+1
			return createLastFrame(dist, pilar_height_tot, 0, 0, y, arc_all)
		else:
			VIEW(arc_all)
	else:
		i=i+1
		arc_all = STRUCT([arc_all,p1_t,t1_t])
		return createLastFrame(dist, pilar_height_tot, beam_weight_tot, i, y, arc_all)

createFloor(0, 0, 0, 0, 0, 0, arc)

















