# workshop_01
from larlib import *


beams_weight = [2.0, 5.0, 10.0, 3.0]
pilars_height = [3.0, 3.0, 3.0]
pilar_space_tot=0

p0 = CUBOID([0,0,0])
arc_all = STRUCT([p0])
pilar_height_tot=0

for y,p in enumerate(pilars_height):
	p1 = CUBOID([1,1,p])
	beam_weight_tot=0
	if y!=0:
			p1_t = STRUCT([T(3)(pilar_height_tot+1), p1])
			arc_all = STRUCT([arc_all,p1_t])
	else:
			arc_all = STRUCT([arc_all,p1])
	
	pilar_height_tot= pilar_height_tot + p

	for i,b in enumerate(beams_weight):
		t1_next = CUBOID([1,b,1])
		if i==0:
			if(y==0):
				t1_next_t = STRUCT([T(2)(0.5),T(3)(pilar_height_tot), t1_next])
			else:
				t1_next_t = STRUCT([T(2)(0.5),T(3)(pilar_height_tot+1), t1_next])
		else:
			if(y==0):
				t1_next_t = STRUCT([T(2)(beam_weight_tot+0.5),T(3)(pilar_height_tot), t1_next])
			else:
				t1_next_t = STRUCT([T(2)(beam_weight_tot+0.5),T(3)(pilar_height_tot+1), t1_next])
		beam_weight_tot = beam_weight_tot + b
		p1_next = CUBOID([1,1,p])
		if(y==0):
			p1_next_t = STRUCT([T(2)(beam_weight_tot), p1_next])
		else:
			p1_next_t = STRUCT([T(2)(beam_weight_tot),T(3)(pilar_height_tot-p+1), p1_next])
		arc = STRUCT([p1_next_t,t1_next_t])
		arc_all = STRUCT([arc_all,arc])


VIEW(arc_all)

# # for hz 
# for y, pilar_height in enumerate(pilars_height):
# 	if y!=0:
# 		pilar_space_tot = pilar_space_tot + pilars_height[y-1] + 1
# 	beam_space_tot = 0 # somma della lunghezza di tutte le travi
# 	for i, beam_weight in enumerate(beams_weight):
# 		beam_space = beam_weight - 1
# 		beam_space_tot = beam_space_tot + beam_weight
# 		if i==0:
# 			p1_dx = CUBOID([1,1,pilars_height[0]])
# 			p1_sx = CUBOID([1,1,pilars_height[0]])
# 			p1_all = STRUCT([p1_dx, T(2)(beam_space + 1), p1_sx])
# 			t1 = CUBOID([1,beam_weight,1])
# 			t1_t = STRUCT([T(2)(0.5), t1])
# 			arc1 = STRUCT([p1_all, T(3)(pilars_height[0]), t1_t])
# 			arc_all = STRUCT([arc_all,arc1])
# 		if i+1<len(beams_weight):
# 			beam_weight_next = beams_weight[i+1];
# 			p1_next = CUBOID([1,1,pilar_height])
# 			p1_next_t = STRUCT([T(2)(beam_weight_next), p1_next])
# 			t1_next = CUBOID([1,beam_weight_next,1])
# 			t1_next_t = STRUCT([T(2)(0.5), t1_next])
# 			arc1_next = STRUCT([p1_next_t, T(3)(pilar_height),t1_next_t])
# 			arc1_next_t = STRUCT([T(2)(beam_space_tot),arc1_next])
# 			arc_all = STRUCT([arc_all,arc1_next_t])

# 	arc_all2 = STRUCT([arc_all2,T(3)(pilar_space_tot),arc_all])


# VIEW(arc_all2)
