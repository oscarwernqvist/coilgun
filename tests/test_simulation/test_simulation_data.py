from simulation.simulate import SimulationData


def test_energy_calculations():
	"""Try to calculate the energy consumtion and gain"""
	sim_data = SimulationData(
		time=[0, 1, 2, 3],
		pos=[0, 1, 2, 3],
		vel=[2, 2, 3, 4],
		energy=[0, 1, 2, 3]
	)

	assert sim_data.energy_consumption() == 6
	assert sim_data.energy_gain(projectile_mass=3) == 18