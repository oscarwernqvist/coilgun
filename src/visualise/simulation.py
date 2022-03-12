import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from simulation.simulate import CoilgunSimulation
from visualise.coil import draw_coil

from GA.DNA import DNA

from ode_models.coilgun import ode_solver_coilgun, calculate_efficiency
from ode_models.inductance_models import (
	exponential_model_of_coil_indunctance, 
	exponential_model_of_coil_indunctance_derivative,
	parmas_for_exponential_model,
	solenoid_resistance
)


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

def plot_ode_solution(dna: DNA, t_max: float, t_steps: int):
	A, B, C, D, E = parmas_for_exponential_model(
		mu_r=dna["projectile_mu_r"],
		N=dna["solenoid_turns"],
		r=dna["solenoid_radius"],
		l=dna["solenoid_length"]
	)

	L = exponential_model_of_coil_indunctance(A, B, C, D, E)
	dLdx = exponential_model_of_coil_indunctance_derivative(A, B, C, D)
	R = solenoid_resistance(
		N=dna["solenoid_turns"],
		r=dna["solenoid_radius"],
		A=dna["wire_cross_sectional_area"],
		resistivity=dna["solenoid_resistivity"]
	)

	t, x, v, I, V, dIdt = ode_solver_coilgun(
		C=dna["capacitance"],
		R=R,
		m=dna["projectile_mass"],
		L=L,
		dLdx=dLdx,
		x0=dna["projectile_start_pos"],
		x1=dna["projectile_end_pos"],
		V0=dna["capacitance_voltage"],
		v0=dna["projectile_velocity"],
		t_max=t_max,
		t_steps=t_steps
	)

	F = I**2 * dLdx(x) / 2

	v0, v1 = v[0], v[-1]
	V0, V1 = V[0], V[-1]

	n = calculate_efficiency(
		v0=v0,
		v1=v1,
		V0=V0,
		V1=V1,
		m=dna["projectile_mass"],
		C=dna["capacitance"]
	)

	print(f"Coilgun efficiency: {n}")

	fig, ((pos_ax, vel_ax), (volt_ax, current_ax), (force_ax, empty_ax)) = plt.subplots(3,2)

	pos_ax.plot(t, x*1e3)
	pos_ax.set(ylabel="Position [mm]")
	vel_ax.plot(t, v)
	vel_ax.set(ylabel="Hastighet [m/s]")
	volt_ax.plot(t, V)
	volt_ax.set(ylabel="Voltage i Kapacitansbank [V]")
	current_ax.plot(t, I)
	current_ax.set(ylabel="Ström genom spolen [A]")
	force_ax.plot(x*1e3, F)
	force_ax.set(ylabel="Kraft på projektilen [N]")
	force_ax.set(xlabel="Projektilens position [mm]")

	plt.show()
