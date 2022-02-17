from .DNA import DNA, MutationRules

from typing import Callable
from abc import ABC, abstractmethod
from random import random


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


class Evolution:
	"""Hold data the evolution of the DNA"""

	def __init__(
		self, 
		generation: list[DNA], 
		last_gen: int, 
		fittness_func: Callable, 
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

	def evaluate_gen(self) -> list[tuple[DNA, float]]:
		"""Evaluate the current generation with the fittness function"""
		self.current_gen += 1

		# Calculate the fittness for all DNA in the current generation
		generation_score = [(dna, self.fittness_func(dna)) for dna in self.generation]

		# Get the best score and DNA from this generation
		gen_best = max(generation_score, key=lambda x: x[1])

		# Update the best DNA
		if gen_best[1] > self.best_score:
			self.best_DNA, self.best_score = gen_best

		return generation_score

	def next_gen(self) -> list[DNA]:
		"""Evolve the next generation"""
		generation_score = self.evaluate_gen()

		# Breed the next generation
		return [self.breeding_protocol.breed(generation_score) for _ in range(self.population)]

	def evolve(self):
		"""Do the evolution"""
		while self.current_gen < self.last_gen:
			new_gen = self.next_gen()

			# Mutate the new generation
			for dna in new_gen:
				dna.mutate(rules=self.mutation_rules)

			self.generation = new_gen
