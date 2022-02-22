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
		min_pos, max_pos = sim_data.position_limits()
		min_x = min(min_pos, 0)
		max_x = max(max_pos, sim.coil.length())
		ax.set_xlim([min_x, max_x])
		ax.set_aspect('equal')

		# Draw the coil onto the figure
		draw_coil(sim.coil, ax)

		return (projectile,)

	def update_animation(frame):
		# Update the animation
		pos = sim_data.pos[frame]
		projectile.set_offsets([pos,0])
		return (projectile,)

	animation = FuncAnimation(
		fig, 
		update_animation, 
		frames=range(sim_data.frames()), 
		init_func=init_animation,
		interval=int(1000 * sim_data.total_time() / sim_data.frames()),
		blit=True
	)

	return animation

