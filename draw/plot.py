import matplotlib.pyplot as plt
import numpy as np

data = np.genfromtxt('/Users/yangxinming/a.csv', delimiter=',')

fig = plt.figure()  # an empty figure with no axes


fig, ax_lst = plt.subplots(2, 2)  # a figure with a 2x2 grid of Axes
fig.suptitle('No axes on this figure')  # Add a title so we know which it is

x = np.arange(0, 10, 0.2)
y = np.sin(x)
#fig, ax = plt.subplots()
ax_lst[0, 0].plot(x, y)
ax_lst[1, 1].plot(x, y)
plt.show()


plt.savefig('a.png')