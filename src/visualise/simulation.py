import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from simulation.simulate import CoilgunSimulation
from visualise.coil import draw_coil


def draw_simulation(sim: CoilgunSimulation) -> FuncAnimation:
	"""Visualise the simulation"""

	# Run the simulation
	sim_data = sim.run()

	# Create figure
	fig, ax = plt.subplots()

	# Setup the projectile object
	projectile = ax.scatter([], [], marker='o', c='red')

	def init_animation():
		# Init the animation
		ax.set_xlim(*sim_data.position_limits())
		ax.set_aspect('equal')

		# Draw the coil onto the figure
		draw_coil(sim.coil, ax)

		return (projectile,)

	def update_animation(frame):
		# Update the animation
		pos = sim_data.pos[frame]
		projectile.set_offsets([pos,0])
		return (projectile,)

	animation = FuncAnimation(fig, update_animation, frames=range(sim_data.frames()), init_func=init_animation, blit=True)

	return animation

