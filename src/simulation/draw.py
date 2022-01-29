import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from coilgun.coil import Coil


def draw_coil(coil: Coil, ax: Axes) -> None:
	"""A function that will draw the Coil on a axes object"""
	
	# Iterate over and draw all the wires
	for i, circles in enumerate(coil.coils):
		z = i * coil.wire_diameter
		for j in range(circles):
			circle_radius = (j + 1/2) * coil.wire_diameter + coil.inner_diameter / 2

			# Draw the current wire
			draw_wire(circle_radius, coils.wire_diameter / 2, z, ax)


def draw_wire(radius: float, wire_radius: float, z: float, ax: Axes) -> None:
	"""Draw a singel loop of wire on an axes object"""
	wire_in = plt.Circle((z, radius), wire_radius, color='black', fill=False)
	marker_in = plt.scatter(z, radius, s=300, color='black', marker='x')
	wire_out = plt.Circle((z, -radius), wire_radius, color='black', fill=False)

	ax.add_patch(wire_in)
	ax.add_artist(marker_in)
	ax.add_patch(wire_out)