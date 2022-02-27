import pytest

from ode_models.inductance_models import exponential_model_of_coil_indunctance, exponential_model_of_coil_indunctance_derivative


@pytest.fixture
def L():
	return exponential_model_of_coil_indunctance(2.0, 3.0, 4.0, 5.0, 6.0)

@pytest.fixture
def dLdx():
	return exponential_model_of_coil_indunctance_derivative(2.0, 3.0, 4.0, 5.0)