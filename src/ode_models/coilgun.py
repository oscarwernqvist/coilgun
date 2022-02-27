from scipy.integrate import solve_ivp
from typing import Callable

def ode_solver_coilgun(C: float, R: float, m: float, L: Callable, dLdx: Callable, y0: list, t_span: tuple):
	"""
	ODE solver for a coilgun.
	This method assumes that the inductance is a known function of the position

	params:
		C: Capacitance of the capaitance bank
		R: Resistance of the coil
		m: Mass of the projectile
		L: Function that calculates the inductance of the coil at the position x
		dLdx: Function that calculates the derivative of the inductance at the position x
	"""

	def dydt(t, y):
		"""
		Calculate the derivative of the state [x, v, I, dIdt]
		"""
		x, v, I, dIdt = y
		return [v, I**2 * dLdx(x) / (2*m), dIdt, -I / (L(x)*C) - R*dIdt / L(x)]

	sol = solve_ivp(fun=dydt, y0=y0, t_span=t_span)

	t = sol.t
	x, v, I, dIdt = sol.y

	# Calculate voltage over capacitance bank
	V = L(x)*dIdt + R*I

	return t, x, v, I, V

