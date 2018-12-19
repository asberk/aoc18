from util import read
import numpy as np
from collections import defaultdict, deque
import matplotlib.pyplot as plt

from scipy.optimize import minimize_scalar

day = '10'
print(f'Day {day}')
print('------')
x = read(day)


test = ['position=< 9,  1> velocity=< 0,  2>', 
        'position=< 7,  0> velocity=<-1,  0>',
        'position=< 3, -2> velocity=<-1,  1>',
        'position=< 6, 10> velocity=<-2, -1>',
        'position=< 2, -4> velocity=< 2,  2>',
        'position=<-6, 10> velocity=< 2, -2>',
        'position=< 1,  8> velocity=< 1, -1>',
        'position=< 1,  7> velocity=< 1,  0>',
        'position=<-3, 11> velocity=< 1, -2>',
        'position=< 7,  6> velocity=<-1, -1>',
        'position=<-2,  3> velocity=< 1,  0>',
        'position=<-4,  3> velocity=< 2,  0>',
        'position=<10, -3> velocity=<-1,  1>',
        'position=< 5, 11> velocity=< 1, -2>',
        'position=< 4,  7> velocity=< 0, -1>',
        'position=< 8, -2> velocity=< 0,  1>',
        'position=<15,  0> velocity=<-2,  0>',
        'position=< 1,  6> velocity=< 1,  0>',
        'position=< 8,  9> velocity=< 0, -1>',
        'position=< 3,  3> velocity=<-1,  1>',
        'position=< 0,  5> velocity=< 0, -1>',
        'position=<-2,  2> velocity=< 2,  0>',
        'position=< 5, -2> velocity=< 1,  2>',
        'position=< 1,  4> velocity=< 2,  1>',
        'position=<-2,  7> velocity=< 2, -2>',
        'position=< 3,  6> velocity=<-1, -1>',
        'position=< 5,  0> velocity=< 1,  0>',
        'position=<-6,  0> velocity=< 2,  0>',
        'position=< 5,  9> velocity=< 1, -2>',
        'position=<14,  7> velocity=<-2,  0>',
        'position=<-3,  6> velocity=< 2, -1>']

def parsePoint(s):
    try:
        p, v = ''.join([ss for ss in s if ss in '-0123456789,>']).split('>')[:2]
    except:
        print(s)
        raise
    px, py = p.split(',')
    vx, vy = v.split(',')
    px, py = int(px), int(py)
    vx, vy = int(vx), int(vy)
    return (px, py, vx, vy)


class Point:

    def __init__(self, px, py, vx, vy):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy

    def move(self, t=1):
        self.px += t * self.vx
        self.py += t * self.vy


def move(pts, t=1):
    for p in pts:
        p.move(t)
    return 

def maxes(pts):
    xs, ys = [p.px for p in pts], [p.py for p in pts]
    return np.max(xs), np.max(ys)

def getStat(pts, fun):
    xs, ys = [p.px for p in pts], [p.py for p in pts]
    return fun(xs), fun(ys)

def draw_grid(points):
    max_x, max_y = maxes(points)
    G = np.zeros((max_y + 1, max_x+1))
    for p in points:
        if p.py >= 0 and p.px >= 0:
            G[p.py, p.px] = 1
    return G

# j = 0
# G = draw_grid(points)
# old_shape = G.shape[0] + 10

# while True:
#     old_shape = G.shape[0]
#     G = draw_grid(points)
#     if G.shape[0] <= 256:
#         break
#     elif G.shape[0] > old_shape:
#         print(j, G.shape)
#         break
#     else:
#         move(points)
#         j += 1

# print('========')
# print(j, G.shape)


points = np.array([list(parsePoint(s)) for s in x])
def optFun(t):
    thing = np.var(points[:, :2] + t * points[:, -2:], axis=0)
    assert thing.size == 2
    thing = (thing ** 2).sum()
    return thing


result = minimize_scalar(optFun)
if result.success:
    t_star = result.x
else:
    raise Exception("Not success")

points = [Point(*parsePoint(s)) for s in x]
move(points, int(t_star))

G = draw_grid(points)
plt.matshow(G)
plt.show()

p1 = 'RGRKHKNA'
p2 = t_star
print('Part 1:', p1)
print('Part 2:', int(p2))
