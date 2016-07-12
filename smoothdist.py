import numpy as np
from scipy.interpolate import interp1d
import sys
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Rectangle

# import data and isolate x and y
if (len(sys.argv) != 4):
	print ("Usage: smoothing.py <input> <smoothed output> <exceeding threshold>")
	sys.exit(2)
data = np.loadtxt(sys.argv[1])
x = data[:,0]
y = data[:,1]

# receive window parameter from user
window = float(input("Window size: ")) / 2

# generate smoothed curve based on window
x2 = np.extract(x >= x[0] + window, x)
x2 = np.extract(x2 <= x2.max() - window, x2)
y2 = np.zeros(x2.size)
tolerance = np.mean(np.diff(x2)) / 100
for i in range(0, y2.size):
	index = np.nonzero(x == x2[i])[0][0]
	min = index
	max = index
	while min > 0 and x[index] - x[min - 1] <= window + tolerance:
		min -= 1
	while max < y.size - 1 and x[max + 1] - x[index] <= window + tolerance:
		max += 1
	y2[i] = np.mean(y[min:max+1])

#reassemble data and output to file
smoothed = np.rot90(np.vstack((y2,x2)), 3)
np.savetxt(sys.argv[2], smoothed, delimiter='\t')

# generate cubic spline interpolation and plot
poly = interp1d(x2, y2, kind='cubic')
xi = np.linspace(x2[0], x2[x2.size - 1], num=(x2[x2.size - 1] - x2[0])/.001, endpoint=True)

# calculate diff between input and curve
globmin = np.where(x == x2[0])[0][0]
globmax = np.where(x == x2[x2.size - 1])[0][0]
ydiff = y[globmin:globmax + 1] - poly(x2)

# set initial threshold (adjustable in graph by user)
threshold = .0025

# identify max points of regions exceeding threshold
def calcjumps(t):
	jumps = np.extract(ydiff > t, x2)
	maxjumps = np.array([])
	i = 0
	while i < jumps.size:
		area = 1
		max = ydiff[np.nonzero(x2 == jumps[i])[0][0]]
		maxi = i
		while i + area < jumps.size - 1 and jumps[i + area] == x[np.nonzero(x == jumps[i])[0][0] + area]:
			if ydiff[np.nonzero(x2 == jumps[i + area])[0][0]] > max:
				max = ydiff[np.nonzero(x2 == jumps[i + area])[0][0]]
				maxi = i + area
			area += 1
		maxjumps = np.append(maxjumps, jumps[maxi])
		i += area + 1
	print('Maximal points exceeding threshold {}: {}'.format(round(t, 5), maxjumps))
	with open(sys.argv[3], "a") as file:
		file.write('Maximal points exceeding threshold {}: {}\n'.format(round(t, 5), maxjumps))
	return maxjumps

# plot with threshold values marked
fig, ax = plt.subplots(2)
ori, = ax[1].plot(x, y, 'o-', color='g') # plot original points
cs, = ax[1].plot(xi, poly(xi), color='c') # plot cubic spline
ax[1].plot(x2, y2, 'o', color = 'c') # plot smoothed curve
plt.xlabel("(Raw - OB) / OB")
plt.ylabel("Wavelength (Angs)")
plt.title("Neutron Imaging Graph")
ws = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
plt.legend([ws, ori, cs], ("window size: " + str(window * 2), "original data", "cubic spline"), loc='best')
maxjumps = calcjumps(threshold)
for i in range(0, maxjumps.size): # mark x-values of points exceeding threshold
	ax[1].axvline(x=maxjumps[i], color='r')
plt.subplots_adjust(bottom = 0.2)
ax[0].set_position([0.12, 0.05, 0.70, 0.03])
ax[1].set_position([0.12, 0.2, 0.70, 0.70])
sthresh = Slider(ax[0], 'Threshold', 0.000, 0.005, valinit = threshold, valfmt='%1.5f')

# update x-values when threshold slider changes
def update(val):
	threshold = sthresh.val
	maxjumps = calcjumps(threshold)
	fig.canvas.draw_idle()
	while len(ax[1].lines) > 3:
		ax[1].lines[-1].remove()
	for i in range(0, maxjumps.size):
		ax[1].axvline(x=maxjumps[i], color='r')
sthresh.on_changed(update)

plt.show()
