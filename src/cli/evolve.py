from argparse import ArgumentParser
from pathlib import Path
from datetime import datetime

from GA.evolution import Evolution, CrossBreeding
from GA.recorder import CheckpointRecorder
from GA.DNA import DNA, MutationRules
from GA.fitness import CoilFitness
from GA.selection import versus
from utils.path import defaults_path, data_path
from .load_objects import read_DNA_from_template, get_simulation_conf, parse_args


# TODO: Add command line args for settings

def main():
	parser = ArgumentParser(
		description='Evolve a coilgun using a genetinc algorithm'
	)
	# Required arguments
	parser.add_argument(
		'-g', '--generations', 
		type=int,
		help="Number of generations to run the simulation for"
	)
	parser.add_argument(
		'-p', '--population-size',
		type=int,
		help="Size of the population"
	)
	parser.add_argument(
		'-d', '--DNA',
		type=str,
		help="Template file for the base DNA. If not provided a default is used"
	)
	parser.add_argument(
		'-r', '--rules',
		type=str,
		help="Template file for the base DNA. If not provided a default is used"
	)
	parser.add_argument(
		'-c', '--conf',
		default=f"{defaults_path() / 'conf_template.yaml'}",
		type=str,
		help="Template file for the simulation configuration. If not provided a default is used"
	)

	# Parse arguments and execute the program
	args = parse_args(parser.parse_args())

	# Setup evoultion object
	first_generation = [read_DNA_from_template(args["DNA"]) for _ in range(args["population_size"])]
	mutation_rules = MutationRules.read_rules(Path(args["rules"]))
	simulation_conf = get_simulation_conf(args)

	for dna in first_generation:
		dna.randomize_DNA(mutation_rules)

	fitness_func = CoilFitness(simulation_conf=simulation_conf)
	breeding_protocol = CrossBreeding(parent_selection=versus)

	evolution = Evolution(
		generation=first_generation,
		last_gen=args["generations"],
		fitness_func=fitness_func,
		breeding_protocol=breeding_protocol,
		mutation_rules=mutation_rules
	)

	now = datetime.now()
	output_folder = data_path() / f"evolution_{now.strftime('%d-%m-%Y_%H:%M:%S')}"
	recorder = CheckpointRecorder(save_every=10, output_folder=output_folder)

	# Evolve
	evolution.evolve(recorder=recorder)


if __name__ == '__main__':
	main()