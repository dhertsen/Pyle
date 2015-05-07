try:
    from gaupy.log import LOGFile
except ImportError:
    print('GauPy module not available')


def gaussian(filename, type='gibbs'):
    return getattr(LOGFile(filename), type)
