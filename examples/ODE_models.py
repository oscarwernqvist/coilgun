import numpy as np
import matplotlib.pyplot as plt

from ode_models.coilgun import ode_solver_coilgun
from ode_models.inductance_models import (
	exponential_model_of_coil_indunctance, 
	exponential_model_of_coil_indunctance_derivative,
	parmas_for_exponential_model
)


# Parmas
mu_r = 5
N = 500
r = 10e-3
l = 50e-3

A, B, C, D, E = parmas_for_exponential_model(mu_r, N, r, l)

print(f"{A=}, {B=}, {C=}, {D=} and {E=}")

L = exponential_model_of_coil_indunctance(A, B, C, D, E)
dLdx = exponential_model_of_coil_indunctance_derivative(A, B, C, D)

C = 1600e-6
R = 0.4
m = 8e-3

V0 = 300
x0 = -50e-3

t, x, v, I, V = ode_solver_coilgun(
	C=C,
	R=R,
	m=m,
	L=L,
	dLdx=dLdx,
	x0=x0,
	t_max=0.003,
	V0=V0,
	v0=0.0,
	x1=20e-3,
	t_steps=100
)

fig, ((pos_ax, vel_ax), (volt_ax, current_ax)) = plt.subplots(2,2)

pos_ax.plot(t, x*1e3)
pos_ax.set(ylabel="Position [mm]")
vel_ax.plot(t, v)
vel_ax.set(ylabel="Hastighet [m/s]")
volt_ax.plot(t, V)
volt_ax.set(ylabel="Voltage i Kapacitansbank [V]")
current_ax.plot(t, I)
current_ax.set(ylabel="Ström genom spolen [A]")

# x = np.linspace(-30, 60)*1e-3

# plt.plot(x*1e3, L(x)*1e6)
# plt.ylabel("uH")
# plt.xlabel("mm")

plt.show()

# x = np.linspace(-2*l, 2*l)

# plt.plot(x, L(x))
# plt.show()
# plt.plot(x, dLdx(x))
# plt.show()