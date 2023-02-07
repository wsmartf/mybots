import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER

phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()

### Uncomment to demo evolved robots ###
# r1 = "weights/evolvedBots/id2287_fit538.npy"
# r2 = "weights/evolvedBots/id6_fit463.npy"
# r3 = "weights/evolvedBots/id1904_fit413.npy"
# r4 = "weights/evolvedBots/id82_fit325.npy"
# r5 = "weights/evolvedBots/id1690_fit370.npy"
# r6 = "weights/evolvedBots/id737_fit389.npy"

# phc = PARALLEL_HILL_CLIMBER()
# phc.Show_Prev(r1)
### --------------------------------- ###


### Uncomment to continue evolving from stored weights ###
# folderName = "weights/evolvedBots"
# weightFiles = [(folderName + f) for f in os.listdir(folderName)]
# print(weightFiles)
# phc = PARALLEL_HILL_CLIMBER(preLoadWeights=True, fileNames=weightFiles)
# phc.Evolve()
# phc.Show_Best()
### ---------------------------------- ###

