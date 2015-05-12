try:
    from gaupy.utils import energy
except ImportError:
    print('GauPy module not available')


def gaussian(filename, type='gibbs'):
    return energy(filename, type=type)
