from enum import Enum


class ProjectileEnum(Enum):
	Projectile1D = "Projectile1D"


class Projectile1D:
	"""A class for a 1D projectile"""

	def __init__(self, mass: float, pos: float, vel: float=None):
		self.mass = mass
		self.pos = pos
		self.vel = vel or 0.0
		self.acc = 0.0


	def add_force(self, force: float):
		"""Add a force to the projectile"""
		self.acc += force / self.mass

	def update(self, dt: float):
		"""Update the position and velocity of the projectile"""
		self.pos += self.vel * dt
		self.vel += self.acc * dt
		self.acc = 0