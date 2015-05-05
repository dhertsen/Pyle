import profile
import random
reload(profile)


def random_energies(length):
    return [random.random() for i in range(length)]


c = profile.Canvas(width=5, space=1)
c.set_size(6, 2)
prof = profile.Profile(random_energies(10), c)
prof.set_bar_style(linewidth=2)
prof.set_leap_style(linestyle=':')
prof.set_line_style(color='red')

c.save('test.pdf')
