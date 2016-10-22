# workshop_01
from larlib import *

beams_weights = [3.0, 3.0, 3.0]
pilars_heights = [5.0, 3.0, 3.0, 3.0, 2.0]
plan_distance = [3.0, 5.0, 3.0, 3.0, 2.0]
pilar_weight = 0.5 
beam_weight = pilar_weight/2.0

# inizializzo una struttura base da cui partire
p0 = CUBOID([0,0,0])
arc = STRUCT([p0])

# funzione che crea il telaio piano
def createFloor(pilar_height_tot, beam_weight_tot, i, y, arc_all):
	p1 = CUBOID([pilar_weight,pilar_weight,pilars_heights[y]])
	p1_t = STRUCT([T(2)(beam_weight_tot),T(3)(pilar_height_tot), p1])
	t1 = CUBOID([beam_weight,beams_weights[i],beam_weight])
	t1_t = STRUCT([T([1,2,3])([beam_weight/2.0, (3.0*pilar_weight/4.0)+beam_weight_tot,pilar_height_tot+pilars_heights[y]]), t1])
	beam_weight_tot=beam_weight_tot+beams_weights[i]+(pilar_weight/2.0)
	if i == len(beams_weights) - 1:
		p1_next_t = STRUCT([T(2)(beam_weight_tot),T(3)(pilar_height_tot), p1])
		pilar_height_tot = pilar_height_tot + pilars_heights[y] + beam_weight
		arc_all = STRUCT([arc_all,p1_t,t1_t,p1_next_t])
		if y != len(pilars_heights) - 1:
			y=y+1
			return createFloor(pilar_height_tot, 0, 0, y, arc_all)
		else:
			VIEW(arc_all)
	else:
		i=i+1
		arc_all = STRUCT([arc_all,p1_t,t1_t])
		return createFloor(pilar_height_tot, beam_weight_tot, i, y, arc_all)

createFloor(0, 0, 0, 0, arc)



















