import numpy as np
from scipy import integrate
from typing import Callable

def ode_solver_coilgun(
	C: float, 		# Capacitance of the capaitance bank
	R: float, 		# Resistance of the coil
	m: float, 		# Mass of the projectile
	L: Callable, 	# Function that calculates the inductance of the coil at the position x
	dLdx: Callable, # Function that calculates the derivative of the inductance at the position x
	x0: float,		# Starting position relative to the center of the coil for the projectile
	t_max: float,	# Maximum time for the simulation
	V0: float,		# Starting voltage over the capacitance bank
	v0: float, 		# Starting velocity of the projectile
	x1: float=None, # If present the simulation will end when the projectile passes this point
	t_steps: int=None # Minimum steps the solver should take
):
	"""
	ODE solver for a coilgun.
	This method assumes that the inductance is a known function of the position
	"""

	def dydt(t, y):
		"""
		Calculate the derivative of the state [x, v, I, dIdt]
		"""
		x, v, I, dIdt = y

		dvdt = I**2 * dLdx(x) / (2*m)
		dIdt2 = -I / (L(x)*C) - R*dIdt / L(x) - dIdt*dLdx(x)*v/L(x)

		return [v, dvdt, dIdt, dIdt2]

	def end_point_reached(t, y):
		"""Stop the solver if the end point is reached"""
		return y[0] - x1
	# Stop at event
	end_point_reached.terminal = True

	# Set the event
	event = end_point_reached if x1 is not None else None

	# Calculate maximum time step
	t_step = t_max / t_steps if t_steps is not None else np.inf

	# Calculate initial conditions
	y0 = [x0, v0, 0.0, V0/L(x0)]

	sol = integrate.solve_ivp(
		fun=dydt, 
		y0=y0, 
		t_span=(0, t_max), 
		events=event,
		max_step=t_step
	)

	t = sol.t
	x, v, I, dIdt = sol.y

	# Calculate voltage over capacitance bank
	#V = L(x)*dIdt + R*I
	V = V0 - 1/C*integrate.cumulative_trapezoid(I, t, initial=0)

	return t, x, v, I, V

def calculate_efficiency(
	v0: float,	# Starting velocity for the projectile
	v1: float, 	# Ending velocity for the projectile
	V0: float, 	# Stating voltage over the capacitance bank
	V1: float,	# Ending voltage over the capacitance bank
	m: float, 	# Mass of the projectile
	C: float 	# Capacitance of the capacitnace bank
) -> float:
	"""
	Calculate the efficiency of a coilgun
	"""
	# Kinetic energy gained of the projectile
	dE_k = m*(v1**2-v0**2)/2
	# Energy lost in the capacitance bank
	dE_C = C*(V0**2-V1**2)/2
	
	return dE_k / dE_C

