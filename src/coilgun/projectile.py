from enum import Enum
from abc import ABC, abstractmethod

from .coil import Coil
from .power_source import PowerSource


class ProjectileEnum(Enum):
	Projectile1D = "Projectile1D"
	MagneticProjectile = "MagneticProjectile"
	FerromageneticProjectile = "FerromageneticProjectile"


class Projectile1D(ABC):
	"""A class for a 1D projectile"""

	def __init__(self, mass: float, pos: float, vel: float):
		self.mass = mass
		self.pos = pos
		self.vel = vel
		self.acc = 0.0


	def add_force(self, force: float):
		"""Add a force to the projectile"""
		self.acc += force / self.mass

	def update(self, dt: float):
		"""Update the position and velocity of the projectile"""
		self.pos += self.vel * dt
		self.vel += self.acc * dt
		self.acc = 0

	@abstractmethod
	def calc_force_from_coil(self, coil: Coil, power_source: PowerSource, t: float):
		"""
		Calculate the forc acting on the projectile from a coil
		with a given power source
		"""



class MagneticProjectile(Projectile1D):
	"""Simulate a magnetic projectile"""

	def __init__(self, mass: float, pos: float, vel: float, m: float):
		super().__init__(mass, pos, vel)

		# m is the magnetic dipol moment of the magnet
		self.m = m

	def calc_force_from_coil(self, coil: Coil, power_source: PowerSource, t: float):
		I = power_source.current(coil=coil, t=t)
		dB = coil.B_field_gradiant(I=I, z=self.pos)
		return self.m * dB


class FerromageneticProjectile(Projectile1D):
	"""Simulate a ferromagenetic projectile"""

	def __init__(self, mass: float, pos: float, vel: float, mu):
		super().__init__(mass, pos, vel)

		raise NotImplementedError