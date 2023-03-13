from solution import SOLUTION
import constants as c
import copy
import os
import pyrosim.pyrosim as pyrosim

class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system("rm body*.txt")

        self.parents = {}
        self.nextAvailableID = 0
        self.fitnesses = []

        SOLUTION.Create_World()

        for i in range(c.START_POPULATION_SIZE):
                self.parents[i] = SOLUTION(self.nextAvailableID)
                self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)

        for currentGeneration in range(c.NUM_GENERATIONS):
            self.Evolve_For_One_Generation(currentGeneration)
            # save best fitness every 5 generations for plotting
            if currentGeneration % 10 == 0:
                best_fit = self.Best_Parent()[1]
                self.fitnesses.append(best_fit)
                print(f'Gen: {currentGeneration} | Best fit: {best_fit}')
        return self.fitnesses
                
    def Evolve_For_One_Generation(self, currentGeneration):
        self.Spawn()
        self.Mutate()

        self.Evaluate(self.children)
        if c.PRINT:
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
            self.children[childIndex].Mutate()

    def Select(self):
        for key in self.children:
            if self.parents[key].Get_Fitness() < self.children[key].Get_Fitness():
                self.parents[key] = self.children[key]

    def Print(self, currentGen):
        print(f'Gen: {currentGen}')
        for el in self.parents:
            print("Parent: ", self.parents[el].Get_Fitness(), "| Child: ", self.children[el].Get_Fitness())

    def Best_Parent(self):
        best_parent_key = 0
        best_fitness = -1000
        for key in self.parents:
            parent_fitness = self.parents[key].Get_Fitness()
            if parent_fitness > best_fitness:
                best_fitness = parent_fitness
                best_parent_key = key

        return self.parents[best_parent_key], best_fitness  

    def Save_Best(self, show="true", id=0):
        best_parent, best_fitness = self.Best_Parent()
        if show == "true":
            best_parent.Start_Simulation("GUI")
            best_parent.Wait_For_Simulation_To_End()
        best_parent.Save_Bot(id)
        print(f"Best parent: {best_parent.myID} | Best fitness: {best_fitness}")


