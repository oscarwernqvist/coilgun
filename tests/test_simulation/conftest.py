import pytest

from simulation.simulate import CoilgunSimulation, SimulationConf
from simulation.projectile import Projectile1D, ProjectileConf


@pytest.fixture
def test_simulation_config():
	return SimulationConf(dt=1, max_time=10)

@pytest.fixture
def test_projectile_conf():
	return ProjectileConf(mass=1, start_pos=-1, start_vel=1)

@pytest.fixture
def test_projectile(test_projectile_conf):
	return test_projectile_conf.create_projectile()

@pytest.fixture
def test_simulation(test_coil, constant_current_source, test_projectile, test_simulation_config):
	return CoilgunSimulation(
		test_coil, constant_current_source, test_projectile, test_simulation_config
	)
