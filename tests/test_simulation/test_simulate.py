


def test_simulation(test_simulation):
	"""Test the simulation of a coilgun"""
	sim_data = test_simulation.run()

	assert sim_data.frames() == 10