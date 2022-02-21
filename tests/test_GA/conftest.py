import pytest

from random import random

from GA.DNA import DNA, MutationRule, MutationRules
from GA.evolution import CrossBreeding, Evolution
from GA.selection import versus
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

@pytest.fixture
def breeding_vs():
	return CrossBreeding(parent_selection=versus)

@pytest.fixture
def test_evolution(breeding_vs):
	# Create 1000 DNA:s with one gene score between 0 and 1
	simple_DNA = [DNA({"score": random()}) for _ in range(100)]
	# Define the mutation rules
	mutation_rules = MutationRules({"score": MutationRule(0, 1, 0.01)})

	# Define the score function for this DNA
	def simple_fitness(dna: DNA) -> float:
		return dna.DNA["score"]

	# Create the evolution object
	evolution = Evolution(
		generation=simple_DNA, 
		last_gen=100, 
		fitness_func=simple_fitness, 
		breeding_protocol=breeding_vs, 
		mutation_rules=mutation_rules
	)
	return evolution
