from cli.evolve import evolution_parser, evolution
from cli.load_objects import parse_args

import functools
from time import time

import numpy as np

def timer(func):
	"""
	Decorator that will print the time of execution for a function
	"""
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		t1 = time()
		func(*args, **kwargs)
		t2 = time()

		return t2 - t1
	return wrapper

# Add decorator to the evolution function
evolution = timer(evolution)

parser = evolution_parser()

generations_nb = range(10, 20+1, 10)
population_nb = range(10, 20+1, 10)

timing_info = []

print("#"*40)
for generations in generations_nb:
	for population in population_nb:
		print(f"Running evolution for {generations} generations with a population of {population}.")
		args = parse_args(parser.parse_args([
			"--ode", 
			"--generations", 
			str(generations),
			"--population-size",
			str(population)
			]))
		time_for_execution = evolution(args)
		timing_info.append(time_for_execution)

		print(f"Time: {time_for_execution}")

		print("#"*40)

X, Y = np.meshgrid(generations_nb, population_nb)
timing_info = np.reshape(timing_info, (len(generations_nb), len(population_nb)))

XY = X*Y

c = np.linalg.lstsq(XY.flatten()[None,:], timing_info.flatten()[None,:], rcond=None)[0].T

print(c)

