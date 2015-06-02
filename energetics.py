import parsers
from pandas import DataFrame


def _energy(value, parser, *pargs, **kwargs):
    try:
        return float(value)
    except:
        try:
            return parser(value, *pargs, **kwargs)
        except:
            return float('nan')


class Energies(DataFrame):

    @property
    def _constructor(self):
        return Energies

    @classmethod
    def from_csv(self, filename):
        return Energies(super(Energies, self).from_csv(
            filename, header=None, index_col=None))

    def parse(self, parser=parsers.gaussian, *pargs, **kwargs):
        '''
        also to remove all nonsense
        '''
        return self.applymap(
            lambda e: _energy(e, parser=parser, *pargs, **kwargs))

    def indexref(self, bar, profile=None):
        if profile:
            return self - self[bar][profile]
        else:
            return self.subtract(self[bar], axis=0)

    def minref(self, overall=False):
        if overall:
            # TODO Really? No shortcut?
            return self - self.min().min(axis=1)
        else:
            return self.subtract(self.min(axis=1), axis=0)
