import numpy as np
import matplotlib.pyplot as plt

from ode_models.coilgun import ode_solver_coilgun
from ode_models.inductance_models import exponential_model_of_coil_indunctance, exponential_model_of_coil_indunctance_derivative


L = exponential_model_of_coil_indunctance(A=156e-6, B=0.004*10**(3*2.06), C=0, D=2.06, E=131.7e-6)
dLdx = exponential_model_of_coil_indunctance_derivative(A=156e-6, B=0.004*10**(3*2.06), C=0, D=2.06)

C = 1600e-6
R = 0.4
m = 8e-3

V0 = 300
x0 = -10e-3

y0 = [x0, 0.0, 0.0, V0/L(x0)]

t, x, v, I, V = ode_solver_coilgun(
	C=C,
	R=R,
	m=m,
	L=L,
	dLdx=dLdx,
	y0=y0,
	t_span=[0, 0.01]
)

fig, ((pos, vel), (volt, current)) = plt.subplots(2,2)

pos.plot(t, x*1e3)
pos.set(ylabel="Position [mm]")
vel.plot(t, v)
vel.set(ylabel="Hastighet [m/s]")
volt.plot(t, V)
volt.set(ylabel="Voltage i Kapacitansbank [V]")
current.plot(t, I)
current.set(ylabel="Ström genom spolen [A]")

# x = np.linspace(-30, 60)*1e-3

# plt.plot(x*1e3, L(x)*1e6)
# plt.ylabel("uH")
# plt.xlabel("mm")

plt.show()

# L = exponential_model_of_coil_indunctance(A=156, B=0.004, C=30.0, D=2.06, E=131.7)
# dLdx = exponential_model_of_coil_indunctance_derivative(A=156, B=0.004, C=30.0, D=2.06)
# x = np.linspace(0, 90)

# plt.plot(x, L(x))
# plt.show()
# plt.plot(x, dLdx(x))
# plt.show()