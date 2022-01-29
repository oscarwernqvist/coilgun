import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from simulation.simulate import CoilgunSimulation
from visualize.coil import draw_coil


def draw_simulation(sim: CoilgunSimulation) -> FuncAnimation:
	"""Visualize the simulation"""

	# Run the simulation
	sim_data = sim.run()

	# Create figure
	fig, ax = plt.subplots()
	ax.set_aspect('equal')

	draw_coil(sim.coil, ax)

	plt.show()

