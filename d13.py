from util import read
import numpy as np
from collections import defaultdict, deque

day = '13'
print(f'Day {day}')
print('------')
lines = read(day)

def mapParser(s):
    if s in '<>':
        return '-'
    elif s in '^v':
        return '|'
    else:
        return s

the_map = [''.join([mapParser(s) for s in ell]) for ell in lines]

class Cart:
    m = the_map
    def __init__(self, name, x, y, d):
        self.name = name
        self.x = x
        self.y = y
        self.t = 0 # mod 3 for Left, Straight, Right
        self.d = d # direction
    def getNbhd(self):
        m = self.m
        y0 = np.maximum(self.y-1, 0)
        y1 = np.minimum(self.y+1, len(m)-1)
        x0 = np.maximum(self.x-1, 0)
        x1 = np.minimum(self.x+1, len(m[0]) - 1)
        nbhd = [m[y][x0:x1+1] for y in range(y0, y1+1)]
        if x0 == self.x:
            nbhd = [' ' + c for c in nbhd]
        elif x1 == self.x:
            nbhd = [c + ' ' for c in nbhd]
        if y0 == self.y:
            nbhd = [' '*3, *nbhd]
        elif y1 == self.y:
            nbhd = [*nbhd, ' '*3]
        return nbhd
    def showNbhd(self):
        print(f'({self.x}, {self.y})')
        for r in self.getNbhd():
            print(r)
        return
    def move(self):
        if self.d == '<':
            if self.m[self.y][self.x] == '+':
                if self.t == 0:
                    self.y += 1
                    self.d = 'v'
                elif self.t == 1:
                    self.x -= 1
                else:
                    self.y -= 1
                    self.d = '^'
                self.t = ((self.t + 1) % 3)
            else:
                self.x -= 1
        elif self.d == '>':
            if self.m[self.y][self.x] == '+':
                if self.t == 0:
                    self.y -= 1
                    self.d = '^'
                elif self.t == 1:
                    self.x += 1
                else:
                    self.y += 1
                    self.d = 'v'
                self.t = ((self.t + 1) % 3)
            else:
                self.x += 1
        elif self.d == 'v':
            if self.m[self.y][self.x] == '+':
                if self.t == 0:
                    self.x += 1
                    self.d = '>'
                elif self.t == 1:
                    self.y += 1
                else:
                    self.x -= 1
                    self.d = '<'
                self.t = ((self.t + 1) % 3)
            else:
                self.y += 1
        elif self.d == '^':
            if self.m[self.y][self.x] == '+':
                if self.t == 0:
                    self.x -= 1
                    self.d = '<'
                elif self.t == 1:
                    self.y -= 1
                else:
                    self.x += 1
                    self.d = '>'
                self.t = ((self.t + 1) % 3)
            else:
                self.y -= 1
        else:
            raise ValueError(
                f'unexpected direction for cart at {self.x}, {self.y}')
        return
    def rotate(self):
        if self.m[self.y][self.x] == '/':
            if self.d == '<':
                self.d = 'v'
            elif self.d == '>':
                self.d = '^'
            elif self.d == '^':
                self.d = '>'
            elif self.d == 'v':
                self.d = '<'
            else:
                raise ValueError('direction not recognized')
        elif self.m[self.y][self.x] == '\\':
            if self.d == '<':
                self.d = '^'
            elif self.d == '>':
                self.d = 'v'
            elif self.d == '^':
                self.d = '<'
            elif self.d == 'v':
                self.d = '>'
            else:
                raise ValueError('direction not recognized')
        else:
            return
        return
    def checkCollision(self, cart_list, return_which=False):
        for i, c in enumerate(cart_list):
            if c.name == self.name:
                continue
            elif (c.x == self.x) and (c.y == self.y):
                if not return_which:
                    print(
                        f'Carts {self.name},{c.name} collide at {self.x},{self.y}.')
                    return True
                else:
                    return (self.name, c.name)
        return False
    def update(self, cart_list, return_which=False):
        self.move()
        self.rotate()
        return self.checkCollision(cart_list, return_which)
    def __le__(self, value):
        if self.y < value.y:
            return True
        elif (self.y == value.y) and (self.x <= value.x):
            return True
        else:
            return False
        return False
    def __lt__(self, value):
        if self.y < value.y:
            return True
        elif (self.y == value.y) and (self.x < value.x):
            return True
        else:
            return False
        return False
    def __ge__(self, value):
        if self.y > value.y:
            return True
        elif (self.y == value.y) and (self.x >= value.x):
            return True
        else:
            return False
        return False
    def __gt__(self, value):
        if self.y > value.y:
            return True
        elif (self.y == value.y) and (self.x > value.x):
            return True
        else:
            return False
        return False
    

def drawMap(the_map, carts):
    m = [r for r in the_map]
    for c in carts:
        m[c.y] = m[c.y][:c.x] + c.d + m[c.y][c.x+1:]
    print()
    print('~'*50)
    print()
    for r in m:
        print(r)
            

carts = []

cart_counter = 0 
for y, row in enumerate(lines):
    for x, s in enumerate(row):
        if s in '<>v^':
            carts.append(Cart(cart_counter, x, y, s))
            cart_counter += 1

def solve_a(carts):
    n_rounds = 0
    collided = False
    while not collided:
        n_rounds += 1
        carts = sorted(carts)
        for c in carts:
            collided = c.update(carts)
            if collided:
                print(f'Done after {n_rounds}.')
                break
        
        for c in carts:
            print(f'{c.name}, {c.x},{c.y}')
        print()
    print('Part 1:', n_rounds)
    return

#solve_a(carts)

def removeCollided(carts, collision_info):
    if isinstance(collision_info, tuple):
        return [c for c in carts if c.name not in collision_info]
    return carts
        

def solve_b(carts):
    n_rounds = 0
    many = True
    while many:
        n_rounds += 1
        carts = sorted(carts)
        for i in range(len(carts)):
            if i >= len(carts):
                break
            c = carts[i]
            collided = c.update(carts, return_which=True)
            carts = removeCollided(carts, collided)
            if len(carts) == 1:
                many = False
                print(f'Done after {n_rounds}.')
                break
        
        for c in carts:
            print(f'{c.name}, {c.x},{c.y}')
        print()
    print('Part 2:', n_rounds)
    return

solve_b(carts)


# wrong answers for part 2: (84,77)
