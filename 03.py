from util import read
import numpy as np
day = '03'
x = read(day)
#x = [int(a) for a in x]

print(f'Day {day}')
print('------')
print('Part 1: ', end='', flush=True)

test = ['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']
# x = test

class Claim:
    def __init__(self, s):
        ID, s = s.split('#')[1].split(' @ ')
        self.ID = int(ID)
        x1, s = s.split(',')
        y1, s = s.split(': ')
        dx, dy = s.split('x')
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.dx, self.dy = int(dx), int(dy)
        self.x2, self.y2 = self.x1 + self.dx -1, self.y1 + self.dy -1

    def area(self):
        return self.dx * self.dy

    def has_overlap(self, claim):
        qx1 = (self.x1 <= claim.x1) and (self.x2 >= claim.x1)
        rx1 = (claim.x1 <= self.x1) and (claim.x2 >= self.x1)
        qy1 = (self.y1 <= claim.y1) and (self.y2 >= claim.y1)
        ry1 = (claim.y1 <= self.y1) and (claim.y2 >= self.y1)
        return (qx1 and qy1) or (rx1 and ry1) or (qx1 and ry1) or (rx1 and qy1)

    def get_overlap_area(self, claim):
        max_x1 = np.maximum(self.x1, claim.x1)
        min_x2 = np.minimum(self.x2, claim.x2)
        max_y1 = np.maximum(self.y1, claim.y1)
        min_y2 = np.minimum(self.y2, claim.y2)
        return (min_x2 - max_x1 + 1) * (min_y2 - max_y1 + 1)
        
claims = [Claim(s) for s in x]

overlaps = {}
for i, p in enumerate(claims):
    for j, q in enumerate(claims[i+1:]):
        if p.has_overlap(q):
            overlaps[(i, j)] = p.get_overlap_area(q)

p1 = np.sum([v for v in overlaps.values()])
print(p1)

wrong_answers = [176468, 191479, ]

print('\nPart 2: ', end='', flush=True)

test = None
# x = test

p2 = None
print(p2)
