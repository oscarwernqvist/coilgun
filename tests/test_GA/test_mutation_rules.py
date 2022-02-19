import pytest

from GA.DNA import MutationRule, MutationRules


def test_mutation_rule(simple_mutation_rule):
	"""Test the mutation rule"""
	assert simple_mutation_rule.min <= simple_mutation_rule.mutate() <= simple_mutation_rule.max

	# This mutation rule has a chance of 100% to mutate so this should always pass
	assert simple_mutation_rule.is_mutating()


@pytest.mark.parametrize(
	("min_value", "max_value", "rate"), 
	[
		(None, None, None),
		(None, 1, 1),
		(1, None, 1),
		(1, 1, None)
	]
)
def test_initialization_of_rule(min_value, max_value, rate):
	"""Test the initialization of a rule"""
	rule = MutationRule(min_value, max_value, rate)

	assert not rule.is_initialized()

	rule = MutationRule.from_dict({'min': 1, 'max': 1, 'rate': 1})

	assert rule.is_initialized()

def test_initialization_of_rules(rules_template):
	"""Test the initialization of a rule"""
	rule = MutationRules()

	assert not rule.is_initialized()

	rule = MutationRules.read_rules(rules_template)

	assert rule.is_initialized()

def test_rule_converstion_2_dict():
	"""Test the rule conversion to and from a dictionary"""
	rule = MutationRule.from_dict({'min': 1.0, 'max': 1.0, 'rate': 1.0})

	assert rule.min == 1.0
	assert rule.max == 1.0
	assert rule.rate == 1.0

	rule_dict = rule.to_dict()

	assert rule_dict['min'] == 1.0
	assert rule_dict['max'] == 1.0
	assert rule_dict['rate'] == 1.0

def test_read_rules(rules_template):
	"""Try to read DNA from a template"""
	rules = MutationRules.read_rules(rules_template)

	rule1 = rules.rule('test_param1')
	rule2 = rules.rule('test_param2')

	assert rule1.min == 1.0
	assert rule1.max == 1.0
	assert rule1.rate == 1.0

	assert rule2.min == 2.0
	assert rule2.max == 2.0
	assert rule2.rate == 2.0

def test_save_rules(tmp_path, simple_mutation_rules):
	"""Try to save the mutation rules"""
	tmp_file = tmp_path / 'test_save.txt'
	simple_mutation_rules.save_rules(tmp_file)

	assert tmp_file.read_text().strip() == "test_param1:\n  max: 10.0\n  min: 1.0\n  rate: 1.0"
