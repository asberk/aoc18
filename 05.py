from util import read
import numpy as np
from collections import deque

day = '05'
print(f'Day {day}')
print('------')
x = read(day)[0]


def checkTypePolarity(a,b):
    sameType = (a.lower() == b.lower())
    oppositePolarity = (a != b)
    return (sameType and oppositePolarity)

def collapse(s):
    i = 0
    while True:
        # we'll handle very short strings manually
        if len(s) == 2:
            return s
        # the main deal
        a = s[i]
        b = s[i+1]
        if checkTypePolarity(a,b):
            s = s[:i] + s[(i+2):]
            i -= 1
        else:
            i += 1
        # edge case conditions
        if i+1 >= len(s):
            break
        elif i < 0:
            i = 0
    return s


collapsed = collapse(x)
p1 = len(collapsed)
print("Part 1: ", p1)

def removeAndReact(s, a):
    a = a.lower()
    s2 = s.replace(a, '').replace(a.upper(), '')
    c = collapse(s2)
    return len(c)

min_length = len(x)
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
for a in ascii_lowercase:
    length = removeAndReact(x, a)
    if length < min_length:
        min_length = np.copy(length)

p2 = int(min_length)
print("Part 2: ", p2)
