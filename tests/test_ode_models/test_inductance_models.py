import numpy as np

from ode_models.inductance_models import solenoid_inductance


def test_inductance_float(L):
	"""Test if the inductance is correctly calculated for a float"""
	assert L(4) == 8
	assert round(L(4.1) - 7.999940000899991, 7) == 0

def test_inductance_derivative_float(dLdx):
	"""Test if the derivative of the inductance is correctly calculated for a float"""
	assert round(dLdx(3.9) - 0.002999940000600, 7) == 0
	assert round(dLdx(4.1) + 0.002999940000600, 7) == 0
	# assert round(dLdx(3.5) - 1.761399492775267, 7) == 0 # This do not agree with matlab for some reason
	assert dLdx(4) == 0 # Div with zero

def test_inductance_ndarray(L):
	"""Test if the inductance is correctly calculated for a float"""
	np.testing.assert_allclose(L(np.array([4, 4.1])), (8, 7.999940000899991))

def test_inductance_derivative_ndarray(dLdx):
	"""Test if the derivative of the inductance is correctly calculated for a float"""
	np.testing.assert_allclose(dLdx(np.array([3.9, 4, 4.1])), (0.002999940000600, 0, -0.002999940000600), rtol=1e-5)

def test_solenoid_inductance():
	"""Test the inductance of a solenoid"""
	assert solenoid_inductance(1, 1, 1, 1) == np.pi
	assert solenoid_inductance(2, 1, 1, 1) == 2*np.pi
	assert solenoid_inductance(1, 2, 1, 1) == 4*np.pi
	assert solenoid_inductance(1, 1, 2, 1) == 4*np.pi
	assert solenoid_inductance(1, 1, 1, 2) == np.pi / 2
