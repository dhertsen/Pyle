import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.text import Text
from matplotlib.transforms import offset_copy
from matplotlib import rc
from mpl_toolkits.axes_grid.axislines import Subplot
import numpy as np


def _set_property(obj, prop, value):
    '''
    Set property of :class:`Leap`, :class:`Bar` of :class:`Label`
    by calling obj.set_prop(value).
    '''
    try:
        set_prop = getattr(obj, 'set_%s' % prop)
        set_prop(value)
    except AttributeError:
        print('Error: property %s not defined' % prop)


def _del(lst, *pargs):
    '''
    In a list of :class:`Leap`, :class:`Bar` of :class:`Label`, remove elements
    with indices ``*pargs`` from the plot. Does not remove them from the list,
    so no index issues!
    '''

    for i in pargs:
        lst[i].remove()


class Canvas(object):

    def __init__(self, barwidth=3, barspace=2, tex=True):
        '''
        Canvas used for all drawings.

        Arguments:
            barwidth
                width of the bars
            barspace
                space between the bars, i.e. the horizontal length
                of the leaps
            tex
                use tex to render all labels
        '''

        # Initializing the plots
        self.fig = plt.figure(1, (3, 3))
        '''``matplotlib.figure.Figure`` used for plotting'''
        self.ax = Subplot(self.fig, 111)
        '''``matplotlib.axis.Axis`` used for plotting'''
        self.fig.add_subplot(self.ax)
        self.fig.set_size_inches(5, 3)

        # Add profiles seperately after initialization of Canvas
        self.profiles = []
        '''list of profiles, i.e. instances of ``Profile``'''

        # All axes off by default
        for side in ['left', 'right', 'top', 'bottom']:
            self.ax.axis[side].set_visible(False)

        self.barwidth = barwidth
        '''width of a bar'''
        self.barspace = barspace
        '''space between bars, i.e. horizontal length of leaps'''

        # Use tex for text font and rendering
        if tex:
            rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
            rc('text', usetex=True)

    def add_profiles(self, energies):
        '''
        Add profiles to canvas. Energies are in a :class:`pandas.DataFrame`
        with one profile per row and columns corresponding to bars. ``NaN``
        values indicate skipped bars.
        '''
        for i, e in energies.iterrows():
            self.profiles.append(Profile(energies=e, canvas=self))

    def barpos(self, i):
        '''
        Return the absolute ``(x_begin, x_end)`` position of the ith bar.

        Arguments:
            i
                number of the bar
        '''
        start = self.barspace + i * (self.barwidth + self.barspace)
        return (start, start + self.barwidth)

    def offset(self, x, y):
        '''
        Returns an offset transform which can be based to text and line
        constructors to shift the label ``(x, y)`` with respect to the
        correspoding bar.

        Arguments:
            x
                horizontal offset
            y
                vertical offset
        '''
        return offset_copy(self.ax.transData, x=x, y=y, units='dots')

    def set_bar_style(self, **kwargs):
        for p in self.profiles:
            p.set_bar_style(**kwargs)

    def set_leap_style(self, **kwargs):
        for p in self.profiles:
            p.set_leap_style(**kwargs)

    def set_line_style(self, **kwargs):
        for p in self.profiles:
            p.set_line_style(**kwargs)

    def set_label_style(self, **kwargs):
        for p in self.profiles:
            p.set_label_style(**kwargs)

    def set_topenergies(self, *pargs, **kwargs):
        for p in self.profiles:
            p.set_topenergies(*pargs, **kwargs)

    def set_bottomenergies(self, *pargs, **kwargs):
        for p in self.profiles:
            p.set_bottomenergies(*pargs, **kwargs)

    def set_size(self, w, h):
        self.fig.set_size_inches(w, h)

    def set_energy_scale(self, emin, emax):
        self.ax.set_ylim(emin, emax)

    def match_toplabels(self):
        for p in self.profiles:
            p.match_toplabels()

    def match_bottomlabels(self):
        for p in self.profiles:
            p.match_bottomlabels()

    def match_labels(self):
        self.match_toplabels()
        self.match_bottomlabels()

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
    # explain why profile and canvas can be accessed as attributes
    # and others have set/get functions

    def __init__(self, energies, canvas):
        self._energies = []
        self._positions = []
        for i, e in enumerate(energies):
            if not np.isnan(e):
                self._energies.append(e)
                self._positions.append(i)
        self._canvas = canvas

        self.bars = []
        for e, p in zip(self._energies, self._positions):
            self.bars.append(Bar(e, p, self._canvas))

        self.leaps = []
        for i, bar in enumerate(self.bars):
            try:
                self.leaps.append(Leap(bar, self.bars[i+1], self._canvas))
            except IndexError:
                pass

        self._len = len(self._energies)
        self._min = min(self._energies)
        self._max = max(self._energies)
        self.toplabels = []
        self.bottomlabels = []

    def __len__(self):
        return self._len

    def __iter__(self):
        '''
        min(profile) will return Bar with minimal energy,
        et vice versa for max(profile)
        '''
        return iter(self.bars)

    def set_bar_style(self, **kwargs):
        for bar in self.bars:
            for prop, val in kwargs.items():
                _set_property(bar, prop, val)

    def set_leap_style(self, **kwargs):
        for leap in self.leaps:
            for prop, val in kwargs.items():
                _set_property(leap, prop, val)

    def set_line_style(self, **kwargs):
        self.set_bar_style(**kwargs)
        self.set_leap_style(**kwargs)

    def set_toplabels(self, labels, offset=3, *pargs, **kwargs):
        for label, bar in zip(labels, self.bars):
            self.toplabels.append(Label(label=label, bar=bar,
                                        canvas=self._canvas,
                                        offset=(0, offset), *pargs, **kwargs))

    def set_bottomlabels(self, labels, offset=3, *pargs, **kwargs):
        for label, bar in zip(labels, self.bars):
            self.bottomlabels.append(Label(label=label, bar=bar,
                                           canvas=self._canvas,
                                           verticalalignment='top',
                                           offset=(0, -offset), *pargs,
                                           **kwargs))

    def set_topenergies(self, *pargs, **kwargs):
        self.set_toplabels(['energy'] * self._len, *pargs, **kwargs)

    def set_bottomenergies(self, *pargs, **kwargs):
        self.set_bottomlabels(['energy'] * self._len, *pargs, **kwargs)

    def set_toplabel_style(self, **kwargs):
        for label in self.toplabels:
            for prop, val in kwargs.items():
                _set_property(label, prop, val)

    def set_bottomlabel_style(self, **kwargs):
        for label in self.bottomlabels:
            for prop, val in kwargs.items():
                _set_property(label, prop, val)

    def set_label_style(self, **kwargs):
        self.set_toplabel_style(**kwargs)
        self.set_bottomlabel_style(**kwargs)

    def set_style(self, **kwargs):
        self.set_label_style(**kwargs)
        self.set_line_style(**kwargs)

    def match_toplabels(self):
        for i, l in enumerate(self.toplabels):
            l.set_color(self.bars[i].get_color())

    def match_bottomlabels(self):
        for i, l in enumerate(self.bottomlabels):
            l.set_color(self.bars[i].get_color())

    def match_labels(self):
        self.match_toplabels()
        self.match_bottomlabels()

    def del_bars(self, *pargs):
        _del(self.bars, *pargs)

    def del_leaps(self, *pargs):
        _del(self.leaps, *pargs)

    def del_toplabels(self, *pargs):
        _del(self.toplabels, *pargs)

    def del_bottomlabels(self, *pargs):
        _del(self.bottomlabels, *pargs)

    def del_labels(self, *pargs):
        _del(self.toplabels, *pargs)
        _del(self.bottomlabels, *pargs)

    def get_lines(self):
        return self.bars + self.leaps

    def get_labels(self):
        return self.toplabels + self.bottomlabels

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
