import math

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from coilgun.coil import Coil, Solenoid, GeometryCoil


def draw_coil(coil: Coil, ax: Axes) -> None:
	"""A function that will draw the Coil on a axes object"""

	if isinstance(coil, Solenoid):
		coils = [1 for _ in range(math.floor(coil.L / coil.wire_diameter))]
	else:
		coils = coil.coils
	
	# Iterate over and draw all the wires
	for i, circles in enumerate(coils):
		z = i * coil.wire_diameter
		for j in range(circles):
			circle_radius = (j + 1/2) * coil.wire_diameter + coil.inner_diameter / 2

			# Draw the current wire
			draw_wire(circle_radius, coil.wire_diameter / 2, z, ax)


def draw_wire(radius: float, wire_radius: float, z: float, ax: Axes) -> None:
	"""Draw a singel loop of wire on an axes object"""
	wire_in = plt.Circle((z, radius), wire_radius, color='black', fill=False)
	wire_out = plt.Circle((z, -radius), wire_radius, color='black', fill=False)

	ax.add_patch(wire_in)
	ax.add_patch(wire_out)

	# Add a cross in the wire that is going into the figure
	ax.plot(
		[z - np.sqrt(1/2) * wire_radius, z + np.sqrt(1/2) * wire_radius], 
		[radius + np.sqrt(1/2) * wire_radius, radius - np.sqrt(1/2) * wire_radius], 
		color='black'
	)
	ax.plot(
		[z + np.sqrt(1/2) * wire_radius, z - np.sqrt(1/2) * wire_radius], 
		[radius + np.sqrt(1/2) * wire_radius, radius - np.sqrt(1/2) * wire_radius], 
		color='black'
	)