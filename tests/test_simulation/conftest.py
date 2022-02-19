import pytest

from simulation.simulate import CoilgunSimulation, SimulationConf
from simulation.projectile import Projectile1D


@pytest.fixture
def test_simulation_config():
	return SimulationConf(dt=1, max_time=10)

@pytest.fixture
def test_projectile():
	return Projectile1D(mass=1, pos=-1, vel=1)

@pytest.fixture
def test_simulation(geometry_coil, constant_current_source, test_projectile, test_simulation_config):
	return CoilgunSimulation(
		geometry_coil, constant_current_source, test_projectile, test_simulation_config
	)
