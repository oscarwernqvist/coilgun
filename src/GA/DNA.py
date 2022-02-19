import random
import yaml
from pathlib import Path


class MutationRule:
	"""
	A rule for mutation

	'min': float,	# Minimum possible value
	'max': float,	# Maximum possible value
	'rate': 0-1		# The probability that this gene will mutate
	"""

	def __init__(self, min_value: float=None, max_value: float=None, rate: float=None):
		self.min = min_value
		self.max = max_value
		self.rate = rate

	def is_initialized(self) -> bool:
		"""The rule is initialized only if all vars are not None"""
		return self.min is not None and self.max is not None and self.rate is not None

	def is_mutating(self) -> bool:
		if not self.is_initialized():
			raise MutationError
		return random.random() < self.rate

	def mutate(self) -> float:
		if not self.is_initialized():
			raise MutationError
		return random.random() * (self.max - self.min) + self.min

	def to_dict(self) -> dict:
		"""Convert the rule to a dict"""
		return {'min': self.min, 'max': self.max, 'rate': self.rate}

	@classmethod
	def from_dict(cls, rules: dict) -> 'MutationRule':
		"""
		Factory method for creating a rule
		from a dict
		"""
		return cls(
			min_value=rules['min'], 
			max_value=rules['max'],
			rate=rules['rate']
		)


class MutationRules:
	"""A class that holds all the mutation rules"""

	def __init__(self, rules: dict=None):
		self.rules = rules

	def is_initialized(self):
		"""The rules are initialized if rules has some content"""
		return self.rules is not None

	def all_rules(self) -> list[str]:
		"""Return a list of all parameters in the rules"""
		return self.rules.keys()

	def rule(self, rule_name) -> MutationRule:
		"""Return a specific rule"""
		return self.rules[rule_name]

	@classmethod
	def read_rules(cls, rules_file: Path) -> 'MutationRules':
		"""
		Factory method for reading rules data from a yaml file
		and creating an object from them
		"""
		with rules_file.open() as yaml_file:
			rules_dict = yaml.safe_load(yaml_file)

		# Unpack the rules
		rules = {param: MutationRule().from_dict(rule) for param, rule in rules_dict.items()}

		return cls(rules=rules)

	def save_rules(self, rules_file: Path) -> str:
		"""Save the rules to a yaml file"""

		# Convert to a dict of dicts so it can be saved as a yaml file
		rules_dict = {param: rule.to_dict() for param, rule in self.rules.items()}

		with rules_file.open('w') as yaml_file:
			yaml_dump = yaml.dump(rules_dict, yaml_file)
		return yaml_dump


class DNA:
	"""
	This class will function as DNA for a digital creature.
	
	DNA (dict): A dictionary filled with information about an objects parameters
	{
		'<param name>': float or None,	# If None a random value will be initialized
	}
	"""

	def __init__(self, DNA: dict=None):
		self.DNA = DNA

	def __getitem__(self, key):
		"""Alows for use of [] on the DNA object"""
		return self.DNA[key]

	def randomize_DNA(self, rules: MutationRules):
		"""Randomize the DNA"""
		if not self.is_initialized():
			raise MutationError

		# Only randomize params that can be mutated
		for param in rules.all_rules():
			if param not in self.DNA.keys():
				raise MutationError

			self.DNA[param] = rules.rule(param).mutate()

	def is_initialized(self) -> bool:
		return self.DNA is not None

	def mutate(self, rules: MutationRules):
		"""Mutate the DNA"""
		if not self.is_initialized():
			raise MutationError

		for param in rules.all_rules():
			if param not in self.DNA.keys():
				raise MutationError

			rule = rules.rule(param)

			# Mutate the param
			if rule.is_mutating():
				self.DNA[param] = rule.mutate()

	@classmethod
	def read_DNA(cls, dna_file: Path) -> 'DNA':
		"""
		Factory method for reading DNA data from a yaml file
		and creating an object from it
		"""
		with dna_file.open() as yaml_file:
			DNA = yaml.safe_load(yaml_file)

		return cls(DNA=DNA)

	def save_DNA(self, dna_file: Path) -> str:
		"""Save the DNA to a yaml file"""
		with dna_file.open('w') as yaml_file:
			yaml_dump = yaml.dump(self.DNA, yaml_file)
		return yaml_dump


# TODO: More specific errors
class MutationError(Exception):
	pass