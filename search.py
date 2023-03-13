import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import matplotlib.pyplot as plt
import random
import constants as c
import argparse
import time

def show_bot_i(i, save_dir):
    os.system(f"python3 simulate.py GUI {str(i)} {str(save_dir)}")

    fitnessFileName = "fitness" + str(i) + ".txt"
    while not os.path.exists(fitnessFileName):
        time.sleep(0.01)

    file = open(fitnessFileName, "r")
    fitness = float(file.read())
    file.close()
    os.system("rm " + fitnessFileName)
    print(f"Robot {i} fitness: {fitness}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-mode', type=str, default='evolve') # evolve, load
    parser.add_argument('-show_best_each_run', type=str, default='true')
    parser.add_argument('-save_dir', type=str, default='save')
    parser.add_argument('-load_dir', type=str, default='savedbots1000gen')
    parser.add_argument('-bot_num', type=int, default=-1)


    params = parser.parse_args()

    # Evolve a new population of robots, save the best one from each run, and show it
    # Modify constants.py to change the number of runs, population size, etc.
    if params.mode == 'evolve':   
        fit_curves = []
        best_fitness = -1000
        best_run = 0

        for i in range(c.NUM_RUNS):
            print(f"Run {i}")
            random.seed(i)
            phc = PARALLEL_HILL_CLIMBER()
            fit_curves.append(phc.Evolve())
            phc.Save_Best(show=params.show_best_each_run, id=i)

            fitness = fit_curves[-1][-1]
            if fitness > best_fitness:
                best_fitness = fitness
                best_run = i
        
        # Show best overall bot
        show_bot_i(i=best_run, save_dir=params.save_dir)

        # plot a graph of fitness curves
        for i in range(len(fit_curves)):
            plt.plot(fit_curves[i])
        plt.savefig("fitness_curves.png")
    
    else:
        if params.bot_num == -1:
            for i in range(c.NUM_RUNS):
                show_bot_i(i, save_dir=params.load_dir)
        else:
            show_bot_i(i=params.bot_num, save_dir=params.load_dir)
        
if __name__ == "__main__": 
    main()