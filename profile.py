import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.text import Text
from matplotlib.transforms import offset_copy
from mpl_toolkits.axes_grid.axislines import Subplot
from matplotlib import rc


def _set_property(line, prop, value):
    try:
        set_prop = getattr(line, 'set_%s' % prop)
        set_prop(value)
    except AttributeError:
        print('Error: property %s not defined' % prop)


class Canvas(object):

    def __init__(self, width=3, space=2, tex=True):

        # Initializing the plots
        self.fig = plt.figure(1, (3, 3))
        self.ax = Subplot(self.fig, 111)
        self.fig.add_subplot(self.ax)
        self.fig.set_size_inches(5, 3)

        # All axes off by default
        for side in ['left', 'right', 'top', 'bottom']:
            self.ax.axis[side].set_visible(False)

        self.width = width
        self.space = space

        # Use tex for text font and rendering
        if tex:
            rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
            rc('text', usetex=True)

    def barpos(self, i):
        start = self.space + i * (self.width + self.space)
        return (start, start + self.width)

    def offset(self, x, y):
        return offset_copy(self.ax.transData, x=x, y=y, units='dots')

    def set_size(self, w, h):
        self.fig.set_size_inches(w, h)

    def set_energy_scale(self, emin, emax):
        self.ax.set_ylim(emin, emax)

    def save(self, filename, transparent=True, format='pdf'):
        # TODO otherwise no output at all, better solution?
        self.ax.plot()
        self.fig.savefig(filename, bbox_inches='tight',
                         transparent=True, format='pdf')
        print('%s written' % filename)

    def toggle_yaxis(self, position='left', label='energy',
                     labelsize=10, ticklabelsize=10):
        if position == 'both':
            positions = ['left', 'right']
        elif position in ['left', 'right']:
            positions = [position]
        else:
            positions = []

        for p in positions:
            self.ax.axis[p].set_label(label)
            self.ax.axis[p].label.set_size(labelsize)
            self.ax.axis[p].major_ticklabels.set_size(ticklabelsize)
            self.ax.axis[p].toggle(ticklabels=True, label=True)
            self.ax.axis[p].set_visible(True)


class Profile(object):

    def __init__(self, energies, positions, canvas):
        self._energies = energies
        self._positions = positions
        self._canvas = canvas

        self._bars = []
        for e, p in zip(self._energies, self._positions):
            self._bars.append(Bar(e, p, self._canvas))

        self._leaps = []
        for i, bar in enumerate(self._bars):
            try:
                self._leaps.append(Leap(bar, self._bars[i+1], self._canvas))
            except IndexError:
                pass

        self._len = len(self._energies)
        self._min = min(self._energies)
        self._max = max(self._energies)
        self._toplabels = []
        self._bottomlabels = []

    def __len__(self):
        return self._len

    def __iter__(self):
        '''
        min(profile) will return Bar with minimal energy,
        et vice versa for max(profile)
        '''
        return iter(self._bars)

    def set_bar_style(self, **kwargs):
        for bar in self._bars:
            for prop, val in kwargs.items():
                _set_property(bar, prop, val)

    def set_leap_style(self, **kwargs):
        for leap in self._leaps:
            for prop, val in kwargs.items():
                _set_property(leap, prop, val)

    def set_line_style(self, **kwargs):
        self.set_bar_style(**kwargs)
        self.set_leap_style(**kwargs)

    def set_toplabels(self, labels, offset=5, *pargs, **kwargs):
        for label, bar in zip(labels, self._bars):
            self._toplabels.append(Label(label=label, bar=bar,
                                         canvas=self._canvas,
                                         offset=(0, offset), *pargs, **kwargs))

    def set_bottomlabels(self, labels, offset=5, *pargs, **kwargs):
        for label, bar in zip(labels, self._bars):
            self._bottomlabels.append(Label(label=label, bar=bar,
                                            canvas=self._canvas,
                                            verticalalignment='top',
                                            offset=(0, -offset), *pargs,
                                            **kwargs))

    def set_toplabel_style(self, **kwargs):
        for label in self._toplabels:
            for prop, val in kwargs.items():
                _set_property(label, prop, val)

    def set_bottomlabel_style(self, **kwargs):
        for label in self._bottomlabels:
            for prop, val in kwargs.items():
                _set_property(label, prop, val)

    def set_label_style(self, **kwargs):
        self.set_toplabel_style(**kwargs)
        self.set_bottomlabel_style(**kwargs)

    def get_bars(self):
        return self._bars

    def get_leaps(self):
        return self._leaps

    def get_lines(self):
        return self._bars + self._leaps

    def get_toplabels(self):
        return self._toplabels

    def get_bottomlabels(self):
        return self._bottomlabels

    def get_labels(self):
        return self._toplabels + self._bottomlabels

    def get_min_energy(self):
        return self._min

    def get_max_energy(self):
        return self._max

    def get_length(self):
        return self._len


class Bar(Line2D):

    def __init__(self, energy, position, canvas, *args, **kwargs):
        # zorder = 2 (leaps, drawn first), 3 (bars) or 4 (labels,
        # drawn last)
        super(Bar, self).__init__([], [], zorder=3, *args, **kwargs)
        self._energy = energy
        self._position = position
        self._canvas = canvas
        self._set_xy()
        self._canvas.ax.add_line(self)

    def __lt__(self, other):
        return self._energy < other._energy

    def _set_xy(self):
        x = self._canvas.barpos(self._position)
        y = [self._energy] * 2
        self.set_data(x, y)

    def get_position(self):
        return self._position

    def get_energy(self):
        return self._energy

    def get_middle(self):
        x, y = self.get_data()
        return (sum(x) / 2.0, y[0])

    def set_position(self, pos):
        self._position = pos
        self._set_xy()

    def set_energy(self, ener):
        self._energy = ener
        self._set_xy()


class Leap(Line2D):

    def __init__(self, bar1, bar2, canvas, *args, **kwargs):
        super(Leap, self).__init__([], [], zorder=2, *args, **kwargs)
        self._canvas = canvas
        self.set_bars(bar1, bar2)
        self._canvas.ax.add_line(self)

    def _set_xy(self):
        x = [self._canvas.barpos(self._bar1.get_position())[1],
             self._canvas.barpos(self._bar2.get_position())[0]]
        y = [self._bar1.get_energy(), self._bar2.get_energy()]
        self.set_data(x, y)

    def set_bars(self, bar1, bar2):
        self._bar1 = bar1
        self._bar2 = bar2
        self._set_xy()


class Label(Text):

    def __init__(self, label, bar, canvas, energy_format='%.1f',
                 horizontalalignment='center', fontsize=10,
                 offset=(0, 0), *args, **kwargs):
        self._bar = bar
        self._canvas = canvas
        if label == 'energy':
            self._label = energy_format % self._bar.get_energy()
        else:
            self._label = label or ''
        self._x, self._y = self._bar.get_middle()
        super(Label, self).__init__(x=self._x, y=self._y, text=self._label,
                                    horizontalalignment=horizontalalignment,
                                    transform=self._canvas.offset(*offset),
                                    fontsize=fontsize, zorder=4,
                                    *args, **kwargs)
        self._canvas.ax.add_artist(self)
