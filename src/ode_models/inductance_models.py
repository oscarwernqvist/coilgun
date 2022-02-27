import numpy as np


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