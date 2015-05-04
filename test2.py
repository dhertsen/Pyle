import matplotlib.lines as lines
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.axislines import Subplot

fig = plt.figure(1, (3, 3))
ax = Subplot(fig, 111)
fig.add_subplot(ax)
# line = lines.Line2D([0, 1], [0, 1], color='red')
# ax.lines.append(line)
ax.plot([0.0, 1.0], [0.0, 1.0], 'r-')
fig.savefig(open('test.pdf', 'w'))
