import numpy as np

from dataclasses import dataclass
from coilgun.coil import Coil
from coilgun.power_source import PowerSource
from coilgun.projectile import Projectile1D


@dataclass
class SimulationConf:
	"""A class that holds the configuration for a coilgun simulation"""

	dt: float 				# The time between updates
	max_time: float 		# The maximum time the simulation will run for


@dataclass
class SimulationData:
	"""A class that holds all the data from a simulation"""

	time: list[float]		# The time for every frame
	pos: list[float]		# The position of the projectile at every time
	vel: list[float]		# The velocity of the projectile at every time
	energy: list[float]		# The energy consumed by the coil at the time t during the time dt

	def frames(self):
		"""Return the number of frames in the simulation"""
		return len(self.time)

	def position_limits(self):
		"""Return the minimum and maximum position of the projectile"""
		return min(self.pos), max(self.pos)

	def energy_consumption(self) -> float:
		"""Return the total energy consumed"""
		return sum(self.energy)

	def energy_gain(self, projectile_mass: float) -> float:
		"""Return the energy gained by the projectile"""
		start_energy = projectile_mass*self.vel[0]**2/2
		end_energy = projectile_mass*self.vel[-1]**2/2
		return end_energy - start_energy

	def total_time(self):
		"""Return the total time the simulation was running"""
		return self.time[-1] - self.time[0]


class CoilgunSimulation:
	"""A class that performances a simulation of a coilgun"""

	def __init__(
		self, 
		coil: Coil, 
		power_source: PowerSource, 
		projectile: Projectile1D, 
		conf: SimulationConf
	):
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

		# Initial conditions
		time = [self.t]
		pos = [self.projectile.pos]
		vel = [self.projectile.vel]
		energy = [0]

		while self.t < self.max_time:
			# Calculate the force on the projectile
			# and update its motion
			F = self.projectile.calc_force_from_coil(
				coil=self.coil, 
				power_source=self.power_source,
				t=self.t
			)
			self.projectile.add_force(F)
			self.projectile.update(self.dt)

			# Calculate energy consumption
			E = self.power_source.energy_consumption(
				coil=self.coil,
				t=self.t,
				dt=self.dt
			)

			self.t += self.dt

			# Save the information
			time.append(self.t)
			pos.append(self.projectile.pos)
			vel.append(self.projectile.vel)
			energy.append(E)

		return SimulationData(time, pos, vel, energy)


