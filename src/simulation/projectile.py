import numpy as np
from dataclasses import dataclass


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


@dataclass
class ProjectileConf:
	"""A class that hold the configuration for a projectile"""

	mass: float 		# The mass of the projectile
	start_pos: float 	# The start postion for the projectile
	start_vel: float 	# The start velocity for the projectile


	def create_projectile(self) -> Projectile1D:
		"""Create a projectile from the configuration"""
		return Projectile1D(mass=self.mass, pos=self.start_pos, vel=self.start_vel)