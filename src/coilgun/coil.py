import numpy as np

from abc import ABC, abstractmethod

from utils.constants import mu_0
from utils.math import sign
from enum import Enum


class CoilEnum(Enum):
	GeometryCoil = "GeometryCoil"
	Solenoid = "Solenoid"


class Coil(ABC):
	"""Base class for a coil"""

	@abstractmethod
	def length(self) -> float:
		"""Return the lenght of the coil"""

	@abstractmethod
	def resistance(self) -> float:
		"""Calculate the resistance in the coil"""

	@abstractmethod
	def B_field(self, I: float, z: float) -> float:
		"""
		Calculate the B field at a coordinate z on the center axis of the coil when a current I 
		flows through the coil. z=0 is the first part of the coil
		"""

	@abstractmethod
	def B_field_gradiant(self, I: float, z: float) -> float:
		"""
		Calculate the B field gradient
		"""


class Solenoid(Coil):
	"""A Solenoid class"""

	def __init__(
		self, 
		L: float, 				# Length of coil [m]
		N: int, 				# Turns of wire in the coil
		inner_diameter: float, 	# Radius of the coil [m]
		wire_diameter: float,	# Diameter of the wire [m]
		resistivity: float 		# Resistivity of the wire [Ohm x m] 
	):
		self.L = L
		self.N = N
		self.inner_diameter = inner_diameter
		self.wire_diameter = wire_diameter
		self.resistivity = resistivity

	def length(self) -> float:
		return self.L

	def resistance(self) -> float:
		# Totoal lenght of the wire
		wire_length = 2 * np.pi * self.inner_diameter * self.N
		# Cross-sectional area of wire
		A = np.pi * self.wire_diameter**2 / 4

		return self.resistivity * wire_length / A

	def B_field(self, I: float, z: float) -> float:
		"""
		Calculate the B field from a solenoid.
		I is the current in the wire and 
		z=0 is placed at the start of the solenoid,
		e.g. to the left.
		"""
		# The formula for the B field of a solenoid
		# use coordinats centered in the coil
		z0 = z - self.L / 2
		R = self.inner_diameter / 2

		cos_a1 = (self.L / 2 - z0) / np.sqrt(R**2 + (self.L / 2 - z0)**2)
		cos_a2 = (self.L / 2 + z0) / np.sqrt(R**2 + (self.L / 2 + z0)**2)

		return mu_0 * self.N * I * (cos_a1 + cos_a2) / (2 * self.L)

	def B_field_gradiant(self, I: float, z: float) -> float:
		# The formula for the B field of a solenoid
		# use coordinats centered in the coil
		z0 = z - self.L / 2
		R = self.inner_diameter / 2

		d_cos_a1 = -R**2 / (R**2+(self.L / 2 - z0)**2)**(3/2)
		d_cos_a2 = R**2 / (R**2+(self.L / 2 + z0)**2)**(3/2)

		return mu_0 * self.N * I * (d_cos_a1 + d_cos_a2) / (2 * self.L)




class GeometryCoil(Coil):
	"""
	This coil is based of multiple circles of wire.
	It can have a different number of circles at different
	places so it can have a costumized geometry.
	"""

	def __init__(
		self, 
		coils: list[int], 		# Number of coils for every 'circle'
		inner_diameter: float, 	# Inner diameter of the coil. [mm]
		wire_diameter: float, 	# Diameter of the wire used in the coil. [mm]
		resistivity: float 		# Resistivity of the material used in the wire [Ohm x mm]
	):
		self.coils = coils
		self.inner_diameter = inner_diameter
		self.wire_diameter = wire_diameter
		self.resistivity = resistivity

	def length(self) -> float:
		return self.wire_diameter * len(self.coils)

	def resistance(self) -> float:
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

	def B_field(self, I: float, z: float) -> float:
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

		return B

	def B_field_gradiant(self, I: float, z: float) -> float:
		raise NotImplementedError
