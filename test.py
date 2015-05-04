import profile
reload(profile)

c = profile.Canvas()

b = profile.Bar(0.0, 1.0, c, color='red')
b.plot()
d = profile.Bar(0.0, 2.0, c, color='red')
d.plot()
c.fig.savefig(open('test.pdf', 'w'))
