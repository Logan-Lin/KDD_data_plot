import numpy as np
import matplotlib.pyplot as plt

x1 = np.arange(-5, 5, 0.01)

y1 = np.sin(x1)
y2 = np.cos(x1)
y3 = np.tanh(x1)

plt.plot(x1, y1, x1, y2, x1, y3)
plt.grid()
plt.xlabel("x")
plt.ylabel("y")
plt.title("HA HA HA")
plt.show()
