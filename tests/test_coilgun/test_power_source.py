from coilgun.power_source import ConstantCurrent, ConstantVoltage


def test_ConstantCurrent(constant_current_source, geometry_coil):
	"""Test the return value of the constant current source"""
	assert constant_current_source.current(coil=geometry_coil, t=0) == 1.0

	# Change the resistance, this should not effect the current
	geometry_coil.resistivity = 10000
	assert constant_current_source.current(coil=geometry_coil, t=100) == 1.0	

def test_ConstantVoltage(constant_voltage_source, geometry_coil):
	"""Test the return value of the constant current source"""
	R = geometry_coil.resistance()
	V = constant_voltage_source.voltage
	assert constant_voltage_source.current(coil=geometry_coil, t=0) ==  V / R
