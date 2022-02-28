import numpy as np

from utils.constants import mu_0


def exponential_model_of_coil_indunctance(A: float, B: float, C: float, D: float, E: float):
	"""Create a function to calculate the inductance of a coil"""
	def L(x):
		"""
		Calculate the inductance of a coil
		L(x) = Ae^(-B|x-C|^D) + E
		"""
		return A*np.exp(-B*np.power(np.abs(x-C), D)) + E

	return L

def exponential_model_of_coil_indunctance_derivative(A: float, B: float, C: float, D: float):
	"""Create a function to calculate the derivative of the inductance of a coil"""
	def dLdx(x):
		"""
		Calculate the derivative of the inductance of a coil
		L'(x) = -ABDe^(-B|x-C|^D)|x-C|^D/(x-C)
		"""
		xc = x - C
		return -A*B*D*np.exp(-B*np.power(np.abs(xc), D))*np.power(np.abs(xc), D-2)*xc

	return dLdx

def solenoid_inductance(mu: float, N: int, r: float, l: float) -> float:
	"""Return the inductance of a coil with a core with permeability mu"""
	A = np.pi * r**2
	return mu*(N**2)*A / l

def solenoid_resistance(N: int, r: float):
	"""Return the resistance of a coil"""
	return N*2*np.pi*r

def parmas_for_exponential_model(mu_r: float, N: int, r: float, l: float) -> tuple:
	"""
	Calculate parmas A, B, C, D and E for the 
	exponential model of the inductance in a coil
	
	mu_r: Relative permeability of the projectile
	N: Number of turns of wire in the coil
	r: radius of the coil
	l: length of the coil
	"""
	# E is the inductance in the absence of a projectile in the core
	E = solenoid_inductance(mu_0, N, r, l)

	# A is the increase of inductance when the projectile is in the center of the coil
	A = E*mu_r - E

	# C is 0 if the coil is centered around 0
	C = 0

	# D was 2.06 for the other studie so I use it here for now
	D = 2.06

	# When the projectile is at outside of the core the exponential should be ~0
	B = (l/2)**(-D)

	return A, B, C, D, E
