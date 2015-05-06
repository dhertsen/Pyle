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


def parse(energies, parser=parsers.gaussian, *pargs, **kwargs):
    '''
    also to remove all nonsense
    '''
    return energies.applymap(
        lambda e: _energy(e, parser=parser, *pargs, **kwargs))


def indexref(energies, bar, profile=None):
    if profile:
        ref = energies[bar][profile]
        return energies - ref
    else:
        return energies.subtract(energies[bar], axis=0)


def minref(energies, overall=False):
    if overall:
        # TODO Really? No shortcut?
        return energies - energies.min().min(axis=1)
    else:
        return energies.subtract(energies.min(axis=1), axis=0)


def csv(filename):
    return DataFrame.from_csv(filename, header=None, index_col=None)
