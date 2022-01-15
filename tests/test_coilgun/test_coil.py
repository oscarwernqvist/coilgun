from coilgun.coil import Coil


def test_coil_resistance(constant_current_coil):
	"""Test the calculation of the resistance in the coil"""
	assert constant_current_coil.resistance() == 224e-6

def test_B_field_from_coil(constant_current_coil):
	"""Test the calculation of the B field from the coil"""
	# My calculator do not have the required precistion
	assert round(constant_current_coil.B_field(z=0) - 954.7230157e-6, 6) == 0