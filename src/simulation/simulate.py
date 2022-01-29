import numpy as np

from dataclasses import dataclass
from coilgun.coil import Coil
from coilgun.power_source import PowerSource
from .projectile import Projectile1D


@dataclass
class SimulationConf:
	"""A class that holds the configuration for a coilgun simulation"""

	dt: float 				# The time between updates
	max_time: float 		# The maximum time the simulation will run for


class CoilgunSimulation:
	"""A class that performances a simulation of a coilgun"""

	def __init__(self, coil: Coil, power_source: PowerSource, projectile: Projectile1D, conf: SimulationConf):
		self.coil = coil
		self.power_source = power_source
		self.projectile = projectile

		self.t = 0.0
		self.dt = conf.dt
		self.max_time = conf.max_time

		# Calculate the coil resistance (it will not change so dont calculate it more than once)
		self.R = self.coil.resistance()

	def run(self):
		"""Run the simulation"""

		simulation_data = []

		while self.t < self.max_time:
			I = self.power_source.current(resistance=self.R)

			# Calculate energy
			E = I**2 * self.R * self.dt

			# Save the information
			simulation_data.append((self.t, self.projectile.pos, self.projectile.vel, E))


			# This is wrong but well I must test it
			B = self.coil.B_field(z=self.projectile.pos, I=I)
			self.projectile.add_force(force=B)
			self.projectile.update(dt=self.dt)

			self.t += self.dt

		return simulation_data


