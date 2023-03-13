import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c
from link import LINK
from simulation import SIMULATION

class SOLUTION:

    def __init__(self, nextAvailableID):
        self.rootID = nextAvailableID
        self.myID = nextAvailableID
        self.sensor_links = []
        self.joints = []
        self.num_segments = random.randint(c.MIN_RAND_SEGMENTS,c.MAX_RAND_SEGMENTS)
        self.weights = None
        self.is_first_instance = True
        self.links = []
        self.saveFiles = False
        self.doSave = False
    
    def Save_Bot(self, id):
        brainfile = "save/brain" + str(id) + ".nndf"
        bodyfile = "save/body" + str(id) + ".urdf"
        self.GenerateBody(bodyfile)
        self.Create_Brain(brainfile)
        
    def weights_init(self):
            self.weights = np.random.rand(len(self.sensor_links),len(self.joints))*2-1

    def Start_Simulation(self, directOrGUI):
        if self.is_first_instance:
            self.CreateRandomBot()
            self.weights_init()
            self.is_first_instance = False
        else:
            self.GenerateBody()
        self.Create_Brain()
        
        systemCommand = "python3 simulate.py " + directOrGUI + " " + str(self.myID) + " none 2&>1 &"
        os.system(systemCommand)

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)

        file = open(fitnessFileName, "r")
        self.fitness = float(file.read())
        file.close()
        os.system("rm " + fitnessFileName)
    
    def Mutate(self):
        for i in range(random.randint(3,10)):
            row1 = random.randint(0,len(self.sensor_links)-1)
            col1 = random.randint(0,len(self.joints)-1)
            if random.random() < 0.5:
                self.weights[row1, col1] = random.random()*2-1
            else:
                w = self.weights[row1, col1]
                new_w = w*random.uniform(0.8, 1.2)
                if new_w > -1 and new_w < 1:
                    self.weights[row1, col1] = new_w
            
        for i in range(len(self.links)):
            if i > 1:
                self.links[i].mutate()


    def Set_ID(self, newID):
        self.myID = newID

    def Get_Fitness(self):
        return self.fitness  
    
    @(staticmethod)
    def Create_World():
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()   

    def hasSensor(self, i, seg_name):
        if i == self.num_segments-1 and len(self.sensor_links) == 0:
            has_sensor = True
        else:
            has_sensor = True if random.randint(0, 1) == 1 else False
        
        if has_sensor:
            color_name="Green"
            rgb=[0,1,0]
            if self.is_first_instance: self.sensor_links.append(seg_name)
        else:
            color_name="Blue"
            rgb=[0,0,1]
        return color_name, rgb
    
    def GenerateBody(self, fileName=None):
        if fileName is None:
            pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")
        else:
            pyrosim.Start_URDF(fileName)

        for i in range(len(self.links)):
            link = self.links[i]
            if link.isRoot:
                pyrosim.Send_Cube(name=link.seg_name, pos=link.cube_pos, size=link.seg_size, color_name=link.color_name, rgb=link.rgb)
            else:
                pyrosim.Send_Joint(name=link.joint_name, parent=link.parent_name, child=link.seg_name, type="revolute", position=link.joint_pos, jointAxis=link.joint_axis)
                pyrosim.Send_Cube(name=link.seg_name, pos=link.cube_pos, size=link.seg_size, color_name=link.color_name, rgb=link.rgb)

        pyrosim.End()

    
    def CreateRandomBot(self):
        pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")

        # Create first "head" link
        seg_size = [random.uniform(c.MIN_RAND, c.MAX_RAND), random.uniform(c.MIN_RAND, c.MAX_RAND), random.uniform(c.MIN_RAND, c.MAX_RAND)]
        cube_pos = [0, 0, c.MAX_RAND/2]
        color_name, rgb = self.hasSensor(0, "0")
        pyrosim.Send_Cube(name="0", pos=cube_pos, size=seg_size, color_name=color_name, rgb=rgb)
        parent_link = LINK(seg_name="0", seg_size=seg_size, cube_pos=cube_pos, color_name=color_name, rgb=rgb, isRoot=True)
        self.links.append(parent_link)

        parent_name = "0"
        parent_size = seg_size
        prev_dir = 0
        i = 1
        for i in range(1, self.num_segments):
            size, dir, link = self.CreateRandomSegment(i, parent_name, parent_size, prev_dir, parent_link)
            parent_name = str(i)
            parent_size = size
            prev_dir = dir
            parent_link = link
        pyrosim.End()
        
    def CreateRandomSegment(self, i, parent_name, parent_size, prev_dir, parent_link):
    
        dirs = [0, 1, 2]
        dir = random.choice(dirs)
        dir2 = None
        if random.random() < 0.5:
            dirs.remove(dir)
            dir2 = random.choice(dirs)

        seg_name = str(i)
        joint_name = parent_name + "_" + seg_name
        if self.is_first_instance: self.joints.append(joint_name)
        
        def branch_in_dir(parent_size, seg_name, dir, prev_dir, i, addl):
            if addl:
                seg_size = [random.uniform(c.MIN_RAND, c.MAX_RAND/1.5), random.uniform(c.MIN_RAND, c.MAX_RAND/1.5), random.uniform(c.MIN_RAND, c.MAX_RAND/1.5)]
            else:
                seg_size = [random.uniform(c.MIN_RAND, c.MAX_RAND), random.uniform(c.MIN_RAND, c.MAX_RAND), random.uniform(c.MIN_RAND, c.MAX_RAND)]

            color_name, rgb = self.hasSensor(i, seg_name)

            joint_axis = random.choice(["0 0 1", "0 1 0", "1 0 0"])
            if dir == 0: # x
                if i==1:
                    joint_pos = [parent_size[0]/2, 0, c.MAX_RAND/2]
                else:
                    if prev_dir == 0:
                        joint_pos = [parent_size[0], 0, 0]
                    elif prev_dir == 1:
                        joint_pos = [parent_size[0]/2, parent_size[1]/2, 0]
                    else:  # prev_dir == 2
                        joint_pos = [parent_size[0]/2, 0, parent_size[2]/2]
                seg_size = [seg_size[0]*2, seg_size[1], seg_size[2]]
                cube_pos = [seg_size[0]/2, 0, 0]
            elif dir == 1: # y
                if i==1:
                    joint_pos = [0, parent_size[1]/2, c.MAX_RAND/2]
                else:
                    if prev_dir == 1:
                        joint_pos = [0, parent_size[1], 0]
                    elif prev_dir == 0:
                        joint_pos = [parent_size[0]/2, parent_size[1]/2, 0]
                    else: # prev_dir == 2
                        joint_pos = [0, parent_size[1]/2, parent_size[2]/2]
                seg_size = [seg_size[0], seg_size[1]*2, seg_size[2]]
                cube_pos = [0, seg_size[1]/2, 0]
            else: # dir == 2,z
                if i==1:
                    joint_pos = [0, 0, c.MAX_RAND/2+parent_size[2]/2]
                else:
                    if prev_dir == 2:
                        joint_pos = [0, 0, parent_size[2]]
                    elif prev_dir == 1:
                        joint_pos = [0, parent_size[1]/2, parent_size[2]/2]
                    else:  # prev_dir == 0
                        joint_pos = [parent_size[0]/2, 0, parent_size[2]/2]
                seg_size = [seg_size[0], seg_size[1], seg_size[2]*2]
                cube_pos = [0, 0, seg_size[2]/2]

            return joint_pos, joint_axis, seg_size, cube_pos, color_name, rgb
        
        joint_pos, joint_axis, seg_size, cube_pos, color_name, rgb = branch_in_dir(parent_size, seg_name, dir, prev_dir, i, False)
        link_addl = None
        if dir2 is not None:
            seg_name2 = str(i) + "addl"
            joint_name2 = parent_name + "_" + seg_name2
            if self.is_first_instance: self.joints.append(joint_name2)

            joint_pos2, joint_axis2, seg_size2, cube_pos2, color_name2, rgb2 = branch_in_dir(parent_size, parent_name, dir2, prev_dir, i, True)
            pyrosim.Send_Joint(name=joint_name2, parent=parent_name, child=seg_name2, type="revolute", position=joint_pos2, jointAxis=joint_axis2)
            pyrosim.Send_Cube(name=seg_name2, pos=cube_pos2, size=seg_size2, color_name=color_name2, rgb=rgb2)
            link_addl = LINK(seg_name=seg_name2, parent_size=parent_size, seg_size=seg_size2, cube_pos=cube_pos2, color_name=color_name2, rgb=rgb2, isRoot=False, parent_name=parent_name, joint_name=joint_name2, joint_pos=joint_pos2, joint_axis=joint_axis2, dir=dir2, prev_dir=prev_dir)
            self.links.append(link_addl)
        
        pyrosim.Send_Joint(name=joint_name, parent=parent_name, child=seg_name, type="revolute", position=joint_pos, jointAxis=joint_axis)
        pyrosim.Send_Cube(name=seg_name, pos=cube_pos, size=seg_size, color_name=color_name, rgb=rgb)
        link = LINK(seg_name=seg_name, parent_size=parent_size, seg_size=seg_size, cube_pos=cube_pos, color_name=color_name, rgb=rgb, isRoot=False, parent_name=parent_name, joint_name=joint_name, joint_pos=joint_pos, joint_axis=joint_axis, dir=dir, prev_dir=prev_dir)
        self.links.append(link)

        parent_link.child1 = link
        parent_link.child2 = link_addl
        
        return seg_size, dir, link

    def Create_Brain(self, fileName=None):

        if fileName is None:
            pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        else:
            pyrosim.Start_NeuralNetwork(fileName)

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