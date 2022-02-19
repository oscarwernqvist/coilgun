import matplotlib.pyplot as plt
from argparse import ArgumentParser

from visualise.coil import draw_coil
from visualise.simulation import draw_simulation
from simulation.simulate import CoilgunSimulation
from utils.path import defaults_path
from .load_objects import get_coil, get_power_source, get_projectile, get_simulation_conf


# TODO: Add command line args for settings

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