from GA.DNA import DNA, MutationRules, MutationRule
from GA.evolution import CrossBreeding, Evolution
from GA.selection import versus

from random import random


def test_cross_breeding(gen_score):
	"""Test the cross breeding"""
	breeding = CrossBreeding(versus)

	dna_A = gen_score[0][0]
	dna_B = gen_score[1][0]
	# This is the worst DNA
	# It should never give any genes
	dna_C = gen_score[2][0]

	for _ in range(1000):
		new_dna = breeding.breed(gen_score)

		for key in new_dna.DNA.keys():
			# Make sure the DNA only has genes from A or B
			assert not new_dna.DNA[key] == dna_C.DNA[key]
			assert new_dna.DNA[key] == dna_A.DNA[key] or new_dna.DNA[key] == dna_B.DNA[key]

def test_evolution():
	"""
	Test the evolution algorithm with a simple DNA.
	The DNA only has one gene, one float between 0 and 1,
	and the fitness function will try to maximize this
	"""
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
		breeding_protocol=CrossBreeding(parent_selection=versus), 
		mutation_rules=mutation_rules
	)

	# Evaluate the current population score
	start_score = sum([dna_score[1] for dna_score in evolution.evaluate_gen()])

	# Do the evolution
	evolution.evolve()

	# New population score
	end_score = sum([dna_score[1] for dna_score in evolution.evaluate_gen()])

	# The population score should be higher now
	assert end_score > start_score
