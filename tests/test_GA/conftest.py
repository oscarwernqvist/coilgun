import pytest

from GA.DNA import DNA, MutationRule, MutationRules
from utils import path


@pytest.fixture
def simple_mutation_rule():
	return MutationRule(min_value=1.0, max_value=10.0, rate=1.0)

@pytest.fixture
def simple_mutation_rules(simple_mutation_rule):
	return MutationRules({'test_param1': simple_mutation_rule})

@pytest.fixture
def bad_mutation_rules(simple_mutation_rule):
	return MutationRules({'bad_param': simple_mutation_rule})

@pytest.fixture
def simple_DNA():
	return DNA({'test_param1': 1.0})

@pytest.fixture
def gen_score():
	dna_A = DNA({str(i): i + 1 for i in range(100)})
	dna_B = DNA({str(i): 2*i + 2 for i in range(100)})
	dna_C = DNA({str(i): 3*i + 3 for i in range(100)})

	return [(dna_A, 1), (dna_B, 0), (dna_C, -1)]

@pytest.fixture
def DNA_template():
	return path.test_path() / 'test_GA' / 'templates' / 'test_template_DNA.yaml'

@pytest.fixture
def rules_template():
	return path.test_path() / 'test_GA' / 'templates' / 'test_template_rules.yaml'
