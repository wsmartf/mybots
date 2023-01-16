import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load("data/backLegSensorValues.npy")
frontLegSensorValues = np.load("data/frontLegSensorValues.npy")
backLeg_targetAngles = np.load("data/backLeg_targetAngles.npy")
frontLeg_targetAngles = np.load("data/frontLeg_targetAngles.npy")

# plt.plot(backLegSensorValues, label='BackLeg', linewidth=5)
# plt.plot(frontLegSensorValues, label='FrontLeg')
# plt.legend()
# plt.show()

plt.plot(backLeg_targetAngles, label='BackLeg', linewidth=5)
plt.plot(frontLeg_targetAngles, label='FrontLeg')
plt.show()