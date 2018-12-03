from util import read
import numpy as np

x = read('02')
#x = [int(a) for a in x]

print('Day 02')
print('------')
print('Part 1:', end='', flush=True)

def countDict(s):
    g = {}
    for a in s:
        if a in g:
            g[a] += 1
        else:
            g[a] = 1
    return g

def filterReps(g, n):
    return {k: v for k, v in g.items() if v == n}

def countHasReps(v, n):
    d = [filterReps(countDict(s), n) for s in v]
    d = [1 if len(a) > 0 else 0 for a in d]
    return np.sum(d)

def dupsAndTrips(s):
    g = countDict(s)
    dups = filterReps(g, 2)
    trips = filterReps(g, 3)
    if (len(dups) > 0) and (len(trips) > 0):
        return 1
    else:
        return 0

test = ['abcdef', 'bababc', 'abbcde', 'abcccd', 'aabcdd', 'abcdee', 'ababab']
#x = test
    
p1 = countHasReps(x, 2) * countHasReps(x, 3)
print(p1)

print()
print('Part 2:', end='', flush=True)

test = ['abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxyz']
# x = test

def difference(b1, b2):
    common = ''
    for j, k in zip(b1, b2):
        if j == k:
            common += j
    if len(b1) - len(common) == 1:
        return common
    else:
        return None

goods = [difference(p, q)
         for i,p in enumerate(x) for q in x[(i+1):]]
goods = [p for p in goods if p is not None]
print(goods[0])
