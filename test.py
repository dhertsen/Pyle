import profile
reload(profile)

c = profile.Canvas()

'''
bar1 = profile.Bar(1.0, 1.0, c, color='red')
bar2 = profile.Bar(10.0, 3.0, c, color='red')
bar3 = profile.Bar(15, 3, c, color='blue')
leap1 = profile.Leap(bar1, bar2, c)
leap2 = profile.Leap(bar1, bar3, c)
profile._set_property(bar1, 'color', 'red')
'''


prof = profile.Profile(range(10), range(10), c)

prof.set_bar_style(linewidth=2)
prof.set_leap_style(linestyle=':')
prof.set_line_style(color='red')

prof.get_bars()[5].set_color('yellow')
'''
profile.Label(label='energy', bar=prof.get_bars()[4], offset=(0, 10), canvas=c)
profile.Label(label='energy', bar=prof.get_bars()[7], offset=(0, 5), canvas=c)
profile.Label(label='energy', bar=prof.get_bars()[7], offset=(0, -25),
              canvas=c)
'''

prof.set_toplabels(['energy'] * 10)
prof.set_bottomlabels(['energy'] * 10)
print min(prof)

# c.toggle_yaxis()
c.set_energy_scale(-1, 10)
c.save('test.pdf')
