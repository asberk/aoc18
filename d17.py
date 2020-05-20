"""
d17

Day 17 of AoC '18

Author: Aaron Berk <aberk@math.ubc.ca>
Copyright © 2020, Aaron Berk, all rights reserved.
Created: 17 May 2020

"""
import pdb
from typing import Tuple
from collections import deque
import numpy as np
import matplotlib.pyplot as plt

from util import read


puzzle_input = read("17")

example_input = [
    "x=495, y=2..7",
    "y=7, x=495..501",
    "x=501, y=3..7",
    "x=498, y=2..4",
    "x=506, y=1..2",
    "x=498, y=10..13",
    "x=504, y=10..13",
    "y=13, x=498..504",
]


def parse_line(line):
    coord1, coord2 = line.split(", ")
    var1, num1 = coord1.split("=")
    var2, num2 = coord2.split("=")

    num1 = [int(a) for a in num1.split("..")]
    num2 = [int(a) for a in num2.split("..")]

    return {var1: num1, var2: num2}


def get_map_bounds(lines):
    # ymin, ymax, xmin, xmax = None, None, None, None
    yx = [
        (min(line["y"]), max(line["y"]), min(line["x"]), max(line["x"]))
        for line in lines
    ]
    ymin, ymax, xmin, xmax = zip(*yx)

    ymin, ymax, xmin, xmax = min(ymin), max(ymax), min(xmin), max(xmax)

    return ymin, ymax, xmin, xmax + 1


def build_map(lines):
    map_bounds = get_map_bounds(lines)
    row_min, row_max, col_min, col_max = map_bounds

    ground_slice = np.zeros((row_max - row_min + 1, col_max - col_min + 1))

    for line in lines:
        cols = line["x"]
        rows = line["y"]
        if len(cols) == 1:
            cc = cols[0]
            for rr in range(rows[0], rows[1] + 1):
                ground_slice[rr - row_min, cc - col_min] = "1"
        elif len(rows) == 1:
            rr = rows[0]
            for cc in range(cols[0], cols[1] + 1):
                ground_slice[rr - row_min, cc - col_min] = "1"
        else:
            raise ValueError("Something went wrong...")
    return ground_slice, map_bounds


def view_map(
    input_image,
    map_bounds,
    row_min=None,
    row_max=None,
    filename=None,
    figsize=(4, 8),
):
    rmin, rmax, cmin, cmax = map_bounds
    if row_min is None:
        row_min = 0
    if row_max is None:
        row_max = input_image.shape[0]

    fig, ax = plt.subplots(1, 1, figsize=figsize)

    img_array = input_image[row_min:row_max, :]
    ax.imshow(img_array)

    xticks = [xx - cmin for xx in range(cmin, cmax + 1) if (xx % 5) == 0]
    yticks = [yy for yy in range(img_array.shape[0]) if (yy % 5) == 0]
    xticklabels = [f"{xx+cmin}" for xx in xticks]
    yticklabels = [f"{yy+rmin+row_min}" for yy in yticks]

    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xticklabels(xticklabels, size=8, rotation=90)
    ax.set_yticklabels(yticklabels, size=8)
    plt.tight_layout()
    if isinstance(filename, str):
        print("Saving figure")
        fig.savefig(filename)
    else:
        plt.show(fig)
    del fig, ax
    return


