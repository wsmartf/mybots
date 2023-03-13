from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
loadDir = sys.argv[3]

loadDir = None if loadDir == "none" else loadDir

simulation = SIMULATION(directOrGUI, solutionID, loadDir)
simulation.Run()
simulation.Get_Fitness()