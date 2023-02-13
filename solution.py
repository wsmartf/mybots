import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c

class SOLUTION:

    def __init__(self, nextAvailableID=0, preLoadWeights=False, weightFile=None):
        self.myID = nextAvailableID
        self.sensor_links = []
        self.joints = []
        self.preLoadWeights = preLoadWeights
        self.weightFile = weightFile

    def weights_init(self):
        if not self.preLoadWeights:
            self.weights = np.random.rand(len(self.sensor_links),c.NUM_SEGMENTS)*2-1
        else:
            self.weights = np.load(self.weightFile)

    def Start_Simulation(self, directOrGUI):
        # self.Create_Brain()
        # systemCommand = "python3 simulate.py " + directOrGUI + " " + str(self.myID) + " 2&>1 &"
        systemCommand = "python3 simulate.py " + directOrGUI + " " + str(self.myID) + " &"

        os.system(systemCommand)

    def Wait_For_Simulation_To_End(self):
        # fitnessFileName = "fitness" + str(self.myID) + ".txt"
        # while not os.path.exists(fitnessFileName):
        #     time.sleep(0.01)

        # file = open(fitnessFileName, "r")
        # self.fitness = float(file.read())
        # file.close()
        # # print(self.fitness)
        # os.system("rm " + fitnessFileName)
        pass
    
    # def Mutate(self):
    #     row1 = random.randint(0,c.NUM_SENSOR_NEURONS-1)
    #     col1 = random.randint(0,c.NUM_MOTOR_NEURONS-1)
    #     self.weights[row1, col1] = random.random()*2-1

    def Set_ID(self, newID):
        self.myID = newID

    def Get_Fitness(self):
        return self.fitness  

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()   

    def CreateRandomBot(self):

        # Body
        pyrosim.Start_URDF("body.urdf")

        seg_size = [random.uniform(c.MIN_RAND, c.MAX_RAND), random.uniform(c.MIN_RAND, c.MAX_RAND), random.uniform(c.MIN_RAND, c.MAX_RAND)]
        seg_pos = [0, 0, c.MAX_RAND/2]

        has_sensor = True if random.randint(0, 1) == 1 else False
        if has_sensor:
            color_name="Green"
            rgb=[0,1,0]
            self.sensor_links.append("Head")
        else:
            color_name="Blue"
            rgb=[0,0,1]

        pyrosim.Send_Cube(name="Head", pos=seg_pos, size=seg_size, color_name=color_name, rgb=rgb)

        parent_name = "Head"
        parent_size = seg_size

        for i in range(c.NUM_SEGMENTS):
            name = str(i)

            has_sensor = True if random.randint(0, 1) == 1 else False
            if has_sensor: self.sensor_links.append(name)
            
            size = self.CreateRandomSegment(name, i, parent_name, parent_size, has_sensor)
            parent_name = name
            parent_size = size

        pyrosim.End()

        self.weights_init()

        # Brain
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        for i in range(len(self.sensor_links)):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = self.sensor_links[i])

        for j in range(len(self.joints)):
            pyrosim.Send_Motor_Neuron(name = j+len(self.sensor_links), jointName = self.joints[j])

        for currentRow in range(len(self.sensor_links)):
            for currentColumn in range(len(self.joints)):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow,
                                    targetNeuronName = currentColumn+len(self.sensor_links), 
                                    weight = self.weights[currentRow][currentColumn])

        pyrosim.End()
        
    def CreateRandomSegment(self, seg_name, i, parent_name, parent_size, has_sensor):
        seg_size = [random.uniform(c.MIN_RAND, c.MAX_RAND), random.uniform(c.MIN_RAND, c.MAX_RAND), random.uniform(c.MIN_RAND, c.MAX_RAND)]
        joint_name = parent_name + "_" + seg_name
        self.joints.append(joint_name)
        joint_pos = [0, parent_size[1]/2, c.MAX_RAND/2] if i == 0 else [0, parent_size[1], 0]

        # joint_axis_int = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
        # joint_axis = str(joint_axis_int[0]) + " " + str(joint_axis_int[1]) + " " + str(joint_axis_int[2])
        joint_axis = "0 0 1"
        pyrosim.Send_Joint(name=joint_name, parent=parent_name, child=seg_name, type="revolute", position=joint_pos, jointAxis=joint_axis)
        if has_sensor:
            color_name="Green"
            rgb=[0,1,0]
        else:
            color_name="Blue"
            rgb=[0,0,1]
        pyrosim.Send_Cube(name=seg_name, pos=[0, seg_size[1]/2, 0] , size=seg_size, color_name=color_name, rgb=rgb)

        return seg_size
