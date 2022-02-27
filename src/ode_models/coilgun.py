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
	v0: float 		# Starting velocity of the projectile
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
		return [v, I**2 * dLdx(x) / (2*m), dIdt, -I / (L(x)*C) - R*dIdt / L(x)]

	# Calculate initial conditions
	y0 = [x0, v0, 0.0, V0/L(x0)]

	sol = integrate.solve_ivp(fun=dydt, y0=y0, t_span=(0, t_max))

	t = sol.t
	x, v, I, dIdt = sol.y

	# Calculate voltage over capacitance bank
	#V = L(x)*dIdt + R*I
	V = V0 - 1/C*integrate.cumulative_trapezoid(I, t, initial=0)

	return t, x, v, I, V

