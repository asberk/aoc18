from util import read
import numpy as np

day = '07'
print(f'Day {day}')
print('------')

test = ['Step C must be finished before step A can begin.',
        'Step C must be finished before step F can begin.',
        'Step A must be finished before step B can begin.',
        'Step A must be finished before step D can begin.',
        'Step B must be finished before step E can begin.',
        'Step D must be finished before step E can begin.',
        'Step F must be finished before step E can begin.']
x = read(day)
# x = test


def parseStringToKeys(s):
    s = s.split(' ')
    node_name = s[1]
    node_child = s[-3]
    return node_name, node_child

all_keys = np.unique([t for s in x for t in parseStringToKeys(s)])

def constructGraph(x):
    g = {key:
         {'name': key, 'parent': [], 'child': [], 'executed': False}
         for key in all_keys}
    for s in x:
        node_name, node_child = parseStringToKeys(s)
        g[node_name]['child'].append(node_child)
    for node_name, v in g.items():
        for child in v['child']:
            g[child]['parent'].append(node_name)
    for node_name, v in g.items():
        if v['parent'] is None:
            v['executed'] = True
    return g
        

def getRoots(g):
    return [k for k,v in g.items() if len(v['parent']) == 0]


g = constructGraph(x)

def parentsExecuted(node_name):
    parents = g[node_name]['parent']
    if (parents is None) or (len(parents) == 0):
        return True
    return all(g[p]['executed'] for p in parents)

executed = []
active = sorted(getRoots(g))
i = 0

while len(executed) < len(all_keys):
    active_node = g[active[i]]
    if parentsExecuted(active[i]):
        active_node['executed'] = True
        executed.append(active[i])
        active = active[:i] + active[i+1:]
        for child_name in active_node['child']:
            if not (child_name in active):
                active.append(child_name)
        active = sorted(active)
        i = 0
    else:
        i += 1

p1 = ''.join(executed)
print("Part 1:", p1)


def nextValidIdx(active):
    if len(active) == 0:
        return None
    try:
        return next(i for i, a in enumerate(sorted(active))
                    if parentsExecuted(a))
    except:
        return None
    return


class Worker(object):
    def __init__(self, ident):
        self.id = ident
        self.step = ''
        self.time = 0
    def __repr__(self):
        return f'id: {self.id}, step: {self.step}, time: {self.time}'
    def _is_busy(self):
        return len(self.step) > 0
    def _increase_time(self):
        if self._is_busy():
            self.time += 1
        return

def getWaitTime(letter, testing=False):
    wt = ord(letter.upper()) - 4
    if testing:
        wt = wt - 60
    return wt

    
g = constructGraph(x)

n_workers = 5
workers = [Worker(i) for i in range(n_workers)]

executed = []
active = sorted(getRoots(g))
total_time = 0
while len(executed) < len(all_keys):
    print('total_time:', total_time)
    for w in workers:
        print(w)
    print()
    for ell, w in enumerate(workers):
        valid_idx = nextValidIdx(active)
        if (len(w.step) == 0) and (valid_idx is not None):
            w.step = active[valid_idx]
            active = active[:valid_idx] + active[valid_idx+1:]
            w.time += 1
        elif len(w.step) > 0:
            w.time += 1
        if (len(w.step) > 0) and (w.time >= getWaitTime(w.step)):
            executed.append(w.step)
            g[w.step]['executed'] = True
            for child_name in g[w.step]['child']:
                if not (child_name in active) and \
                   not any(child_name in ww.step for ww in workers):
                    active.append(child_name)
            active = sorted(active)
            valid_idx = nextValidIdx(active)
            if valid_idx is not None:
                w.step = active[valid_idx]
                active = active[:valid_idx] + active[valid_idx+1:]
                w.time = 0
            else:
                w.step = ''
                w.time = 0

    total_time += 1

print(total_time)
print(''.join(executed))
#wrong_answers = [966, 967, 968, 972]
