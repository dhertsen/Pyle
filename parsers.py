try:
    from gaupy.log import energy
except ImportError:
    print('GauPy module not available')


def gaussian(filename, type='gibbs'):
    return energy(filename, type=type)
