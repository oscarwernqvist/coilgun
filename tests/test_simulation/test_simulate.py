


def test_simulation(test_simulation):
	"""Test the simulation of a coilgun"""
	data = test_simulation.run()

	assert len(data) == 10