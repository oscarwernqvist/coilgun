


def test_simulation(test_simulation):
	"""Test the simulation of a coilgun"""
	sim_data = test_simulation.run()

	# 10 second simulation with dt=1s
	# This will give one frame for 0, 1, ..., 10
	assert sim_data.frames() == 11