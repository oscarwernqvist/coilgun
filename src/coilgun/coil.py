import numpy as np

from dataclasses import dataclass
from utils.constants import mu_0
from utils.math import sign


@dataclass
class Coil():
	"""Class representing a single coil in a coilgun"""

	coils: list[int]  	 		# Number of coils for every 'circle'
	inner_diameter: float 		# Inner diameter of the coil. [mm]
	wire_diameter: float 		# Diameter of the wire used in the coil. [mm]
	resistivity: float 			# Resistivity of the material used in the wire [Ohm x mm]

	def resistance(self):
		"""Calculate the resistance in the coil"""

		# Length of wire (can be calulated using the formula for the arithmetic seris)
		a1 = self.inner_diameter + self.wire_diameter
		d = 2 * self.wire_diameter
		n = np.array(self.coils)

		L = np.sum(n * (2 * a1 + (n-1) * d) ) * np.pi / 2.0

		# Cross-sectional area of wire
		A = np.pi * self.wire_diameter**2 / 4

		# Resistance of wire
		return self.resistivity * L / A

	def B_field(self, I: float, z: float):
		"""
		Calculate the B field at a coordinate z on the center axis of the coil when a current I 
		flows through the coil. z=0 is the first 'circle'
		"""

		# The B field can be calculated using the formula for a current loop
		B = 0
		# Iterate over one 'circle' at a time
		for i, n in enumerate(self.coils):
			# Dist to current circle
			dz = i * self.wire_diameter - z
			# Radius for all coils in the current circle
			a = np.array([self.inner_diameter + self.wire_diameter * (2*i + 1) for i in range(n)]) / 2
			# Convert to meter
			a = a * 1e-3
			dz = dz * 1e-3

			dB = mu_0 * I * np.sum(a**2 / np.power(dz**2 + a**2, 3/2)) / 2

			B += sign(dz) * dB 	# Not sure about this sign(dz). It is not how the B field works

			print(B * 2 / mu_0 / I)

		return B



		
