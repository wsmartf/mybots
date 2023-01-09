import pyrosim.pyrosim as pyrosim

length = 1
width = 1
height = 1

x1, y1, z1 = 0, 0, 0.5
x2, y2, z2 = 1, 0, 1

pyrosim.Start_SDF("boxes.sdf")
pyrosim.Send_Cube(name="Box", pos=[x1,y1,z1] , size=[length, width, height])
pyrosim.Send_Cube(name="Box2", pos=[x2,y2,z2] , size=[length, width, height])
pyrosim.End()