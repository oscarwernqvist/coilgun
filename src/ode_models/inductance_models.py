import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import linregress

import matplotlib.pyplot as plt


"""
Fit data of the inductance in a coil to the function
L(x) = A*exp(-B|x|^C) + D
"""

def L(x, A, B, C, D):
	return A*np.exp(-B*np.power(np.abs(x), C)) + D

def plot_relation(x, y, ax1, ax2):
	"""Find and plot the relation between x and y"""
	logx = np.log(x)
	logy = np.log(y)

	res = linregress(logx, logy)

	ax1.scatter(logx, logy, marker="o", c="b", label="Original data")
	ax1.plot(logx, res.intercept + res.slope*logx, 'r', label=f"Fitted line with a slope {res.slope:.4f}")
	ax1.legend()

	ax2.scatter(x, y, marker="o", c="b", label="Original data")
	ax2.plot(x, x**res.slope, 'r', label=f"Fitted line with an exponent {res.slope:.4f}")
	ax2.legend()


data_file = None

if data_file is None:
	xdata = []
	ydata = []
	Ns = np.arange(5) + 1 
	for N in Ns:

		x = np.linspace(-5, 5, 100)

		y0 = L(x, 5*N**2, 2, 2, N)

		rng = np.random.default_rng()
		y_noise = 0.2 * rng.normal(size=x.size)

		y = y0 + y_noise

		xdata.append(x)
		ydata.append(y)

else: 
	pass # Read data from file


# Fit A, B, C, D to the data
ABCDs = []
for x, y in zip(xdata, ydata):
	ABCD, _ = curve_fit(L, x, y)
	ABCDs.append(ABCD)
ABCDs = np.array(ABCDs)

fig1, ((ax_A1, ax_B1), (ax_C1, ax_D1)) = plt.subplots(2, 2)
fig2, ((ax_A2, ax_B2), (ax_C2, ax_D2)) = plt.subplots(2, 2)

# Find relation to A
# ax_A1.scatter(np.log(Ns), np.log(ABCDs[:,0]))

# ax_A2.scatter(Ns, ABCDs[:,0])
# ax_A2.set_ylim(bottom=0)
plot_relation(Ns, ABCDs[:,0]-Ns**2, ax_A1, ax_A2)
plot_relation(Ns, ABCDs[:,1], ax_B1, ax_B2)
plot_relation(Ns, ABCDs[:,2], ax_C1, ax_C2)
plot_relation(Ns, ABCDs[:,3], ax_D1, ax_D2)

plt.show()

# plt.scatter(xdata, ydata, marker='*', c='b', label='data')
# plt.plot(
# 	xdata, 
# 	L(xdata, *popt), 
# 	'r-',
# 	label='fit: A=%5.3f, B=%5.3f, C=%5.3f, D=%5.3f' % tuple(popt)
# )
# plt.xlabel('x')
# plt.ylabel('y')
# plt.legend()
# plt.show()

