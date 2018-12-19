from util import read
import numpy as np
from collections import defaultdict, deque

day = '09'
print(f'Day {day}')
print('------')
x = read(day)

x = x[0].split(' ')
players, points = int(x[0]), int(x[-2])


def play_game(players, points):
    P = defaultdict(int)
    c = deque([0])

    for m in range(1, points + 1):
        if (m % 23) == 0:
            c.rotate(7)
            P[m % players] += m + c.pop()
            c.rotate(-1)
        else:
            c.rotate(-1)
            c.append(m)
    return max(P.values())

p1 = play_game(players, points)
p2 = play_game(players, 100*points)

print("Part 1:", p1)
print("Part 2:", p2)
