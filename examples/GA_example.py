"""
This is an example file that will show how the 
genetic algorithm works and how it is implemented.

It will do this by trying to evolve a population
that only has one trait, a single float between
0 and 1. The algorithm will try to maximize this value
"""

from GA.DNA import DNA, MutationRules, MutationRule
from GA.evolution import Evolution, CrossBreeding, Recorder
from GA.selection import versus
from matplotlib import pyplot as plt
import random


def main():
	# Create the population
	pop = [DNA({"score": random.random()}) for _ in range(100)]

	# Define the mutation rules
	mutation_rules = MutationRules(
		rules={
			"score": MutationRule(
				min_value=0, 
				max_value=1, 
				rate=0.01
			)
		}
	)

	# Define the score function for this DNA
	def simple_fittness(dna: DNA) -> float:
		return dna.DNA["score"]

	# Create the evolution object
	evolution = Evolution(
		generation=pop, 
		last_gen=10, 
		fittness_func=simple_fittness, 
		breeding_protocol=CrossBreeding(parent_selection=versus), 
		mutation_rules=mutation_rules
	)

	def record_func(evolution_object, *args, **kwargs):
		"""This function will be called every iteration of the evolution"""
		return evolution_object.population_score()

	# Create a Recorder object to record information about the evoulution
	recorder = Recorder(record_func)

	# Start the evolution
	evolution.evolve(recorder=recorder)

	# Plot the result
	plt.plot(recorder.data)
	plt.show()


if __name__ == '__main__':
	main()
