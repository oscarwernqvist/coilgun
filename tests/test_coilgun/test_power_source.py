from coilgun.power_source import ConstantCurrent, ConstantVoltage


def test_ConstantCurrent(constant_current_source):
	"""Test the return value of the constant current source"""
	assert constant_current_source.current(resistance=1) == 1.0

def test_ConstantVoltage(constant_voltage_source):
	"""Test the return value of the constant current source"""
	R = 10
	V = constant_voltage_source.voltage
	assert constant_voltage_source.current(resistance=R) ==  V / R
