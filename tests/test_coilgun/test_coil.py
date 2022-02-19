from coilgun.coil import Coil


def test_coil_resistance(geometry_coil):
	"""Test the calculation of the resistance in the coil"""
	assert geometry_coil.resistance() == 224e-6

def test_B_field_from_coil(geometry_coil):
	"""Test the calculation of the B field from the coil"""
	# My calculator do not have the required precistion
	assert round(geometry_coil.B_field(z=0, I=1) - 954.7230157e-6, 6) == 0