import numpy as np
import matplotlib.pyplot as plt


x1 = np.linspace(0.0, 5.0)
x2 = np.linspace(0.0, 2.0)
x3 = np.linspace(0, 10)

y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
y2 = np.cos(2 * np.pi * x2)
y3 = np.sin(x3)

plt.subplot(3, 1, 1)
plt.plot(x1, y1, 'o-')
plt.ylabel('Damped oscillation')
plt.title('A tale of 3 subplots')

plt.subplot(3, 1, 2)
plt.plot(x2, y2, '.-')
plt.ylabel('Undamped')

plt.subplot(3, 1, 3)
plt.plot(x3, y3, '.-')
plt.xlabel("FUCK")
plt.ylabel("SON OF BITCH")

plt.show()
