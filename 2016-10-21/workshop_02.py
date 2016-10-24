"""workshop_02"""
from larlib import *
import csv
import numpy as np

"""
beamsWeights ---> lunghezza delle travi tra i pilastri dell'edificio
pillarsHeights ---> lunghezza dei pilastri dell'edificio
planDistance ---> distanza tra un piano e l'altro all'interno dell'edificio
pillarWeight ---> larghezza di un pilastro
beamWeight ---> larghezza delle travi, sempre la meta' dei pilastri in modo 
				 che una trave possa sempre poggiare su un pilastro
"""

# beamsWeights = [4.0, 4.0]
# pillarsHeights = [5.0, 2.5, 2.5]
# planDistance = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0 ,3.0, 3.0, 3.0, 3.0]
# pillarWeight = 0.5 
# beamWeight = pillarWeight/2.0

"""
leggo le dimensioni delle travi e dei pilastri e le distanze tra esse da un file csv
"""
with open('./data/frame_data_440651.csv', 'rb') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect, delimiter=';')
    for i,row in enumerate(reader):
    	if i == 0:
    		beamsWeights = row
    		beamsWeights = filter(None, beamsWeights)
    		beamsWeights = np.array(beamsWeights, dtype=float)
    		print beamsWeights
    	if i == 1:
    		pillarsHeights = row
    		pillarsHeights = filter(None, pillarsHeights)
    		pillarsHeights = np.array(pillarsHeights, dtype=float)
    		print pillarsHeights
    	if i == 2:
    		planDistance = row
    		planDistance = filter(None, planDistance)
    		planDistance = np.array(planDistance, dtype=float)
    		print planDistance
    	if i == 3:
    		pillarWeight = row[0]
    		pillarWeight = float(pillarWeight)
    	if i == 4:
    		beamWeight = row[0]
    		beamWeight = float(beamWeight)


"""
inizializzo una struttura vuota in cui verra' costruito il telaio
"""
firstPillar = CUBOID([0,0,0])
initStruct = STRUCT([firstPillar])

"""
funzione ricorsiva che crea l'intera struttura andando a creare un piano sull'altro
"""
def createFloor(pillarHeightTot, beamWeightTot, planDistanceTot, x, z, y, struct):
	if  z < len(pillarsHeights): #1
		pillar = COLOR(GREEN)(CUBOID([pillarWeight,pillarWeight,pillarsHeights[z]]))
		pillarT = STRUCT([T(1)(planDistanceTot),T(2)(beamWeightTot),T(3)(pillarHeightTot), pillar])
		beam = COLOR(RED)(CUBOID([beamWeight,beamsWeights[y],beamWeight]))
		beamT = STRUCT([T([1,2,3])([beamWeight/2.0+planDistanceTot, (3.0*pillarWeight/4.0)+beamWeightTot, pillarHeightTot+pillarsHeights[z]]), beam])
		if  x < len(planDistance): #0
			struct = STRUCT([struct,pillarT,beamT])
			t2 = COLOR(RED)(CUBOID([planDistance[x],beamWeight,beamWeight]))
			t2T = STRUCT([T([1,2,3])([beamWeight/2.0+planDistanceTot, (pillarWeight/4.0)+beamWeightTot, pillarHeightTot+pillarsHeights[z]]), t2])
			beamWeightTot=beamWeightTot+beamsWeights[y]+(pillarWeight/2.0)
			if y < len(beamsWeights) - 1: #0
				y=y+1
				struct = STRUCT([struct,t2T])
				return createFloor(pillarHeightTot, beamWeightTot, planDistanceTot, x, z, y, struct)
			else:
				pillarNextT = STRUCT([T(1)(planDistanceTot),T(2)(beamWeightTot),T(3)(pillarHeightTot), pillar])
				t2NextT = STRUCT([T([1,2,3])([beamWeight/2.0+planDistanceTot, (pillarWeight/4.0)+beamWeightTot,pillarHeightTot+pillarsHeights[z]]), t2])
				struct = STRUCT([struct,t2T,pillarNextT,t2NextT])
				planDistanceTot = planDistanceTot + planDistance[x]
				x=x+1
				return createFloor(pillarHeightTot, 0, planDistanceTot, x, z, 0, struct)
		else:
			pillarHeightTot = pillarHeightTot + pillarsHeights[z] + beamWeight
			z=z+1
			return createFloor(pillarHeightTot, 0, 0, 0, z, 0, struct)
	else:
		dist = 0
		for p in planDistance:
			dist = dist + p
		return createLastFrame(dist, 0, 0, 0, 0, struct)

"""
funzione ricorsiva che crea il telaio di chiusura della struttura
"""
def createLastFrame(dist, pillarHeightTot, beamWeightTot, i, y, struct):
	pillar = COLOR(GREEN)(CUBOID([pillarWeight,pillarWeight,pillarsHeights[y]]))
	pillarT = STRUCT([T(1)(dist),T(2)(beamWeightTot),T(3)(pillarHeightTot), pillar])
	beam = COLOR(RED)(CUBOID([beamWeight,beamsWeights[i],beamWeight]))
	beamT = STRUCT([T([1,2,3])([beamWeight/2.0+dist, (3.0*pillarWeight/4.0)+beamWeightTot,pillarHeightTot+pillarsHeights[y]]), beam])
	beamWeightTot=beamWeightTot+beamsWeights[i]+(pillarWeight/2.0)
	if i == len(beamsWeights) - 1:
		pillarNextT = STRUCT([T(1)(dist),T(2)(beamWeightTot),T(3)(pillarHeightTot), pillar])
		pillarHeightTot = pillarHeightTot + pillarsHeights[y] + beamWeight
		struct = STRUCT([struct,pillarT,beamT,pillarNextT])
		if y != len(pillarsHeights) - 1:
			y=y+1
			return createLastFrame(dist, pillarHeightTot, 0, 0, y, struct)
		else:
			VIEW(struct)
	else:
		i=i+1
		struct = STRUCT([struct,pillarT,beamT])
		return createLastFrame(dist, pillarHeightTot, beamWeightTot, i, y, struct)

createFloor(0, 0, 0, 0, 0, 0, initStruct)

















