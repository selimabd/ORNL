import numpy as np


def calculate_diff_between_input_and_curve(x, y, x2, poly):
    '''
    calculate diff between input and curve
    '''
    
    globmin = np.where(x == x2[0])[0][0]
    globmax = np.where(x == x2[x2.size - 1])[0][0]
    ydiff = y[globmin:globmax + 1] - poly(x2)
    
    return ydiff


def calculate_jumps(t, ydiff, x2, x):
    '''
    identify max points of regions exceeding threshold
    '''
    
    jumps = np.extract(ydiff > t, x2)
    maxjumps = np.array([])
    i = 0
    while i < jumps.size:
        area = 1
        max = ydiff[np.nonzero(x2 == jumps[i])[0][0]]
        maxi = i
        while ((i + area) < (jumps.size - 1)) and (jumps[i + area] == x[np.nonzero(x == jumps[i])[0][0] + area]):
            if (ydiff[np.nonzero(x2 == jumps[i + area])[0][0]]) > max:
                max = ydiff[np.nonzero(x2 == jumps[i + area])[0][0]]
                maxi = i + area
            area += 1
        maxjumps = np.append(maxjumps, jumps[maxi])
        i += area + 1
    print('Maximal points exceeding threshold {}: {}'.format(round(t, 5), maxjumps))
#    with open(thresholdOutput, "a") as file:
#        file.write('Maximal points exceeding threshold {}: {}\n'.format(round(t, 5), maxjumps))
    return maxjumps