import pyrosim.pyrosim as pyrosim

length = 1
width = 1
height = 1

x, y, z = 0, 0, 0.5

pyrosim.Start_SDF("boxes.sdf")

for x in range(5):
    x1 = x
    for y in range(5):
        y1 = y
        for i in range(10):
            z1 = z+i
            new_l = pow(length*0.9, i)
            new_w = pow(width*0.9, i)
            new_h = pow(height*0.9, i)
            new_name = "Box",x,y,i
            pyrosim.Send_Cube(name="Box", pos=[x1,y1,z1] , size=[new_l, new_w, new_h])

pyrosim.End()