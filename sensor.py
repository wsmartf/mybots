import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim
import math

class SENSOR:

    def __init__(self, linkName):
        self.linkName = linkName
        self.values = np.zeros(c.STEPS)
    
    def Get_Value(self, i):
        self.values[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        # self.values[i] = math.sin(2*i)*val
        return self.values[i]

    # def Print_Value(self, i):
    #     print(self.values[i])

    def Save_Values(self):
        filename = "data/" + self.linkName + "SensorValues.npy"
        np.save(filename, self.values)