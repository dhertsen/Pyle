import pyle.energetics as energetics
import pyle.profile as profile

# Energies are obtained from a CSV file
e = energetics.csv('test1.csv')
# Clean the input
e = energetics.parse(e)
# Use the first bar of every profile as a reference
e = energetics.indexref(e, bar=0)

# Open a canvas
canvas = profile.Canvas()
# and add the profiles
canvas.add_profiles(e)

# General bar and leap options
canvas.set_bar_style(linewidth=3.0)
canvas.set_leap_style(linestyle=':')

# Colors of the profiles
canvas.profiles[0].set_line_style(color='red')
canvas.profiles[1].set_line_style(color='blue')
canvas.profiles[2].set_line_style(color='green')
canvas.profiles[2].bars[0].set_color('grey')

# For most bars, top energies are printed
canvas.set_topenergies()
# Delete some of these
canvas.profiles[0].del_toplabels(2, 3)
canvas.profiles[1].del_toplabels(1)
# Add some bottom energies
canvas.profiles[0].set_bottomlabels(['', '', 'energy', 'energy', ''])
# Make labels the same colour as the bars
canvas.match_labels()

# Pythonic irony
canvas.ax.text(2, -35, 'Most. Useful. Ever.', fontsize=20)

# Over and out
canvas.save('test1.pdf')
