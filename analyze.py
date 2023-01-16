import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load("data/backLegSensorValues.npy")
frontLegSensorValues = np.load("data/frontLegSensorValues.npy")

plt.plot(backLegSensorValues, label='BackLeg', linewidth=5)
plt.plot(frontLegSensorValues, label='FrontLeg')
plt.legend()
plt.show()