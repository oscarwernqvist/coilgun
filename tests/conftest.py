import pytest

from coilgun.coil import GeometryCoil
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