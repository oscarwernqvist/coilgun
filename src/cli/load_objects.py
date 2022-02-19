from pathlib import Path

from GA.fitness import coil_from_DNA, power_source_from_DNA, projectile_from_DNA
from GA.DNA import DNA
from simulation.simulate import SimulationConf

def read_DNA_from_template(template):
	"""Read DNA from a template file"""
	return DNA.read_DNA(Path(template))

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
	"""Get the configuration for a simulation"""
	return SimulationConf(dt=1, max_time=10)