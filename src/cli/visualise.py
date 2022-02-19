import matplotlib.pyplot as plt
from argparse import ArgumentParser
from pathlib import Path

from GA.fitness import coil_from_DNA, power_source_from_DNA, projectile_from_DNA
from GA.DNA import DNA
from simulation.simulate import CoilgunSimulation, SimulationConf
from visualise.coil import draw_coil
from visualise.simulation import draw_simulation
from utils.path import defaults_path


# TODO: Add command line args for settings

def read_DNA_from_template(template):
	"""Read DNA from a template file"""
	dna = DNA()
	dna.read_DNA(Path(template))
	return dna

def get_coil(args):
	"""Get a coil from a template file"""
	coil_dna = read_DNA_from_template(args.coil)
	return coil_from_DNA(coil_dna)
	# return CoilConfig(coils=[1, 2, 3, 4], inner_diameter=10, wire_diameter=1, resistivity=1e-6).create_coil()

def get_power_source(args):
	"""Get a power source from a template file"""
	power_dna = read_DNA_from_template(args.power_source)
	return power_source_from_DNA(power_dna)
	# return PowerSourceConfig(power_source="ConstantCurrent", kwargs={'current': 1}).create_power_source()

def get_projectile(args):
	"""Get a projectile from a template file"""
	projectile_dna = read_DNA_from_template(args.projectile)
	return projectile_from_DNA(projectile_dna)
	# return ProjectileConf(mass=1, start_pos=-1, start_vel=1).create_projectile()

def get_simulation_conf(args):
	"""Get a power source"""
	return SimulationConf(dt=1, max_time=10)

def show_coil(args):
	"""Command line interface for showing a coil"""

	# Create a coil
	coil = get_coil(args)

	# Create a figure
	fig, ax = plt.subplots()
	ax.set_aspect('equal')

	# Draw the coil
	draw_coil(coil, ax)
	plt.show()

def show_simulation(args):
	"""Command line interface for showing a simulation"""
	coil = get_coil(args)
	power_source = get_power_source(args)
	projectile = get_projectile(args)
	conf = get_simulation_conf(args)

	sim = CoilgunSimulation(coil, power_source, projectile, conf)

	animation = draw_simulation(sim)
	
	plt.show()

def main():
	parser = ArgumentParser(
		description='Visualise a coilgun using matplotlib'
	)
	subparsers = parser.add_subparsers(
		help='Differnet visualizations', 
		dest='prog', 
		required=True
	)

	# Visualise a coil
	coil_parser = subparsers.add_parser(
		'coil', 
		help='Visualise a coil'
	)
	coil_parser.add_argument(
		'-c', '--coil', 
		default=f"{defaults_path() / 'coil_template.yaml'}",
		type=str,
		help="Template file for the coil. If not provided a default is used"
	)

	# Visualise a simulation
	sim_parser = subparsers.add_parser(
		'simulation', 
		aliases=['sim'], 
		help='Visualise a simulation of a coilgun'
	)
	sim_parser.add_argument(
		'-c', '--coil', 
		default=f"{defaults_path() / 'coil_template.yaml'}",
		type=str,
		help="Template file for the coil. If not provided a default is used"
	)
	sim_parser.add_argument(
		'-s', '--power-source', 
		default=f"{defaults_path() / 'power_template.yaml'}",
		type=str,
		help="Template file for the power source. If not provided a default is used"
	)
	sim_parser.add_argument(
		'-p', '--projectile', 
		default=f"{defaults_path() / 'projectile_template.yaml'}",
		type=str,
		help="Template file for the projectile. If not provided a default is used"
	)

	# Parse arguments and execute the right program
	args = parser.parse_args()

	if args.prog == 'coil':
		show_coil(args)
	elif args.prog in ['simulation', 'sim']:
		show_simulation(args)



if __name__ == '__main__':
	main()