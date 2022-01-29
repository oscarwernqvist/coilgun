import matplotlib.pyplot as plt

from coilgun.coil import Coil
from simulation.draw import draw_coil


def show_coil():
	"""Command line interface for showing a coil"""

	# Create a coil
	coil = Coil(coils=[1, 2, 3, 4], inner_diameter=10, wire_diameter=1, resistivity=1e-6)

	# Create a figure
	fig, ax = plt.subplots()
	ax.set_aspect('equal')

	# Draw the coil
	draw_coil(coil, ax)
	plt.show()


if __name__ == '__main__':
	show_coil()