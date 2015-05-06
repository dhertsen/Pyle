import pyle.energetics as energetics
import pyle.profile as profile
from molmod.units import kjmol

# Energies are obtained from a CSV file
e = energetics.csv('test2.csv')
# Clean the input. Extra arguments are parsed to
# the parser function. In this case, an electronic
# energy is parsed from a Gaussian output file
# instead of a Gibbs free energy (default).
e = energetics.parse(e, type='energy')
# Use the first bar of every profile as a reference
e = energetics.indexref(e, bar=0)
# Convert these electronic energies to kJ/mol
e = e / kjmol

# Open a canvas
canvas = profile.Canvas()
# and add the profiles
canvas.add_profiles(e)

# General bar and leap options
canvas.set_bar_style(linewidth=3.0)
canvas.set_leap_style(linestyle='--')

# Top energies are printed
canvas.set_topenergies()
canvas.profiles[0].set_bottomlabels(['a', 'TS', 'b'])
# Make labels the same colour as the bars
canvas.match_labels()
# Adjust size a little bit
canvas.set_energy_scale(-50, 220)
canvas.set_size(3, 1)

# Add some text right under the second bar
xtxt, ytxt = canvas.profiles[0].bars[1].get_middle()
canvas.ax.text(xtxt, -25, 'from Gaussian\noutput files',
               horizontalalignment='center', fontsize=8, color='#CCCCCC')

# Over and out
canvas.save('test2.pdf')
