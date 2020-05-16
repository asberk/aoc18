"""
d13p2

Day 13 Part 2

Author: Aaron Berk <aberk@math.ubc.ca>
Copyright © 2020, Aaron Berk, all rights reserved.
Created: 15 May 2020

"""
import numpy as np
import pandas as pd
from heapq import heappush
import matplotlib.pyplot as plt
from time import sleep
import util

d13_input = util.read("13")
map_chars = np.unique(list("".join(d13_input)))
nws_map_chars = [x for x in map_chars if x != " "]
cart_chars = ["<", ">", "^", "v"]


check_plain_map_status = False


def get_valid_region():
    valid_region = np.zeros((len(d13_input), len(d13_input[0])))
    for i, row in enumerate(d13_input):
        for j, elem in enumerate(row):
            if elem in nws_map_chars:
                valid_region[i, j] = 1
    return valid_region


def plot_valid_region():
    """
    Plots a binary matrix of the valid regions of the map.

    Returns
    -------
    fig
    ax
    map_im
    """
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    map_im = ax.imshow(get_valid_region())
    ax.axis("off")
    return fig, ax, map_im


def convert_input_to_array():
    arr_map = np.array([list(x) for x in d13_input]).copy()
    return arr_map


def get_initial_cart_positions():
    arr_map = convert_input_to_array()
    init_pos_r, init_pos_c = np.where(np.isin(arr_map, cart_chars))
    return init_pos_r, init_pos_c


def get_initial_cart_states():
    arr_map = convert_input_to_array()
    init_pos_r, init_pos_c = np.where(np.isin(arr_map, cart_chars))
    cart_directions = np.array(
        [arr_map[r, c] for r, c in zip(init_pos_r, init_pos_c)]
    )
    return init_pos_r, init_pos_c, cart_directions


def print_map_stats():
    print(pd.value_counts(list("".join(d13_input))))


def get_nbhd(arr_map, pr, pc):
    return arr_map[pr - 1 : pr + 2, pc - 1 : pc + 2]


def find_track_type(elem):
    if elem in "<>":
        return "-"
    if elem in "^v":
        return "|"
    raise ValueError("find_track_type: Unexpected character")


def get_plain_map():
    plain_map = convert_input_to_array()
    positions = get_initial_cart_positions()
    for r, c in zip(*positions):
        plain_map[r, c] = find_track_type(plain_map[r, c])
    return plain_map


class Cart:
    VALID_CART_CHARS = ["<", ">", "^", "v"]
    DIRECTIONS = ["left", "straight", "right"]
    TURNS = {
        ">": {"left": "^", "straight": ">", "right": "v"},
        "<": {"left": "v", "straight": "<", "right": "^"},
        "^": {"left": "<", "straight": "^", "right": ">"},
        "v": {"left": ">", "straight": "v", "right": "<"},
    }
    MAP = get_plain_map()
    VALID_REGION = get_valid_region()

    def __init__(self, pr, pc, char):
        self.pr = pr
        self.pc = pc
        self.char = char
        self.alive = True
        self.t = 0  # number of turns

    def show_cart_locale(self, rad=3):
        locale = self.MAP[
            self.pr - rad : self.pr + rad + 1, self.pc - rad : self.pc + rad + 1
        ].copy()
        locale[rad, rad] = self.char
        print(locale)
        return

    def read_terrain(self):
        return self.MAP[self.pr, self.pc]

    def update_cart(self):
        # adjust cart direction if necessary
        self.turn_cart()
        # move cart
        self.move_cart()
        # check new position is valid
        self._is_on_map()
        return

    def turn_cart(self):
        if self._at_ur_dl_corner():
            if self.char == "^":
                self.char = ">"
            elif self.char == ">":
                self.char = "^"
            elif self.char == "<":
                self.char = "v"
            elif self.char == "v":
                self.char = "<"
            else:
                raise
        elif self._at_ul_dr_corner():
            if self.char == "^":
                self.char = "<"
            elif self.char == "<":
                self.char = "^"
            elif self.char == ">":
                self.char = "v"
            elif self.char == "v":
                self.char = ">"
            else:
                raise
        elif self._at_intersection():
            self.char = self.TURNS[self.char][self.DIRECTIONS[self.t]]
            self._update_t()
        return

    def move_cart(self):
        if self.char == "<":
            self.pc -= 1
        elif self.char == ">":
            self.pc += 1
        elif self.char == "v":
            self.pr += 1
        elif self.char == "^":
            self.pr -= 1
        else:
            raise
        return

    def has_crashed(self, boolean):
        self.alive = not boolean
        return

    def _has_valid_char(self):
        if self.char is not None:
            assert self.char in self.VALID_CART_CHARS
        return

    def _at_corner(self):
        return self.read_terrain() in "/\\"

    def _at_ur_dl_corner(self):
        return self.read_terrain() == "/"

    def _at_ul_dr_corner(self):
        return self.read_terrain() == "\\"

    def _at_intersection(self):
        return self.read_terrain() == "+"

    def _update_t(self):
        self.t = (self.t + 1) % 3

    def _is_on_map(self):
        if not self.VALID_REGION[self.pr, self.pc] == 1:
            new_map = get_plain_map()
            new_map[self.pr, self.pc] = self.char
            print("Cart off map:")
            print(get_nbhd(new_map, self.pr, self.pc))
            raise
        return

    def __le__(self, other):
        if self.pr < other.pr:
            return True
        elif self.pr > other.pr:
            return False
        elif self.pc <= other.pc:
            # Only enter this part if carts in same row
            return True
        else:
            return False

    def __ge__(self, other):
        if self.pr > other.pr:
            return True
        elif self.pr < other.pr:
            return False
        elif self.pc >= other.pc:
            # Only enter this part if carts in same row
            return True
        else:
            return False

    def __eq__(self, other):
        return (self <= other) and (self >= other)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (self <= other) and (self != other)

    def __gt__(self, other):
        return (self >= other) and (self != other)

    def __repr__(self):
        return f"Cart({self.pr}, {self.pc}, {self.char})"


