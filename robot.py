import pyrosim.pyrosim as pyrosim
import pybullet as p
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c
import math

class ROBOT:

    def __init__(self, solutionID):
        self.robotId = p.loadURDF("body.urdf")
        self.solutionID = solutionID
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

        brainFile = "brain" + str(self.solutionID) + ".nndf"
        self.nn = NEURAL_NETWORK(brainFile)
        os.system("rm " + brainFile)

        self.stepsInAir = 0
        self.maxStepsInAir = 0
        self.inAirLastStep = False
        self.totalStepsInAir = 0

    def Prepare_To_Sense(self):
        self.sensors = {}

        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, i):

        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        zPos = basePosition[2]

        inAirAndUpright = zPos > 2

        for sensor_name in self.sensors:
            val = self.sensors[sensor_name].Get_Value(i)
            if val != -1:
                inAirAndUpright = False

        if self.inAirLastStep and inAirAndUpright:
            self.stepsInAir += 1
        elif self.inAirLastStep:
            if self.stepsInAir > c.STEPS_IN_AIR_PARAM:
                self.totalStepsInAir += self.stepsInAir
            self.stepsInAir = 0
            self.inAirLastStep = False
        elif inAirAndUpright:
            self.inAirLastStep = True
            self.stepsInAir = 1
        
        if self.stepsInAir > self.maxStepsInAir:
            self.maxStepsInAir = self.stepsInAir

    def Prepare_To_Act(self):
        self.motors = {}

        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)*c.MOTOR_JOINT_RANGE
                self.motors[jointName].Set_Value(desiredAngle, self.robotId)

    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self):

        # basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        # basePosition = basePositionAndOrientation[0]
        # xPosition = basePosition[0]

        weightedFit = 0.6*self.maxStepsInAir+0.4*self.totalStepsInAir

        tmpFileName = "tmp" + str(self.solutionID) + ".txt"
        fitnessFileName = "fitness" + str(self.solutionID) + ".txt"
        file = open(tmpFileName, "w")
        file.write(str(weightedFit))
        file.close()
        os.system("mv " + tmpFileName + " " + fitnessFileName)


    # def Save_Values(self):
    #     for sensor_name in self.sensors:
    #         self.sensors[sensor_name].Save_Values()
    #     for motor_name in self.motors:
    #         self.motors[motor_name].Save_Values()
