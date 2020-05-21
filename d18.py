"""
d18

Day 18 of AoC '18

Author: Aaron Berk <aberk@math.ubc.ca>
Copyright © 2020, Aaron Berk, all rights reserved.
Created: 20 May 2020
"""
# import cProfile
import matplotlib.pyplot as plt

from util import read

puzzle_input = read("18")
example_input = [
    ".#.#...|#.",
    ".....#|##|",
    ".|..|...#.",
    "..|#.....#",
    "#.#|||#|#|",
    "...#.||...",
    ".|....|...",
    "||...#|.#|",
    "|.||||..|.",
    "...#.|..|.",
]


def surrounding_acre_indices(r, c):
    return [
        (r - 1, c - 1),
        (r - 1, c),
        (r - 1, c + 1),
        (r, c - 1),
        (r, c + 1),
        (r + 1, c - 1),
        (r + 1, c),
        (r + 1, c + 1),
    ]


class Acreage:
    def __init__(self, Map):
        self.Map = Map
        self.nr = len(Map)
        self.nc = len(Map[0])
        self.minute = 0
        self.trv = [self.total_resource_value()]

    def __getitem__(self, idx):
        r, c = idx
        return self.Map[r][c]

    def update_step(self):
        new_map = [
            "".join([self.process_element(r, c) for c in range(self.nc)])
            for r in range(self.nr)
        ]
        self.minute += 1
        self.Map = new_map
        self.trv.append(self.total_resource_value())

    def process_element(self, r, c):
        state = self[r, c]
        neighbour_states = [
            self[idx] for idx in self.get_valid_neighbour_idx(r, c)
        ]
        if state == ".":
            new_state = self._process_open(neighbour_states)
        elif state == "|":
            new_state = self._process_tree(neighbour_states)
        elif state == "#":
            new_state = self._process_lumberyard(neighbour_states)
        else:
            raise ValueError(f"Unexpected character {state} at ({r}, {c}).")
        return new_state

    def _process_open(self, neighbour_states):
        tree_count = sum(1 for state in neighbour_states if state == "|")
        if tree_count >= 3:
            new_state = "|"
        else:
            new_state = "."
        return new_state

    def _process_tree(self, neighbour_states):
        lumberyard_count = sum(1 for state in neighbour_states if state == "#")
        if lumberyard_count >= 3:
            new_state = "#"
        else:
            new_state = "|"
        return new_state

    def _process_lumberyard(self, neighbour_states):
        lumberyard_count = sum(1 for state in neighbour_states if state == "#")
        tree_count = sum(1 for state in neighbour_states if state == "|")
        if (lumberyard_count >= 1) and (tree_count >= 1):
            new_state = "#"
        else:
            new_state = "."
        return new_state

    def get_valid_neighbour_idx(self, r, c):
        valid_neighbour_idx = [
            idx
            for idx in surrounding_acre_indices(r, c)
            if not (
                (idx[0] < 0)
                or (idx[1] < 0)
                or (idx[0] >= self.nr)
                or (idx[1] >= self.nc)
            )
        ]
        return valid_neighbour_idx

    def __repr__(self):
        output = f"Time: {self.minute}\n"
        output = output + "\n".join(self.Map)
        return output

    def total_resource_value(self):
        concat_map = "".join(self.Map)
        trv = concat_map.count("|") * concat_map.count("#")
        return trv

    def part_one(self):
        for _ in range(10):
            acreage.update_step()
        p1_answer = self.trv[10]
        return p1_answer

    def part_two_a(self):
        """
        This doesn't solve part 2. It just runs the process for long enough that
        it stabilizes. The rest of part 2 happens below.
        """
        self.stable_after = 600
        while True:
            self.update_step()
            if self.minute == 636:  # can't know this a priori
                print(self)
            elif self.minute == (self.stable_after + 50):
                return
        return

    def part_two_b(self):
        p2_input = 1000000000  # minutes
        stable_after = self.stable_after  # minutes
        x = range(stable_after, len(self.trv))
        y = self.trv[stable_after:]
        ymin = min(y)
        x_argmin = [xx for xx, yy in zip(x, y) if yy == ymin]
        period = x_argmin[1] - x_argmin[0]
        mod_minute = (p2_input - x_argmin[0]) % period + x_argmin[0]
        p2_answer = self.trv[mod_minute]
        return p2_answer

    def part_two(self):
        self.part_two_a()
        return self.part_two_b()


acreage = Acreage(puzzle_input)
print(acreage)
print("Part 1:", acreage.part_one())  # 539682
print("Part 2:", acreage.part_two())  # 226450

# # d18.py ends here
