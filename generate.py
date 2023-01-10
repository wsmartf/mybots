import pyrosim.pyrosim as pyrosim

def CreateWorld():
    length, width, height = 1, 1, 1
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[2, 2, 0.5] , size=[length, width, height])
    pyrosim.End()

def CreateRobot():
    length, width, height = 1, 1, 1
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5] , size=[length, width, height])
        
    pyrosim.Send_Joint(name = "Torso_Backleg", parent= "Torso", child = "Backleg", type = "revolute", position = [-0.5, 0, 1])
    pyrosim.Send_Cube(name="Backleg", pos=[-0.5, 0, -0.5] , size=[length, width, height])

    pyrosim.Send_Joint(name = "Torso_Frontleg", parent= "Torso", child = "Frontleg", type = "revolute", position = [0.5, 0, 1])
    pyrosim.Send_Cube(name="Frontleg", pos=[0.5, 0, -0.5] , size=[length, width, height])

    pyrosim.End()

CreateWorld()
CreateRobot()