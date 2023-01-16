import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import math
import random

STEPS = 10000

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = np.zeros(STEPS)
frontLegSensorValues = np.zeros(STEPS)

targetX = np.linspace(0, 2*np.pi, STEPS)

backLeg_amplitude = np.pi/4
backLeg_frequency = 20
backLeg_phaseOffset = np.pi/4

backLeg_targetAngles = backLeg_amplitude*np.sin(backLeg_frequency*targetX + backLeg_phaseOffset)

frontLeg_amplitude = np.pi/4
frontLeg_frequency = 20
frontLeg_phaseOffset = 0

frontLeg_targetAngles = frontLeg_amplitude*np.sin(frontLeg_frequency*targetX + frontLeg_phaseOffset)

# np.save("data/backLeg_targetAngles.npy", backLeg_targetAngles)
# np.save("data/frontLeg_targetAngles.npy", frontLeg_targetAngles)
# exit()

for i in range(STEPS):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b"Torso_BackLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = backLeg_targetAngles[i],
        maxForce = 80)

    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b"Torso_FrontLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = frontLeg_targetAngles[i],
        maxForce = 80)
    
    time.sleep(0.001)

p.disconnect()

np.save("data/backLegSensorValues.npy", backLegSensorValues)
np.save("data/frontLegSensorValues.npy", frontLegSensorValues)