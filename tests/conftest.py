import pytest

from coilgun.coil import GeometryCoil, Solenoid
from coilgun.power_source import ConstantCurrent, ConstantVoltage


@pytest.fixture
def constant_current_source():
	return ConstantCurrent(current=1)

@pytest.fixture
def constant_voltage_source():
	return ConstantVoltage(voltage=30)

@pytest.fixture
def geometry_coil():
	return GeometryCoil(
		coils=[1,2,4],
		inner_diameter=5,
		wire_diameter=1,
		resistivity=1e-6
	)

@pytest.fixture
def solenoid():
	return Solenoid(
		L=0.1,
		N=100,
		inner_diameter=0.1,
		wire_diameter=1e-3,
		resistivity=1e-9
	)