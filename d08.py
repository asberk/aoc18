from util import read
import numpy as np

day = '08'
print(f'Day {day}')
print('------')

x = read(day)
x = [int(y) for y in x[0].split(' ')]

def parse(data):
    nc, nm = data[:2]
    data = data[2:]
    totals = 0
    values = []

    for i in range(nc):
        total, value, data = parse(data)
        totals += total
        values.append(value)

    totals += sum(data[:nm])

    if nc == 0:
        print(nc, nm, len(data))
        return (totals, totals, data[nm:])
    else:
        value = sum([values[j-1] for j in data[:nm]
                     if j > 0 and j <= len(values)])
        return (totals, value, data[nm:])

total, value, remaining = parse(x)
print("Part 1:", total)
print("Part 2:", value)
