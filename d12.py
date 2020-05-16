from util import read
import numpy as np
from collections import defaultdict, deque

day = '12'
print(f'Day {day}')
print('------')
x = read(day)

x0 = x[0].split(': ')[1]
x = x[2:]

def getRulePair(s):
    return s.split(' => ')

rp = [getRulePair(s) for s in x]
rp = {k: v for k,v in rp}

g = [x0]

def parse(s):
    if '*' in s:
        raise Exception('unknown character')
    assert len(s) == 5, f'weird length {len(s)}'
    return rp.get(s, '*')

for i in range(20):
    gg = '.'*5 + g[-1] + '.'*5
    new = ''
    for j, l in enumerate(gg[2:-2], 2):
        new += parse(gg[j-2:j+3])
    g.append(new)

v = np.arange(-3*20, -3*20 + len(g[-1]))
p1 = np.sum([v[j] for j, gg in enumerate(g[-1]) if gg == '#'])
print("Part 1:", p1)


def valueAtGeneration(n):
    v = np.arange(-3*n, -3*n + len(g[n]))
    return np.sum([v[j] for j, gg in enumerate(g[n]) if gg == '#'])


for i in range(20, 2000):
    gg = '.'*5 + g[-1] + '.'*5
    new = ''
    for j, l in enumerate(gg[2:-2], 2):
        new += parse(gg[j-2:j+3])
    g.append(new)
    if i > 100:
        v0, v1 = valueAtGeneration(i),   valueAtGeneration(i-1)
        v2, v3 = valueAtGeneration(i-2), valueAtGeneration(i-3)
        v4, v5 = valueAtGeneration(i-4), valueAtGeneration(i-5)
        d1, d2, d3, d4, d5 = v0 - v1, v1 - v2, v2 - v3, v3 - v4, v4 - v5
        hasCGrowth = (d1 == d2) and (d2 == d3) and (d3 == d4) and (d4 == d5)
        if hasCGrowth:
            break

n_gen = len(g) - 1
vv = valueAtGeneration(n_gen)

print('Part 2:', d5*(50000000000 - n_gen) + vv)
