import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c

class SOLUTION:

    def __init__(self, nextAvailableID, preLoadWeights=False, weightFile=None):
        self.myID = nextAvailableID
        self.sensor_links = []
        self.joints = []
        self.preLoadWeights = preLoadWeights
        self.weightFile = weightFile
        self.links = []
        self.num_segments = random.randint(2,7)
        
        self.CreateRandomBot()
        self.weights_init()

        print("sensor_links: ", self.sensor_links)
        print("joints: ", self.joints)
        print("weights: ", self.weights)
        print("shape: ", self.weights.shape)
       

    def weights_init(self):
        if not self.preLoadWeights:
            self.weights = np.random.rand(len(self.sensor_links),len(self.joints))*2-1
        else:
            self.weights = np.load(self.weightFile)

    def Start_Simulation(self, directOrGUI):
        # systemCommand = "python3 simulate.py " + directOrGUI + " " + str(self.myID) + " 2&>1 &"
        self.Create_Brain()
        systemCommand = "python3 simulate.py " + directOrGUI + " " + str(self.myID) + " &"

        os.system(systemCommand)

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)

        file = open(fitnessFileName, "r")
        self.fitness = float(file.read())
        file.close()
        # print(self.fitness)
        os.system("rm " + fitnessFileName)
    
    def Mutate(self):
        row1 = random.randint(0,len(self.sensor_links)-1)
        # print("num s links: ", len(self.sensor_links), " row1: ", row1)

        col1 = random.randint(0,len(self.joints)-1)
        # print("num joints: ", len(self.joints), " row2: ", col1)

        self.weights[row1, col1] = random.random()*2-1

    def Set_ID(self, newID):
        self.myID = newID

    def Get_Fitness(self):
        return self.fitness  
    
    @(staticmethod)
    def Create_World():
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
        parent_blocked_direction = None

        for i in range(self.num_segments):
            name = str(i)

            has_sensor = True if random.randint(0, 1) == 1 else False
            if has_sensor: self.sensor_links.append(name)
            
            size, blocked_direction = self.CreateRandomSegment(name, i, parent_name, parent_size, has_sensor, parent_blocked_direction)
            parent_name = name
            parent_size = size
            parent_blocked_direction = blocked_direction

        pyrosim.End()

        # self.weights_init()

    def Create_Brain(self):
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

        
    def CreateRandomSegment(self, seg_name, i, parent_name, parent_size, has_sensor, blocked_direction):
        
        seg_size = [random.uniform(c.MIN_RAND, c.MAX_RAND), random.uniform(c.MIN_RAND, c.MAX_RAND), random.uniform(c.MIN_RAND, c.MAX_RAND)]
        joint_name = parent_name + "_" + seg_name
        self.joints.append(joint_name)

        joint_axis = random.choice(["0 0 1", "0 1 0", "1 0 0"])

        directions = [3, -3, 2, -2, 1, -1] # x, -x, y, -y, z, -z
        prev_sign = 1
        prev_dir = 3

        if blocked_direction is not None:
            directions.remove(blocked_direction)
            prev_sign = np.sign(blocked_direction)
            prev_dir = abs(blocked_direction)
        direction = random.choice(directions)
        
        rand = random.uniform(-1, 1)
        sign = np.sign(direction)
        dir = abs(direction)

        for i in range(2):
            if dir != prev_dir:
                direction = random.choice(directions)
            else:
                break
        
        if dir == 2: #y
            if i==0:
                joint_pos = [0, sign*parent_size[1]/2, c.MAX_RAND/2]
            else:
                if prev_dir == 2:
                    joint_pos=[0, sign*parent_size[1], 0]
                else:
                    if prev_dir == 3: # x
                        if prev_sign == sign:
                            joint_pos = [sign*parent_size[0]/2, sign*parent_size[1]/2, 0]
                        else:
                            joint_pos = [prev_sign*parent_size[0]/2, sign*parent_size[1]/2, 0]
                    else: # z
                        if prev_sign == sign:
                            joint_pos = [0, sign*parent_size[1]/2, sign*parent_size[2]/2]
                        else:
                            joint_pos = [0, sign*parent_size[1]/2, prev_sign*parent_size[2]/2]
            cube_pos = [0, sign*seg_size[1]/2, 0] 
        elif dir == 3: # x
            if i==0:
                joint_pos = [sign*parent_size[0]/2, 0, c.MAX_RAND/2]
            else:
                if prev_dir == 3:
                    joint_pos = [sign*parent_size[0], 0, 0]
                else:
                    if prev_dir == 2: # y
                        if prev_sign == sign:
                            joint_pos = [sign*parent_size[0]/2, sign*parent_size[1]/2, 0]
                        else:
                            joint_pos = [sign*parent_size[0]/2, prev_sign*parent_size[1]/2, 0]
                    else: # z
                        if prev_sign == sign:
                            joint_pos = [sign*parent_size[0]/2, 0, sign*parent_size[2]/2]
                        else:
                            joint_pos = [sign*parent_size[0]/2, 0, prev_sign*parent_size[2]/2]
            cube_pos = [sign*seg_size[0]/2, 0, 0]
        elif dir == 1: # z
            if i==0:
                joint_pos = [0, 0, parent_size[2]/2+c.MAX_RAND/2]
                cube_pos = [0, 0, seg_size[2]/2]
            else:
                if prev_dir == 1:
                    joint_pos = [0, 0, sign*parent_size[2]]
                else:
                    if prev_dir == 2: # y
                        if prev_sign == sign:
                            joint_pos = [0, sign*parent_size[1]/2, sign*parent_size[2]/2]
                        else:
                            joint_pos = [0, prev_sign*parent_size[1]/2, sign*parent_size[2]/2]
                    else: # x
                        if prev_sign == sign:
                            joint_pos = [sign*parent_size[0]/2, 0, sign*parent_size[2]/2]
                        else:
                            joint_pos = [prev_sign*parent_size[0]/2, 0, sign*parent_size[2]/2]
                cube_pos = [0, 0, sign*seg_size[2]/2]

        new_blocked_direction = direction*-1

        pyrosim.Send_Joint(name=joint_name, parent=parent_name, child=seg_name, type="revolute", position=joint_pos, jointAxis=joint_axis)
        
        if has_sensor:
            color_name="Green"
            rgb=[0,1,0]
        else:
            color_name="Blue"
            rgb=[0,0,1]
        pyrosim.Send_Cube(name=seg_name, pos=cube_pos, size=seg_size, color_name=color_name, rgb=rgb)

        return seg_size, new_blocked_direction
