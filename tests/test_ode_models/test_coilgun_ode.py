from ode_models.coilgun import calculate_efficiency


def test_efficiency():
	"""Test the calculation of the efficiency"""
	assert calculate_efficiency(0, 1, 0, 1, 1, 1) == 1
	assert calculate_efficiency(1, 1, 0, 1, 1, 1) == 0
	assert calculate_efficiency(0, 1, 0, 2, 1, 1) == 0.25
	assert calculate_efficiency(0, 1, 0, 1, 1, 2) == 0.5