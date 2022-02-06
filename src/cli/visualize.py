import matplotlib.pyplot as plt
from argparse import ArgumentParser

from coilgun.coil import CoilConfig
from coilgun.power_source import PowerSourceConfig
from simulation.projectile import ProjectileConf
from simulation.simulate import CoilgunSimulation, SimulationConf
from visualize.coil import draw_coil
from visualize.simulation import draw_simulation


# TODO: Add command line args for settings


def get_coil():
	"""Get a coil"""
	return CoilConfig(coils=[1, 2, 3, 4], inner_diameter=10, wire_diameter=1, resistivity=1e-6).create_coil()

def get_power_source():
	"""Get a power source"""
	return PowerSourceConfig(power_source="ConstantCurrent", kwargs={'current': 1}).create_power_source()

def get_projectile():
	"""Get a power source"""
	return ProjectileConf(mass=1, start_pos=-1, start_vel=1).create_projectile()

def get_simulation_conf():
	"""Get a power source"""
	return SimulationConf(dt=1, max_time=10)

def show_coil(args):
	"""Command line interface for showing a coil"""

	# Create a coil
	coil = get_coil()

	# Create a figure
	fig, ax = plt.subplots()
	ax.set_aspect('equal')

	# Draw the coil
	draw_coil(coil, ax)
	plt.show()

def show_simulation(args):
	"""Command line interface for showing a simulation"""
	coil = get_coil()
	power_source = get_power_source()
	projectile = get_projectile()
	conf = get_simulation_conf()

	sim = CoilgunSimulation(coil, power_source, projectile, conf)

	animation = draw_simulation(sim)
	
	plt.show()

def main():
	parser = ArgumentParser(description='Visualize a coilgun using matplotlib')
	subparsers = parser.add_subparsers(help='Differnet visualizations', dest='prog', required=True)

	# Visualize a coil
	coil_parser = subparsers.add_parser('coil', help='Visualize a coil')

	# Visualize a simulation
	sim_parser = subparsers.add_parser('simulation', aliases=['sim'], help='Visualize a simulation of a coilgun')

	# Parse arguments and execute the right program
	args = parser.parse_args()

	if args.prog == 'coil':
		show_coil(args)
	elif args.prog in ['simulation', 'sim']:
		show_simulation(args)



if __name__ == '__main__':
	main()