class Cell:
    SAND = 0
    CLAY = 1
    FALLING = 0.75
    STILL = 0.5
    VALID_STATES = [SAND, CLAY, FALLING, STILL]

    def __init__(self, r, c, s, map_bounds=None):
        """
        __init__(self, r, c, s)

        Parameters
        ----------
        r : int
            Row position.
        c : int
            Col position
        s : float
            State: 0 for sand, 1 for clay, 0.75 for falling water, 0.5 for still
            water.
        """
        self.r = r
        self.c = c
        self.loc = (r, c)
        self.row_min, self.row_max, self.col_min, self.col_max = map_bounds

        self.neighbours = {"N": None, "E": None, "S": None, "W": None}

        self.s = s
        assert self.s in self.VALID_STATES

        self.valid_neighbour_idx = self.get_valid_neighbour_idx()
        self.bounded = {
            "N": False,
            "E": False,
            "S": False,
            "W": False,
        }

    def __repr__(self):
        return f"Cell({self.r}, {self.c}, {self.s})"

    def is_falling(self):
        return self.s == self.FALLING

    def is_still(self):
        return self.s == self.STILL

    def is_clay(self):
        return self.s == self.CLAY

    def is_sand(self):
        return self.s == self.SAND

    def is_water(self):
        return self.s in [self.FALLING, self.STILL]

    def is_ground(self):
        return not self.is_water()

    def set_falling(self):
        self.s = self.FALLING
        return

    def set_still(self):
        self.s = self.STILL
        n_nbr = self.neighbours["N"]
        if n_nbr is not None:
            n_nbr.detect_bounded()
        return

    def _fall_below(self):
        if not self.is_falling():
            return
        s_nbr = self.neighbours["S"]
        if (s_nbr is None) or not s_nbr.is_sand():
            return
        s_nbr.set_falling()
        return s_nbr

    def _fall_EW(self, input_dirn=None):
        if not self.is_falling():
            return

        out = []
        self.detect_bounded()

        if input_dirn is None:
            directions = ["E", "W"]
        else:
            directions = [input_dirn]

        for dirn in directions:
            nbr = self.neighbours[dirn]
            if nbr is None:
                continue
            nbr.detect_bounded()
            if self.bounded["S"] and (nbr.is_sand() or nbr.is_falling()):
                nbr.set_falling()
                nbr2 = nbr._fall_EW(dirn)
                if len(directions) == 1:
                    return nbr2
                elif isinstance(nbr2, Cell):
                    out.append(nbr2)
            if (input_dirn is not None) and nbr.is_clay():
                return self
            elif (input_dirn is not None) and not self.bounded["S"]:
                return self
            elif nbr.is_clay():
                out.append(self)
            elif nbr.is_sand() and not self.bounded["S"]:
                out.append(self)

        return out

    def _fall_to_still(self):
        if not self.is_falling():
            return
        self.detect_bounded()
        if self.bounded["E"] and self.bounded["W"] and self.bounded["S"]:
            self.set_still()
            return self
        return

    def _still_ew(self):
        if not self.is_still():
            return
        out = []
        for dirn in ["E", "W"]:
            ew_nbr = self.neighbours[dirn]
            if ew_nbr is None:
                continue
            if ew_nbr.is_sand() or ew_nbr.is_falling():
                ew_nbr.set_still()
                out.append(ew_nbr)
        return out

    def detect_bounded(self):
        """
        detect_bounded(self)

        Dot becomes bounded in the following examples:

        bounded below:
        .
        #

        both bounded from left
        #..

        both bounded from left, right and below
        #..#
        ####

        Parameters
        ----------
        self: Cell
        """
        for dirn, neighbour in self.neighbours.items():
            if neighbour is None:
                continue
            if neighbour.is_still() or neighbour.is_clay():
                self.bounded[dirn] = True
            if (dirn in ["E", "W"]) and (neighbour.bounded[dirn]):
                self.bounded[dirn] = True
            if (
                (dirn == "E")
                and (self.bounded[dirn])
                and (self.neighbours["W"] is not None)
            ):
                self.neighbours["W"].bounded[dirn] = True
            if (
                (dirn == "W")
                and (self.bounded[dirn])
                and (self.neighbours["E"] is not None)
            ):
                self.neighbours["E"].bounded[dirn] = True
        return

    def _has_neighbour(self, direction):
        return isinstance(self.neighbours[direction], Cell)

    def _nbr_state(self, direction, state):
        assert direction in ["N", "E", "W", "S"], "Invalid direction"
        return self._has_neighbour(direction) and (
            self.neighbours[direction].s == state
        )

    def add_neighbour(self, cell):
        if (cell.r == self.r - 1) and (cell.c == self.c):
            self.neighbours["N"] = cell
        elif (cell.r == self.r + 1) and (cell.c == self.c):
            self.neighbours["S"] = cell
        elif (cell.r == self.r) and (cell.c == self.c + 1):
            self.neighbours["E"] = cell
        elif (cell.r == self.r) and (cell.c == self.c - 1):
            self.neighbours["W"] = cell
        else:
            raise RuntimeError(f"cell {cell} is not a neighbour of {self}")
        return

    def get_valid_neighbour_idx(self):
        potential_neighbour_idx = [
            (self.r - 1, self.c),  # N
            (self.r, self.c - 1),  # W
            (self.r, self.c + 1),  # E
            (self.r + 1, self.c),  # S
        ]
        valid_neighbour_idx = []
        for coord in potential_neighbour_idx:
            if (coord[0] < 0) or (coord[1] < 0):
                continue
            if isinstance(self.row_max, np.int) and (coord[0] > self.row_max):
                continue
            if isinstance(self.col_max, np.int) and (coord[1] > self.col_max):
                continue
            if isinstance(self.row_min, np.int) and (coord[0] < self.row_min):
                continue
            if isinstance(self.col_min, np.int) and (coord[1] < self.col_min):
                continue
            valid_neighbour_idx.append(coord)
        return valid_neighbour_idx


