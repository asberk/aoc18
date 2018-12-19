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

#def getMaxPowerSize(c, S, w=3):
    
    

# Part 2
sizes = range(1, 301)
powers = []
for j, w in enumerate(sizes):
    powers.append(getMaxPower(w))
    # sort of arbitrary
    if (j > 25) and (powers[j][0] < powers[j-1][0]):
        break
powers = np.array(powers)
print(powers[np.argmax(powers[:, 0])])
