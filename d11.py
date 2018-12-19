from util import read
import numpy as np
from collections import defaultdict, deque, Counter

day = '11'
print(f'Day {day}')
print('------')
x = 5153 # grid serial number
grid_serial_no = 5153

c = np.zeros((300, 300))



def computePowerLevel(i,j):
    """
    0 <= j,i <= 299
    1 <= x,y <= 300
    """
    x, y = j + 1, i + 1
    rackID = x + 10
    power_level = rackID * y
    power_level += grid_serial_no
    power_level *= rackID
    power_level = int((power_level % 1000) / 100)
    power_level -= 5
    return power_level


c = np.array([[computePowerLevel(i,j) for j in range(300)]
              for i in range(300)])

def sum_convolve(m, w=1):
    o = np.zeros((m.shape[0]-w+1, m.shape[1]-w+1))
    for i in range(o.shape[0]):
        for j in range(o.shape[1]):
            o[i,j] = m[i:i+w, j:j+w].sum()
    return o

def getMaxPower(w):
    if w < 1:
        raise ValueError('Require w >= 1')
    elif w == 1:
        cc = c
    else:
        cc = sum_convolve(c, w)
    cc_max = cc.max()
    i, j = np.where(cc == cc_max)
    return [cc_max, j[0]+1, i[0] + 1, w]
    
# Part 1
print(getMaxPower(3))


def summedAreaTable(c):
    sat = np.array([[c[:i, :j].sum() for j in range(c.shape[1])]
                    for i in range(c.shape[0])])
    return sat

def computeArea(S, i, j, w):
    if (i == 0) and (j == 0):
        return S[w-1, w-1]
    elif i == 0:
        return S[i+w-1, j+w-1] - S[i+w-1, j-1]
    elif j == 0:
        return S[i+w-1, j+w-1] - S[i-1, j+w-1]
    else:
        return S[i+w-1, j+w-1] + S[i-1, j-1] - S[i+w-1, j-1] - S[i-1, j+w-1]
    return

def getMaxPowerSize(c, S=None, w=3):
    if S is None:
        S = summedAreaTable(c)
    all_powers = [[computeArea(S, i, j, w)
                   for j in range(S.shape[1]-w+1)]
                  for i in range(S.shape[0]-w+1)]
    all_powers = np.array(all_powers)
    all_powers_max = all_powers.max()
    i_max, j_max = np.where(all_powers == all_powers_max)
    return [all_powers_max, j_max[0] + 1, i_max[0]+1, w]

S = summedAreaTable(c)
P = np.array([getMaxPowerSize(c, S, w) for w in range(1, 301)])
print('summed area table:', P[np.argmax(P[:, 0])])

# Part 2
sizes = range(1, 301)
powers = []
for j, w in enumerate(sizes):
    powers.append(getMaxPower(w))
    # sort of arbitrary
    if (j > 25) and (powers[j][0] < powers[j-1][0]):
        break
powers = np.array(powers)
print('arbitrary cut-off', powers[np.argmax(powers[:, 0])])


