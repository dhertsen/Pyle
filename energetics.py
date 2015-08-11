import parsers
from pandas import DataFrame


def _energy(value, parser=parsers.gaussian, *pargs, **kwargs):
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

    def __str__(self, index=False):
        return self.to_string(header=False, index=index, na_rep=' ')

    @classmethod
    def from_csv(self, filename):
        return Energies(super(Energies, self).from_csv(
            filename, header=None, index_col=None))

    def to_csv(self, filename):
        super(Energies, self).to_csv(filename, header=None, index=False)
        print('%s written' % filename)

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
            return self - self.min().min(axis=1)
        else:
            return self.subtract(self.min(axis=1), axis=0)
