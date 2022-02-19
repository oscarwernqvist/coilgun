from typing import Callable
from abc import ABC, abstractmethod
from random import random

from .DNA import DNA, MutationRules
from .fitness import FitnessFunction



class Breeding:
	"""Breed DNA into new DNA"""

	def __init__(self, parent_selection: Callable) -> DNA:
		self.parent_selection = parent_selection

	@abstractmethod
	def breed(self, gen_score: list[tuple[DNA, float]]):
		"""Breed DNA with eachother"""


class CrossBreeding(Breeding):
	"""Breed two parnet DNA with eachother. The offspring takes DNA from both parents with 50% probability"""

	def breed(self, gen_score: list[tuple[DNA, float]]) -> DNA:
		parent_A = self.parent_selection(gen_score).DNA
		parent_B = self.parent_selection(gen_score).DNA

		child = {}

		for param in parent_A.keys():
			child[param] = parent_A[param] if random() < 0.5 else parent_B[param]

		return DNA(child)


class Recorder:
	"""Record details about the evolution"""

	def __init__(self, record_func: Callable):
		self.record_func = record_func
		self.data = []

	def record(self, *args, **kwargs):
		self.data.append(self.record_func(*args, **kwargs))


class Evolution:
	"""Hold data the evolution of the DNA"""

	def __init__(
		self, 
		generation: list[DNA], 
		last_gen: int, 
		fittness_func: FitnessFunction, 
		breeding_protocol: Breeding, 
		mutation_rules: MutationRules
	):
		self.generation = generation
		self.last_gen = last_gen
		self.fittness_func = fittness_func
		self.breeding_protocol = breeding_protocol
		self.mutation_rules = mutation_rules

		self.population = len(generation)
		self.current_gen = 0

		# Keep track of the best DNA
		self.best_score = -float('inf')
		self.best_DNA = None

		# Keep track of the current score
		self.generation_score = None

	def evaluate_gen(self) -> list[tuple[DNA, float]]:
		"""Evaluate the current generation with the fittness function"""
		self.current_gen += 1

		# Calculate the fittness for all DNA in the current generation
		self.generation_score = [(dna, self.fittness_func(dna)) for dna in self.generation]

		# Get the best score and DNA from this generation
		gen_best = max(self.generation_score, key=lambda x: x[1])

		# Update the best DNA
		if gen_best[1] > self.best_score:
			self.best_DNA, self.best_score = gen_best

		return self.generation_score

	def next_gen(self) -> list[DNA]:
		"""Evolve the next generation"""
		self.evaluate_gen()

		# Breed the next generation
		new_gen = [self.breeding_protocol.breed(self.generation_score) for _ in range(self.population)]

		# Mutate the new generation
		for dna in new_gen:
			dna.mutate(rules=self.mutation_rules)

		self.generation = new_gen

		return self.generation

	def evolve(self, recorder: Recorder=None):
		"""Do the evolution"""
		while self.current_gen < self.last_gen:
			new_gen = self.next_gen()

			if recorder is not None:
				recorder.record(self)

	def population_score(self):
		"""Return the average score of the population"""
		if self.generation_score is None:
			self.evaluate_gen()
		return sum([dna_score[1] for dna_score in self.generation_score])
