import pytest

from GA.DNA import MutationError, DNA


def test_initialization(DNA_template):
	"""Test the information of the DNA"""
	dna = DNA()

	assert not dna.is_initialized()

	dna.read_DNA(DNA_template)

	assert dna.is_initialized()

def test_randomazation(simple_DNA, simple_mutation_rules):
	"""Test if the DNA can be randomized"""
	before_randomazation = simple_DNA.DNA['test_param1']
	# Ransomize
	simple_DNA.randomize_DNA(rules=simple_mutation_rules)

	# assert the randomazation has changed the value
	assert not before_randomazation == simple_DNA.DNA['test_param1']

def test_mutation(simple_DNA, simple_mutation_rules):
	"""Test a muation of the DNA"""
	before_mutation = simple_DNA.DNA['test_param1']

	# Mutate
	simple_DNA.mutate(rules=simple_mutation_rules)

	# assert the mutation has changed the value
	assert not before_mutation == simple_DNA.DNA['test_param1']

def test_mutation_error(simple_DNA, bad_mutation_rules, simple_mutation_rules):
	"""Try to mutate with a bad mutation rule"""

	# With bad rules
	with pytest.raises(MutationError):
		simple_DNA.mutate(rules=bad_mutation_rules)

	# With none initialized DNA and good rules
	with pytest.raises(MutationError):
		DNA().mutate(rules=simple_mutation_rules)

def test_read_DNA(DNA_template):
	"""Try to read DNA from a template"""
	dna = DNA()
	dna.read_DNA(DNA_template)
	assert dna.DNA['test_param1'] == 1.0
	assert dna.DNA['test_param2'] == 2.0
	assert dna.DNA['test_param3'] == 3.0
	assert dna.DNA['test_param4'] == 4.0

def test_write_DNA(tmp_path, simple_DNA):
	"""Try to write DNA to a file"""
	tmp_file = tmp_path / 'test_save.txt'
	simple_DNA.save_DNA(tmp_file)

	assert tmp_file.read_text().strip() == "test_param1: 1.0"