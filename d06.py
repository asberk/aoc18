from util import read
import numpy as np
from collections import Counter
from scipy.spatial.distance import cdist
from time import time
# if making plots:
# import matplotlib.pyplot as plt

day = '06'
print(f'Day {day}')
print('------')
start_time = time()
x = read(day)

def parseLoc(s):
    return [int(ss) for ss in s.split(', ')]

locs = np.array([parseLoc(s) for s in x])
r_locs, c_locs = zip(*locs)
min_r, min_c = np.min(r_locs), np.min(c_locs) - 1
max_r, max_c = np.max(r_locs), np.max(c_locs) + 2
r_grid, c_grid = np.meshgrid(np.arange(min_r,max_r), np.arange(min_c, max_c))
targets = np.dstack((r_grid, c_grid)).reshape(-1, 2)

# rows: locs, cols: targets
distmat = cdist(locs, targets, metric='cityblock')
# >>> distmat.shape == (50, 91188)

# index of closest loc for each target
closest_loc_idx = np.argmin(distmat, axis=0)
# >>> closest_loc_idx.size == 91188

# dist to closest loc for each target
closest_dist = np.min(distmat, axis=0)
# >>> closest_dist.size == 91188

locIdx_grid = closest_loc_idx.reshape(r_grid.shape)
# if it makes it to the edge, it goes all the way:
infinite_box_idxs = np.unique(
    np.concatenate((locIdx_grid[0, :], locIdx_grid[-1, :], 
                    locIdx_grid[:,0], locIdx_grid[:, -1])))

target_on_border = ((distmat == closest_dist.reshape(1,-1)).sum(axis=0) > 1)
# >>> target_on_border.size == 91188

# A little procedural map generation.
# target_is_infinite = np.isin(closest_loc_idx, infinite_box_idxs)
# target_excluded = (target_on_border | target_is_infinite)
# plt.figure(figsize=(7,7))
# plt.imshow(target_excluded.reshape(r_grid.shape))
# plt.axis('off');
# plt.tight_layout()
# plt.savefig('/Users/aberk/code/aoc18/day06_pmg.png', dpi=300);

# exclude the border targets by giving them loc indices that don't exist
closest_loc_idx[target_on_border] = locs.shape[0] + 13

# count the number of times each loc occurs
ctr = Counter(closest_loc_idx)
# filter out the ones that don't belong
dd = {k : v for k,v in ctr.items()
      if (k not in infinite_box_idxs) and (k < locs.shape[0])}
# get largest area from resulting dict.
largest_area = [(tuple(locs[k]), v) for k, v in dd.items()
                if v == max(list(dd.values()))]
# make sure there's only one of them. 
assert len(largest_area) == 1
largest_area = largest_area[0]
loc, area = largest_area
print("Part 1:", area)


# A pictorial solution
# plt.figure(figsize=(10,10))
# plt.scatter(locs[:, 0]-min_r, locs[:, 1]-min_c, marker='.', c='w');
# plt.imshow(closest_loc_idx.reshape(r_grid.shape))
# plt.scatter(loc[0]-min_r, loc[1]-min_c, marker='*', c='w', s=150)

# plt.axis('scaled');
# plt.axis('off');
# plt.tight_layout()
# plt.savefig('/Users/aberk/code/aoc18/day06.png', dpi=300);


p2 = (distmat.sum(axis=0) < 10000).sum()
print("Part 2:", p2)
end_time = time()
print(f'  time: {end_time - start_time:.4f} seconds')
