from utils import math


def test_sign_function():
	assert math.sign(1.0) == 1.0
	assert math.sign(10) == 1.0
	assert math.sign(-1) == -1.0
	assert math.sign(100.0) == 1.0
	assert math.sign(-11.73e-6) == -1.0
	assert math.sign(0.0) == 1.0