class WaterFlow:

    CLAY = 1.0
    SAND = 0.0
    FALLING = 0.75
    STILL = 0.5

    def __init__(self, carte: np.ndarray, map_bounds: Tuple, fount_src: Tuple):
        self.carte = carte
        self.fount_src = fount_src
        self.row_min, self.row_max, self.col_min, self.col_max = map_bounds
        assert self.fount_src[1] > self.col_min
        assert self.fount_src[1] < self.col_max

        self.cells = {
            (r, c): Cell(
                r,
                c,
                carte[r - self.row_min, c - self.col_min],
                map_bounds=map_bounds,
            )
            for r in range(self.row_min, self.row_max + 1)
            for c in range(self.col_min, self.col_max + 1)
        }

        for cell in self.cells.values():
            for loc in cell.valid_neighbour_idx:
                cell.add_neighbour(self.cells[loc])

        self.active_cells = None
        self.visited_cells = None

    def __repr__(self):
        return f"WaterFlow()"

    def __getitem__(self, idx):
        return self.cells[idx]

    def save_fig(self, visited_cells, figsize=(6, 14)):
        ground = self.carte.copy()
        for cell in visited_cells:
            ground[cell.r - self.row_min, cell.c - self.col_min] = cell.s
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        ax.imshow(ground)
        ax.axis("off")
        plt.tight_layout()
        fig.savefig(f"./fig/d17/ground_{len(visited_cells)}.png")
        plt.close(fig)
        return

    def ensure_falling_row_bounded(self, ew_nbrs):
        """
        ensure_falling_row_bounded(self, ew_nbrs)

        If ew_nbrs is a list of two Cells, then it denotes the endpoints in a
        row for a group of falling water that's bounded by two pieces of clay.
        This function ensures that all of those cells are recognized as bounded.
        """
        if (ew_nbrs is not None) and (len(ew_nbrs) == 2):
            ew_nbrs = sorted(ew_nbrs, key=lambda x: x.c)
        else:
            return
        out = []
        cell_w, cell_e = ew_nbrs
        # if cell_w.r >= 44:
        #     #pdb.set_trace()
        cell_w.detect_bounded()
        cell_e.detect_bounded()

        if not cell_w.bounded["S"]:
            out.append(cell_w)
        if not cell_e.bounded["S"]:
            out.append(cell_e)
        r = cell_w.r
        c0, c1 = cell_w.c, cell_e.c
        if cell_w.bounded["W"] and cell_w.bounded["S"]:
            for c in range(c0 + 1, c1 + 1):
                ibc = self[r, c]  # in_between_cell
                if not ibc.is_falling():
                    print(
                        f"ensure_falling_row_bounded::Uh oh investigate this: {ibc}"
                    )
                ibc.bounded["W"] = True
                if (not ibc.bounded["S"]) and (ibc not in out):
                    out.append(ibc)
        if cell_e.bounded["E"] and cell_e.bounded["S"]:
            for c in range(c0, c1):
                ibc = self[r, c]  # in_between_cell
                if not ibc.is_falling():
                    print(
                        f"ensure_falling_row_bounded::Uh oh investigate this: {ibc}"
                    )
                ibc.bounded["E"] = True
                if (not ibc.bounded["S"]) and (ibc not in out):
                    out.append(ibc)
        return out

    def set_bounded_falling_to_still(self, ew_nbrs):
        if (ew_nbrs is not None) and (len(ew_nbrs) == 2):
            ew_nbrs = sorted(ew_nbrs, key=lambda x: x.c)
        else:
            return
        out = []
        cell_l, cell_r = ew_nbrs
        r = cell_l.r
        for c in range(cell_l.c, cell_r.c + 1):
            ibc = self[r, c]  # in_between_cell
            if (
                ibc.is_falling()
                and ibc.bounded["S"]
                and ibc.bounded["E"]
                and ibc.bounded["W"]
            ):
                ibc.set_still()
                if ibc._nbr_state("N", self.FALLING):
                    out.append(ibc.neighbours["N"])
        return out

    def update_visited_cells(self, ew_nbrs):
        if ew_nbrs is None:
            return
        if isinstance(ew_nbrs, Cell):
            ew_nbrs = [ew_nbrs]
        if len(ew_nbrs) == 1:
            cell = ew_nbrs[0]
            r, c = cell.r, cell.c
            while (
                ((r, c) in self.cells.keys())
                and (self[r, c] is not None)
                and self[r, c].is_water()
            ):
                self.visited_cells.add(self[r, c])
                c -= 1
            c = cell.c
            while (
                ((r, c) in self.cells.keys())
                and (self[r, c] is not None)
                and self[r, c].is_water()
            ):
                self.visited_cells.add(self[r, c])
                c += 1
        elif len(ew_nbrs) == 2:
            # pdb.set_trace()
            ew_nbrs = sorted(ew_nbrs, key=lambda x: x.c)
            cell_w, cell_e = ew_nbrs
            r = cell_w.r
            c0, c1 = cell_w.c, cell_e.c
            for c in range(c0, c1 + 1):
                self.visited_cells.add(self[r, c])
        else:
            raise RuntimeError(
                f"update_visited_cells::Something went wrong with {ew_nbrs}"
            )
        return

    def update_current_map(self):
        if not hasattr(self, "current_map"):
            self.current_map = self.carte.copy()
        for cell in self.visited_cells:
            self.current_map[
                cell.r - cell.row_min, cell.c - cell.col_min
            ] = cell.s
        return

    def get_visited_cell_bounds(self):
        vcb_rmin, vcb_rmax, vcb_cmin, vcb_cmax = (
            self.row_max,
            self.row_min,
            self.col_max,
            self.col_min,
        )
        for cell in self.visited_cells:
            vcb_rmin = min([vcb_rmin, cell.r])
            vcb_rmax = max([vcb_rmax, cell.r])
            vcb_cmin = min([vcb_cmin, cell.c])
            vcb_cmax = max([vcb_cmax, cell.c])
        return vcb_rmin, vcb_rmax, vcb_cmin, vcb_cmax

    def view_current_map(
        self,
        figsize=(6, 6),
        filename=None,
        row_min=None,
        row_max=None,
        height=None,
    ):
        self.update_current_map()
        cell_bounds = self.get_visited_cell_bounds()
        if row_max is None:
            row_max = min(int(cell_bounds[1] + 2), self.row_max)
        if (row_min is None) and (height is None):
            row_min = 0
        elif row_min is None:
            row_min = max([0, int(row_max - height)])
        view_map(
            self.current_map,
            (self.row_min, self.row_max, self.col_min, self.col_max),
            row_min=row_min,
            row_max=row_max,
            filename=filename,
            figsize=figsize,
        )
        return

    def search_for_remaining_active_cells(self, cell):
        r0, c0 = cell.r, cell.c

        out = []
        while self[r0, c0].is_water():
            n_nbr = self[r0, c0].neighbours["N"]
            if (n_nbr is not None) and n_nbr.is_falling():
                out.append(n_nbr)
                out.append(self[r0, c0])
            if self[r0, c0].is_still() and (
                self[r0, c0]._nbr_state("E", Cell.FALLING)
                or (self[r0, c0]._nbr_state("W", Cell.FALLING))
            ):
                out.append(self[r0, c0])
            c0 += 1

        c0 = cell.c
        while self[r0, c0].is_water():
            n_nbr = self[r0, c0].neighbours["N"]
            if (n_nbr is not None) and n_nbr.is_falling():
                out.append(n_nbr)
                out.append(self[r0, c0])
            c0 -= 1

        return out

    def catch_unsupported_falling_cells(self):
        out = []
        for cell in self.visited_cells:
            if (
                cell.is_falling()
                and not cell.bounded["S"]
                and cell._nbr_state("S", Cell.SAND)
            ):
                out.append(cell)
        return out

    def flow(self, num_steps=None, debug=False):
        if not hasattr(self, "active_cells") or (self.active_cells is None):
            active_cells = deque(
                [cell for cell in self.cells.values() if cell.s == Cell.FALLING]
            )
            self.visited_cells = set(cell for cell in active_cells)
        else:
            active_cells = self.active_cells

        active_cells = set(active_cells)
        ctr = 0
        if debug:
            num_steps = 200
        while (len(active_cells) > 0) and (ctr <= 11000):
            if isinstance(num_steps, np.int) and (ctr >= num_steps):
                break
            ctr += 1
            cell = active_cells.pop()
            self.visited_cells.add(cell)
            if cell.is_clay():
                continue
            if cell.neighbours["S"] is None:
                continue

            s_nbr = cell._fall_below()

            if s_nbr is not None:
                if s_nbr not in active_cells:
                    active_cells.add(s_nbr)
                continue

            ew_nbrs = cell._fall_EW()

            self.update_visited_cells(ew_nbrs)
            unsupported_falling_cells = self.ensure_falling_row_bounded(ew_nbrs)

            if (unsupported_falling_cells is not None) and (
                len(unsupported_falling_cells) > 0
            ):
                for ufc in unsupported_falling_cells:
                    if ufc not in active_cells:
                        active_cells.add(ufc)

            upper_falling_cells = self.set_bounded_falling_to_still(ew_nbrs)

            if (upper_falling_cells is not None) and (
                len(upper_falling_cells) > 0
            ):
                for ufc in upper_falling_cells:
                    if ufc not in active_cells:
                        active_cells.add(ufc)

            other_unsupported_falling_cells = (
                self.catch_unsupported_falling_cells()
            )
            if len(other_unsupported_falling_cells) > 0:
                for oufc in other_unsupported_falling_cells:
                    if oufc not in active_cells:
                        active_cells.add(oufc)

            self.update_current_map()

            if len(active_cells) == 0:
                found_cells = self.search_for_remaining_active_cells(cell)
                for found_cell in found_cells:
                    active_cells.add(found_cell)

            if debug:
                self.save_fig(self.visited_cells)
                input(">")
            elif (ctr % 1000) == 0:
                self.view_current_map(
                    figsize=(12, 12),
                    height=200,
                    filename=f"./fig/d17/main_flow/flow_{ctr}.png",
                )
        self.active_cells = active_cells
        return


def main():

    lines = [parse_line(line) for line in puzzle_input]

    ground_slice, map_bounds = build_map(lines)
    print(ground_slice.shape)
    print(map_bounds)
    col_min = map_bounds[2]

    ground_slice[0, 500 - col_min] = Cell.FALLING

    wf = WaterFlow(ground_slice, map_bounds, (0, 500))

    return wf


if __name__ == "__main__":
    wf = main()

    wf.flow(debug=False)

    wf.update_current_map()
    for rrmm in [i * 100 for i in range(1, 19)] + [1851]:
        wf.view_current_map(
            figsize=(12, 12),
            height=200,
            row_max=rrmm,
            filename=f"./fig/d17/main_flow/final_flow_{rrmm}.png",
        )

    total_water = 0
    amount_of_still_water = 0
    for loc, cell in wf.cells.items():
        if cell.is_water():
            total_water += 1
            if cell.is_still():
                amount_of_still_water += 1
    print("Part 1:", total_water)
    print("Part 2:", amount_of_still_water)


# # d17.py ends here
