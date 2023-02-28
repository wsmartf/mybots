from solution import SOLUTION
import constants as c
import copy
import os
import pyrosim.pyrosim as pyrosim
import numpy as np
import random

class PARALLEL_HILL_CLIMBER:

    def __init__(self, preLoadWeights=False, fileNames=None):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system("rm body*.txt")

        self.parents = {}
        self.nextAvailableID = 0
        self.fitnesses = []

        SOLUTION.Create_World()

        if not preLoadWeights:
            for i in range(c.POPULATION_SIZE):
                self.parents[i] = SOLUTION(self.nextAvailableID)
                self.nextAvailableID += 1
        else:
            for i in range(len(fileNames)):
                self.parents[i] = SOLUTION(self.nextAvailableID, preLoadWeights=True, weightFile=fileNames[i])
                self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)

        for currentGeneration in range(c.NUM_GENERATIONS):
            self.Evolve_For_One_Generation(currentGeneration)
            self.fitnesses.append(self.Best_Parent()[1])

        return self.fitnesses
                
    def Evolve_For_One_Generation(self, currentGeneration):
        self.Spawn()
        self.Mutate()

        self.Evaluate(self.children)
        self.Print(currentGeneration)
        self.Select()

    def Evaluate(self, solutions):

        for el in solutions:
            solutions[el].Start_Simulation("DIRECT")

        for el in solutions:
            solutions[el].Wait_For_Simulation_To_End()
    
    def Spawn(self):
        self.children = {}
        for index in self.parents:
            self.children[index] = copy.deepcopy(self.parents[index])
            self.children[index].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for childIndex in self.children:
            # num_mutations = random.randint(1,self.children[childIndex].num_segments)
            # for i in range(num_mutations):
            self.children[childIndex].Mutate()

    def Select(self):
        for key in self.children:
            if self.parents[key].Get_Fitness() < self.children[key].Get_Fitness():
                self.parents[key] = self.children[key]

    def Print(self, currentGen):
        print(currentGen)
        for el in self.parents:
            print("Parent: ", self.parents[el].Get_Fitness(), "| Child: ", self.children[el].Get_Fitness())
            # print("Parent: ", self.parents[el].weights, "| Child: ", self.children[el].weights)

    def Best_Parent(self):
        best_parent_key = 0
        best_fitness = -1000
        for key in self.parents:
            parent_fitness = self.parents[key].Get_Fitness()
            if parent_fitness > best_fitness:
                best_fitness = parent_fitness
                best_parent_key = key

        return self.parents[best_parent_key], best_fitness  

    def Show_Best(self):
        best_parent, best_fitness = self.Best_Parent()
        best_parent.Start_Simulation("GUI")
        best_parent.Wait_For_Simulation_To_End()
        print("Best fitness: ", best_fitness)

    def Save_Weights(self):
        for parent_key in self.parents:
            parent = self.parents[parent_key]
            self.Save_Weight(parent)

    def Save_Weight(self, parent):
        filename = "weights/" + "id" + str(parent.myID) + "_fit" + str(int(parent.Get_Fitness())) + ".npy"
        np.save(filename, parent.weights)
    
    # def Show_Prev(self, weight_file):
    #     bot = SOLUTION(self.nextAvailableID, True, weight_file)
    #     bot.Start_Simulation("GUI")

