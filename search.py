import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
from snake import SNAKE
import matplotlib.pyplot as plt

fit_curves = []

for i in range(5):
    phc = PARALLEL_HILL_CLIMBER()
    fit_curves.append(phc.Evolve())
    phc.Show_Best()

# plot a graph of fitness curves
for i in range(len(fit_curves)):
    plt.plot(fit_curves[i])

plt.show()