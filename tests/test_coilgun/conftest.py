import pytest

from coilgun.coil import Coil
from coilgun.power_source import ConstantCurrent, ConstantVoltage


@pytest.fixture
def constant_current_source():
	return ConstantCurrent(I=1)

@pytest.fixture
def constant_voltage_source():
	return ConstantVoltage(voltage=30)

@pytest.fixture
def constant_current_coil(constant_current_source):
	return Coil(
		coils=[1,2,4],
		inner_diameter=5,
		wire_diameter=1,
		resistivity=1e-6,
		power_source=constant_current_source)

@pytest.fixture
def constant_voltage_coil(constant_voltage_source):
	return Coil(
		coils=[1,2,4],
		inner_diameter=5,
		wire_diameter=1,
		resistivity=1e-6,
		power_source=constant_voltage_source)