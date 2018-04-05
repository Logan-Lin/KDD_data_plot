import pymysql
import matplotlib.pyplot as plt
import numpy as np

database = pymysql.connect("localhost", "root", "094213", "KDD")
cursor = database.cursor()

t = np.arange(-np.pi, np.pi, 0.01)
s = 1 + np.sin(t)

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel="time (s)", ylabel='voltage (mV)', title="That's really simple!")
ax.grid()

fig.savefig("matplotlib_samples/Simple_plot.png")
plt.show()
