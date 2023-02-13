from solution import SOLUTION
import constants as c
import copy
import os
import pyrosim.pyrosim as pyrosim
import numpy as np
import random

class SNAKE:

    def __init__(self):
        self.snake = SOLUTION()
        self.snake.Create_World()
        self.snake.CreateRandomBot()
        

    def Simulate(self):
        # self.snake.CreateRandomBot()
        self.snake.Start_Simulation("GUI")