def draw_map(valid_region, cartlist, ctr, fig, ax):
    for r, c in [(cart.pr, cart.pc) for cart in cartlist if cart.alive]:
        valid_region[r, c] = 2
    ax.imshow(valid_region, cmap="viridis")
    plt.tight_layout()
    fig.savefig(f"fig/output{ctr:05d}.png")
    return


class Track:
    def __init__(self, cart_list):
        self.cart_list = []
        for cart in cart_list:
            heappush(self.cart_list, cart)
        self.counter = 0
        self.more_than_one = len(self.cart_list) > 1

    def check_for_collision(self, cart):
        for i, other in enumerate(self.cart_list):
            if (
                (cart == other)
                and (not (id(cart) == id(other)))
                and other.alive
            ):
                cart.has_crashed(True)
                other.has_crashed(True)
                break
        self.cart_list = [cart for cart in self.cart_list if cart.alive]
        return

    def run(self, do_draw_map=False):
        if do_draw_map:
            fig, ax = plt.subplots(1, 1, figsize=(10, 10))
            vr = get_valid_region()
            ax.imshow(vr)
            ax.axis("off")
        while len(self.cart_list) > 1:
            if do_draw_map:
                vr[vr > 1] = 1
                draw_map(vr, self.cart_list, self.counter, fig=fig, ax=ax)
            self.counter += 1
            self.cart_list = sorted(
                [cart for cart in self.cart_list if cart.alive]
            )
            for ci, cart in enumerate(self.cart_list):
                if not cart.alive:
                    continue
                cart.update_cart()
                self.check_for_collision(cart)
                if not cart.alive:
                    continue
        if len(self.cart_list) == 0:
            print(
                "Warning: there were an even number of carts and they all died"
            )
        final_cart = self.cart_list[0]
        print("Found final cart:")
        print(final_cart)
        print(f"Answer: {final_cart.pc},{final_cart.pr}")
        print(f"Counter: {self.counter}")
        return

    def __repr__(self):
        return "\n".join([cart.__repr__() for cart in self.cart_list])


arr_map = convert_input_to_array()
init_pos_r, init_pos_c, init_dir = get_initial_cart_states()
plain_map = get_plain_map()

cart_list = [Cart(r, c, d) for r, c, d in zip(*get_initial_cart_states())]
track = Track(cart_list)

if check_plain_map_status:
    for i, (pr, pc) in enumerate(zip(init_pos_r, init_pos_c)):
        print(f"Cart {i}")
        print(arr_map[pr - 1 : pr + 2, pc - 1 : pc + 2])
        print(plain_map[pr - 1 : pr + 2, pc - 1 : pc + 2])


track.run(True)

# # d13p2.py ends here
