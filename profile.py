import matplotlib.lines as lines
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.axislines import Subplot


class Canvas(object):

    def __init__(self, width=3, space=1):

        # Initializing the plots
        self.fig = plt.figure(1, (3, 3))
        self.ax = Subplot(self.fig, 111)
        self.fig.add_subplot(self.ax)
        self.width = width
        self.space = space

    def barpos(self, i):
        start = i * (self.width + self.space)
        return (start, start + self.width)


class Profile(object):

    def __init__(self, energies, positions, canvas):
        self.energies = energies
        self.positions = positions
        self.canvas = canvas


class Bar(lines.Line2D):

    def __init__(self, energy, position, canvas, **kwargs):
        self.energy = energy
        self.position = position
        self.canvas = canvas
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def plot(self):
        x = self.canvas.barpos(self.position)
        y = [self.energy] * 2
        print x
        print y
        line = lines.Line2D(x, y, self.__dict__)
        self.canvas.ax.lines.append(line)
        # self.canvas.ax.plot(line)


class Leap(lines.Line2D):
    pass
