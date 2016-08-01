import numpy as np
# generate smoothed curve based on window


def generate_smooth_curve(x, y, window):
    x2 = x
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
        
    return {'x2': x2, 'y2': y2}