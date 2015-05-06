from gaupy.log import LOGFile
from gaupy.filenames import GaussianFile


def gaussian(filename, type='gibbs'):
    return getattr(LOGFile(filename), type)


def gaussian_spe(filename):
    f = GaussianFile(filename)
    fspe = f.add('spe')
    fl = LOGFile(f)
    fspel = LOGFile(fspe)
    return fl['energy'] + fspel['gibbscorrection']
