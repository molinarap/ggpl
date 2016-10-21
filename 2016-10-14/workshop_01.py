# workshop_01
from larlib import *

beams_weight = [3.0, 3.0, 3.0, 3.0, 3.0]
pilars_height = [5.0, 3.0, 3.0, 3.0, 2.0]
pilars_weight = 0.5

# inizializzo una struttura base da cui partire
p0 = CUBOID([0,0,0])
arc = STRUCT([p0])

# funzione che crea il telaio piano
def createFloor(pilar_height_tot, beam_weight_tot, i, y, arc_all):
	p1 = CUBOID([pilars_weight,pilars_weight,pilars_height[y]])
	p1_t = STRUCT([T(2)(beam_weight_tot),T(3)(pilar_height_tot), p1])
	t1 = CUBOID([pilars_weight,beams_weight[i],pilars_weight])
	t1_t = STRUCT([T([1,2,3])([0, (pilars_weight/2.0)+beam_weight_tot,pilar_height_tot+pilars_height[y]]), t1])
	beam_weight_tot=beam_weight_tot+beams_weight[i]
	if i == len(beams_weight) - 1:
		p1_next_t = STRUCT([T(2)(beam_weight_tot),T(3)(pilar_height_tot), p1])
		arc_all = STRUCT([arc_all,p1_t,t1_t,p1_next_t])
		pilar_height_tot = pilar_height_tot + pilars_height[y] + pilars_weight
		if y == len(pilars_height) - 1:
			VIEW(arc_all)
		else:
			y=y+1
			return createFloor(pilar_height_tot, 0, 0, y, arc_all)
	else:
		i=i+1
		arc_all = STRUCT([arc_all,p1_t,t1_t])
		return createFloor(pilar_height_tot, beam_weight_tot, i, y, arc_all)

createFloor(0, 0, 0, 0, arc)


