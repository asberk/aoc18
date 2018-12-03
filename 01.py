from util import read
import numpy as np

x = read('01')
x = [int(a) for a in x]

print('Day 01')
print('------')
print('Part 1:', np.sum(x))

print()
print('Part 2:', end='')

test1 = [1, -1]
test2 = [3,3,4,-2,-4]
test3 = [-6, +3, +8, +5, -6]
test4 = [+7, +7, -2, -7, -4]
#x = test4

FLAG = False
g = {}
a = 0
idx = 0
while True:
    if a in g:
        g[a] += 1
        print(a)
        break
    else:
        g[a] = 1
    a += x[np.mod(idx, len(x)).astype(int)]
    idx += 1

