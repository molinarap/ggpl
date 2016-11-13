""" workshop 05 """
from pyplasm import *

""" pavimento e muro dell'aula """
wall = CUBOID([5.0,0.1,3.0])
floor = CUBOID([5.0,5.0,0.1])

""" definizione della funzione per la creazione di una lavagna """
def makeBlackboard(boardX,boardY,boardZ,legX,legY,legZ):
	blackboard = COLOR(BLACK)(CUBOID([boardX,boardY,boardZ]))
	board = CUBOID([3.0,0.1,1.5])
	boardBlackboard = COLOR(BROWN)(OFFSET([0.1, 0.1, 0.1])(SKEL_1(board)))
	blackboard = STRUCT([boardBlackboard, blackboard])
	totalBlackboard = STRUCT([T([1,2,3])([0.8,0.05,1.0]), blackboard])
	return totalBlackboard

""" definizione della funzione per la creazione di un banco """
def makeDesk(planX,planY,planZ,legX,legY,legZ):
	tableLeg = CUBOID([legX,legY,legZ])
	couple = STRUCT([tableLeg, T(2)(legZ), tableLeg])
	legs = STRUCT([couple, T(1)(planX), couple])
	plan = COLOR(BROWN)(CUBOID([planX+legX,planY+legY,planZ]))
	desk = STRUCT([legs, T(3)(legZ), plan])
	totalDesk = STRUCT([T([1,2,3])([1.5,2.5,0.0]), desk])
	return totalDesk

""" definizione della funzione per la creazione di una sedia """
def makeChair(legX,legY,legZ,seatX,seatY,seatZ):
	chairLeg = CUBOID([legX,legY,legZ])
	couple = STRUCT([chairLeg, T(2)(seatY), chairLeg])
	legs = STRUCT([couple, T(1)(seatX), couple]) 
	seat = COLOR(BROWN)(CUBOID([seatX+legX,seatY+legY,seatZ]))
	parzChair = STRUCT([legs, T(3)(legZ-seatZ), seat, T(3)(seatZ), couple])
	back = COLOR(BROWN)(CUBOID([legX,seatY-legY,seatZ*2]))
	chair = STRUCT([parzChair, T([1,2,3])([0.02,0.05,0.6]), back])
	totalChair = STRUCT([T([1,2,3])([1.7,3.2,0.0]), chair])
	return totalChair

blackboardStruct= makeBlackboard(3.0,0.1,1.5,0.1,0.1,0.6)
deskStruct = makeDesk(0.8,0.5,0.05,0.05,0.05,0.5)
chairStruct = makeChair(0.05,0.05,0.4,0.3,0.3,0.08)

""" assemblo tutti gli oggetti """
allObj = STRUCT([wall, floor, a, b, c])


VIEW(allObj)
