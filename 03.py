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
        self.x2, self.y2 = self.x1 + self.dx - 1, self.y1 + self.dy - 1

    def area(self):
        return self.dx * self.dy

    def has_overlap(self, claim):
        qx = (self.x1 <= claim.x1) and (self.x2 >= claim.x1)
        rx = (claim.x1 <= self.x1) and (claim.x2 >= self.x1)
        qy = (self.y1 <= claim.y1) and (self.y2 >= claim.y1)
        ry = (claim.y1 <= self.y1) and (claim.y2 >= self.y1)
        return (qx and qy) or (rx and ry) or (qx and ry) or (rx and qy)

    def get_overlap_area(self, claim):
        if not self.has_overlap(claim):
            return 0
        max_x1 = np.maximum(self.x1, claim.x1)
        min_x2 = np.minimum(self.x2, claim.x2)
        max_y1 = np.maximum(self.y1, claim.y1)
        min_y2 = np.minimum(self.y2, claim.y2)
        return (min_x2 - max_x1 + 1) * (min_y2 - max_y1 + 1)
        
claims = [Claim(s) for s in x]

arr = np.zeros((1000, 1000))

for i, c in enumerate(claims):
    for xi in range(c.x1, c.x2 + 1):
        for yi in range(c.y1, c.y2 + 1):
            arr[xi, yi] += 1
p1 = (arr > 1).sum()
print(p1)

print('\nPart 2: ', end='', flush=True)

possibles = []
olap_mat = np.zeros((len(claims), len(claims)))
for i, p in enumerate(claims):
    for j, q in enumerate(claims[i+1:], i+1):
        olap_mat[i,j] = p.has_overlap(q)
        olap_mat[j,i] = olap_mat[i,j]
    if not olap_mat[i].any():
        possibles.append(p.ID)
        
if len(possibles) == 1:
    p2 = possibles[0]
    print(p2)
else:
    print(possibles)
    print('something went very wrong')
