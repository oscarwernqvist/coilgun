from dataclasses import dataclass
import numpy as np

from GA.DNA import DNA
from ode_models.coilgun import ode_solver_coilgun, ode_solver_RL
from utils.constants import mu_0


@dataclass
class CapacitanceBankData:
	"""Data for a capacitance bank"""
	C: float 	# [F] Capacitance of the bank
	V: float 	# [V] Initial voltage over the bank


@dataclass
class ProjectileData:
	"""Data for a projectile"""
	
	m: float 			# [kg] Mass of projectile
	x0: float 			# [m] Initial position of the projectile
	v0: float 			# [m/s] Initial velocity of the projectile
	mu_r: float 		# [-] Relative permability of the projectile
	x1: float = None 	# [m] Stop simulation when this position is reached. If None stop when time is up


@dataclass
class CoilData:
	"""Data for a coil"""
	
	l: float 	# [m] Length of the coil
	r: float 	# [m] Radius of the coil
	N: int 		# [-] Number of turns of wire in the coil
	rho: float 	# [Ohm x m] Resestivity of the wire
	A: float 	# [m^2]	Cross-sectional area of the wire

	def resistance(self):
		"""Return resistance of the coil"""
		# Length of wire
		L = self.N * 2 * np.pi * self.r
		# R = rho*L/A
		return self.rho * L / self.A

	def coil_inductance(self, core_mu):
		"""Return the inductance of a coil with a core with permeability 'core_mu'"""
		# Cross-sectional area of the coil
		A_coil = np.pi * self.r**2
		return core_mu * (self.N**2) * A_coil / self.l

	def params_for_inductance_model(self, projectile: ProjectileData):
		"""
		Return the constants A, B, C and D to the inductance model
		L(x) = Aexp(-B|x|^C)+D
		"""
		D = self.coil_inductance(mu_0)
		A = D*projectile.mu_r - D
		C = 2.06
		B = (self.l/2)**(-C)

		return A, B, C, D

	def inductance_model(self, projectile: ProjectileData):
		"""
		Return a function that will calculate the inductance 
		of the coil as a function of the projectile position
		"""
		A, B, C, D = self.params_for_inductance_model(projectile)
		def L(x):
			"""
			Calculate the inductance of a coil
			L(x) = Ae^(-B|x-C|^D) + E
			"""
			return A*np.exp(-B*np.power(np.abs(x), C)) + D

		return L

	def inductance_model_derivitive(self, projectile: ProjectileData):
		"""
		Return a function that will calculate the derivative 
		of the inductance with respect of the projectile position
		"""
		A, B, C, D = self.params_for_inductance_model(projectile)
		def dLdx(x):
			"""
			Calculate the derivative of the inductance of a coil
			L'(x) = -ABDe^(-B|x-C|^D)|x-C|^(D-1)/(x-C)
			"""
			return -A*B*C*np.exp(-B*np.power(np.abs(x), C))*np.power(np.abs(x), C-2)*x

		return dLdx

class CoilgunSimulationODE:
	"""
	Simulation of a coilgun using an ODE model
	"""
	
	def __init__(self, coil: CoilData, CB: CapacitanceBankData, projectile: ProjectileData):
		self.coil = coil
		self.CB = CB
		self.projectile = projectile

	@classmethod
	def from_DNA(cls, DNA: DNA):
		"""Create a coilgun simulation from DNA"""
		coil = CoilData(
			l=DNA["solenoid_length"],
			r=DNA["solenoid_radius"],
			N=DNA["solenoid_turns"],
			rho=DNA["solenoid_resistivity"],
			A=DNA["wire_cross_sectional_area"]
		)

		CB = CapacitanceBankData(
			C=DNA["capacitance"],
			V=DNA["capacitance_voltage"]
		)

		projectile = ProjectileData(
			m=DNA["projectile_mass"],
			x0=DNA["projectile_start_pos"],
			v0=DNA["projectile_velocity"],
			mu_r=DNA["projectile_mu_r"],
			x1=DNA["projectile_end_pos"]
		)

		return cls(coil=coil, CB=CB, projectile=projectile)

	def run(self, t_max: float, t_steps: int):
		"""Run the simulation during a time t_max for t_steps"""
		L = self.coil.inductance_model(self.projectile)
		dLdx = self.coil.inductance_model_derivitive(self.projectile)
		R = self.coil.resistance()

		# Drain the CB
		t1, x1, v1, I1, V1, _ = ode_solver_coilgun(
			C=self.CB.C,
			V0=self.CB.V,
			m=self.projectile.m,
			x0=self.projectile.x0,
			x1=self.projectile.x1,
			v0=self.projectile.v0,
			L=L,
			dLdx=dLdx,
			R=R,
			t_max=t_max,
			t_steps=t_steps
		)

		# After CB is drained the current do not go to zero imedietly
		t2, x2, v2, I2 = ode_solver_RL(
			m=self.projectile.m,
			x0=x1[-1],
			x1=None,
			v0=v1[-1],
			L=L,
			dLdx=dLdx,
			R=R,
			I0=I1[-1],
			t_max=t_max,
			t_steps=t_steps
		)
		# first element is the same as the last
		t = np.concatenate((t1, t2[1:] + t1[-1]))
		x = np.concatenate((x1, x2[1:]))
		v = np.concatenate((v1, v2[1:]))
		I = np.concatenate((I1, I2[1:]))
		V = np.concatenate((V1, [V1[-1]]*(len(t2)-1)))

		# Return time, pos, vel, current, voltage
		return t, x, v, I, V
