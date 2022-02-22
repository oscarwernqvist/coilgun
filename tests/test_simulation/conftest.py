import pytest

from simulation.simulate import CoilgunSimulation, SimulationConf
from coilgun.projectile import MagneticProjectile


@pytest.fixture
def test_simulation_config():
	return SimulationConf(dt=1, max_time=10)

@pytest.fixture
def magnetic_projectile():
	return MagneticProjectile(mass=1, pos=-1, vel=1, m=1)

@pytest.fixture
def test_simulation(solenoid, constant_current_source, magnetic_projectile, test_simulation_config):
	return CoilgunSimulation(
		solenoid, constant_current_source, magnetic_projectile, test_simulation_config
	)
