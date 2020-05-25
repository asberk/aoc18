"""
d20

Day 20 of AoC '18

Author: Aaron Berk <aberk@math.ubc.ca>
Copyright © 2020, Aaron Berk, all rights reserved.
Created: 23 May 2020

Commentary:
   
"""
import re
from util import read

puzzle_input = read("20")

example_1 = "^ENWWW(NEEE|SSE(EE|N))$"
example_2 = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"


class Node:
    def __init__(self, value=None, parents=None, children=None, l=None, r=None):
        self.value = value
        self.parents = parents
        self.children = children
        self.l = None
        self.r = None
        self.level = None

    def add_parents(self, parents):
        if not isinstance(parents, (tuple, list)):
            parents = [parents]
        if self.parents is None:
            self.parents = parents
            return
        for parent in parents:
            self.parents.append(parent)
        return

    def is_leaf_node(self):
        return (self.children is None) or (len(self.children) == 0)

    def is_root(self):
        return self.value == "^"

    def is_tail(self):
        return self.value == "$"

    def get_level(self):
        return self.level

    def set_level(self):
        """
        Level isn't a great name in this set-up, but could help us solve part one.
        """
        if self.is_root():
            self.level = 0
        assert self.parents is not None, f"Only root node has no parents."
        self.level = min(parent.level for parent in self.parents)


class Graph:
    def __init__(self, root=None):
        self.root = root


def find_branches(string):
    string_iter = re.finditer(r"(\^|[NESW]+|\(|\)|\||\$)", string)
    node_dict = {}
    node_stack = []
    par_stack = []
    pipe_stack = []
    ctr = 0
    for i, c in enumerate(string_iter):
        if c[0] == "^":
            continue
        elif c[0] == "$":
            return
        elif c[0] == "(":
            par_stack.append(i)

        elif c[0] == "|":
            pipe_stack.append(i)
        elif c[0] == ")":
            if len(par_stack) == 0:
                raise RuntimeError(
                    f"Missing (: unmatched right paren at index {i}"
                )
            elif len(pipe_stack) == 0:
                raise RuntimeError(
                    f"Missing |: unmatched right paren at index {i}"
                )
            pipe_idx = pipe_stack.pop()
            # left_node = Node(
            left_branches[ctr] = (par_stack.pop(), pipe_idx)
            right_branches[ctr] = (pipe_idx, i)
            ctr += 1
        else:
            l, r = c.span()

            Node(c[0], l=l, r=r)

    if len(par_stack) > 0:
        print(f"Warning: unmatched left paren(s): {par_stack}")
    elif len(pipe_stack) > 0:
        print(f"Warning: unmatched pipe(s): {pipe_stack}")
    return left_branches, right_branches


string_iter = re.finditer(r"(\^|[NESW]+|\(|\)|\||\$)", example_2)
l_branch, r_branch = find_branches(example_1)
idx = 0

level = 0
for i, item in enumerate(string_iter):
    if item == "^":
        paren_tree


# # d20.py ends here
