"""
d15

Day 15 of Advent of Code

Author: Aaron Berk <aberk@math.ubc.ca>
Copyright © 2020, Aaron Berk, all rights reserved.
Created: 16 May 2020

"""
import numpy as np
from collections import deque
import pdb
from util import read

the_map = read("15")


class Node:
    def __init__(self, r, c, s, nr=None, nc=None):
        """
        A node in a plus-shaped graph

        Parameters
        ----------
        r : int

        c : int

        s : char

        """
        self.r = r
        self.c = c
        self.loc = (r, c)
        self.s = s
        self.nr = nr
        self.nc = nc
        self.valid_neighbour_idx = self.get_valid_neighbour_idx()
        self.neighbours = []
        self.occupant = None

    def __repr__(self):
        return f"Node({self.r}, {self.c}, {self.s})"

    def get_valid_neighbour_idx(self):
        potential_neighbour_idx = [
            (self.r - 1, self.c),
            (self.r, self.c - 1),
            (self.r, self.c + 1),
            (self.r + 1, self.c),
        ]
        valid_neighbour_idx = []
        for coord in potential_neighbour_idx:
            if (coord[0] < 0) or (coord[1] < 0):
                continue
            if isinstance(self.nr, np.int) and (coord[0] >= self.nr):
                continue
            if isinstance(self.nc, np.int) and (coord[1] >= self.nc):
                continue
            valid_neighbour_idx.append(coord)
        return valid_neighbour_idx

    def add_neighbour(self, node):
        self.neighbours.append(node)
        return

    def near_enemy(self, state):
        """
        near_enemy(self, state)

        Check if self is near an enemy of some other node's `state`.

        Parameters
        ----------
        self: Node
            Graph node.
        state: str
            Should be either G or E, else raise.

        Returns
        -------
        out : bool
            True or False. If state is G then returns True if node neighbours E,
            False otherwise. If state is E then returns True if node neighbours
            G, False otherwise.
        """
        assert (
            len(self.neighbours) > 0
        ), f"Unexpected lack of neighbours. Did you initialize correctly?"

        if state not in ["G", "E"]:
            raise TypeError(
                f"Unexpected node state. state should be G or E but got {state}."
            )

        enemy_state = {"G": "E", "E": "G"}[state]
        for neighbour in self.neighbours:
            if neighbour.s == enemy_state:
                return True
        return False


def _is_non_key_value(v0, parents):
    return v0.loc in set(
        loc for loc in parents.values() if loc not in parents.keys()
    )


def get_path_from_parents(v0, v1, parents):
    # assert _is_non_key_value(
    #     v0, parents
    # ), f"Expected v0 to be in values but not keys."
    path = [v1.loc]
    while path[-1] != v0.loc:
        path.append(parents[path[-1]])
    return path


class PlusGraph:
    def __init__(self, states):
        self.nc = len(states[0])
        self.nr = len(states)

        self.nodes = {
            (r, c): Node(r, c, s, self.nr, self.nc)
            for r, row in enumerate(states)
            for c, s in enumerate(row)
        }

        for loc, node in self.nodes.items():
            for pair in node.valid_neighbour_idx:
                node.add_neighbour(self.nodes[pair])

    def bfs(self, n1):
        """
        bfs(self, n1)

        Parameters
        ----------
        self: PlusGraph
            A graph with "plus-wise" connections
        n1: Node
            Input node

        Returns
        -------
        v : Node
        distance : int
        path : list of tuples
        """
        # pdb.set_trace()
        if n1.s not in ["G", "E"]:
            raise ValueError(f"Unexpected node state for {n1}")
        discovered = {loc: False for loc in self.nodes.keys()}
        valid = {loc: (node.s == ".") for loc, node in self.nodes.items()}
        parents = {}
        Q = deque()
        discovered[n1.loc] = True
        distance = {n1.loc: 0}
        Q.append(n1)
        while len(Q) > 0:
            # pdb.set_trace()
            v = Q.pop()
            if v.near_enemy(n1.s):
                path = get_path_from_parents(n1, v, parents)
                path = path[::-1]
                return v, distance[v.loc], path
            for loc in v.valid_neighbour_idx[::-1]:
                if valid[loc] and not discovered[loc]:
                    discovered[loc] = True
                    parents[loc] = v.loc
                    distance[loc] = distance[v.loc] + 1
                    Q.append(self.nodes[loc])
            Q = sorted(
                Q, key=lambda x: (distance[x.loc], x.r, x.c), reverse=True
            )
        return (n1, 0, [n1.loc])

    def get_occupied_nodes(self):
        return {
            loc: node
            for loc, node in self.nodes.items()
            if node.s in ["G", "E"]
        }

    def __getitem__(self, idx):
        return self.nodes[idx]

    def __iter__(self):
        for node in self.nodes.values():
            yield node

    def __repr__(self):

        string = [
            "".join([self.nodes[(r, c)].s for c in range(self.nc)])
            for r in range(self.nr)
        ]
        string = "\n".join(string)
        return string


class Creature:
    ENEMY = {"G": "E", "E": "G"}

    def __init__(self, node, starting_hp, strength):
        assert node.s in ["G", "E"], f"Invalid node for Creature."
        self.node = None
        self.race = node.s
        self.set_node(node)
        self.hp = starting_hp
        self.strength = strength
        self.alive = self.hp > 0

        assert self.race in [
            "G",
            "E",
        ], f"Expected race to be one of G or E but got {race}"

        self.target_node = None
        self.dist_to_target_node = None
        self.path = None

    def __repr__(self):
        if self.race == "G":
            race = "Gnome"
        elif self.race == "E":
            race = "Elf"
        return f"{race}({self.r}, {self.c}, {self.hp})"

    def attack(self, enemy):
        if enemy.race == self.race:
            print("in here...")
            print(enemy)
            print(self)
            raise ValueError(
                f"Whoops, friendly fire for {self.race} at ({self.r}, {self.c})!"
            )
        enemy.take_damage(self.strength)

    def set_node(self, node: Node):
        self.node = node
        self.node.occupant = self
        self.r = node.r
        self.c = node.c
        self.loc = node.loc
        node.s = self.race

    def take_damage(self, damage):
        self.hp -= damage
        self.alive = self.hp > 0
        if not self.alive:
            self.node.s = "."
            self.node.occupant = None
            self.node = None
        return

    def near_enemy(self):
        enemy = self.ENEMY[self.race]
        return any(neighbour.s == enemy for neighbour in self.node.neighbours)

    def _is_enemy(self, creature):
        return self.race != creature.race

    def _has_enemy(self, node):
        enemy_race = self.ENEMY[self.race]
        return (node.s in self.ENEMY) and (node.occupant.race == enemy_race)

    def find_neighbouring_enemy(self):
        neighbouring_enemies = [
            node for node in self.node.neighbours if self._has_enemy(node)
        ]
        if len(neighbouring_enemies) == 0:
            return None
        if len(neighbouring_enemies) == 1:
            return neighbouring_enemies[0].occupant
        neighbouring_enemies = sorted(
            neighbouring_enemies,
            key=lambda node: (node.occupant.hp, node.r, node.c),
        )
        return neighbouring_enemies[0].occupant

    def attack_phase(self):
        # pdb.set_trace()
        neighbouring_enemy = self.find_neighbouring_enemy()
        if neighbouring_enemy is not None:
            self.attack(neighbouring_enemy)
        return

    def plan_path(self, pg: PlusGraph):
        if self.near_enemy():
            self.target_node = self.node
            self.dist_to_target_node = 0
            self.path = [self.node.loc]
        else:
            nearest_node, distance, path = pg.bfs(self.node)
            self.target_node = nearest_node
            self.dist_to_target_node = distance
            self.path = path
        return

    def move(self, pg: PlusGraph):
        # pdb.set_trace()
        if len(self.path) == 1:
            assert self.path[0] == (self.r, self.c)
            return
        new_r, new_c = self.path[1]
        self.node.s = "."
        self.set_node(pg[new_r, new_c])
        return


example_maps = {
    1: [
        "#########",
        "#G..G..G#",
        "#.......#",
        "#.......#",
        "#G..E..G#",
        "#.......#",
        "#.......#",
        "#G..G..G#",
        "#########",
    ],
    2: [
        "#######",
        "#.G...#",
        "#...EG#",
        "#.#.#G#",
        "#..G#E#",
        "#.....#",
        "#######",
    ],
    3: [
        "#######",
        "#G..#E#",
        "#E#E.E#",
        "#G.##.#",
        "#...#E#",
        "#...E.#",
        "#######",
    ],
    4: [
        "#######",
        "#E..EG#",
        "#.#G.E#",
        "#E.##E#",
        "#G..#.#",
        "#..E#.#",
        "#######",
    ],
}


def still_battling(creatures):
    """
    still_battling(creatures)

    Check if the race war is ongoing (i.e., if all living creatures are of one race).
    """
    return any(creatures[0].race != creature.race for creature in creatures[1:])


def do_battle(elf_attack_power=3):
    """
    do_battle()

    Warning: ctr might be one low. So if the outcome is not correct with
      outcome = ctr * total_remaining_hp,
    then try adding one:
      outcome = (ctr+1) * total_remaining_hp.
    """
    pg = PlusGraph(the_map)

    starting_number_of_elves = 0
    creatures = []
    for loc, node in pg.get_occupied_nodes().items():
        if node.s == "E":
            attack_power = elf_attack_power
            starting_number_of_elves += 1
        else:
            attack_power = 3
        creatures.append(Creature(node, 200, attack_power))

    ctr = 0
    while True:
        creatures = sorted(creatures, key=lambda x: (x.r, x.c))
        # print(f"Time {ctr}")
        # pdb.set_trace()
        for c in creatures:
            if not c.alive:
                continue
            c.plan_path(pg)
            c.move(pg)
            c.attack_phase()
        creatures = [c for c in creatures if c.alive]
        # print(pg)
        # for c in creatures:
        #     print(c)
        if not still_battling(creatures):
            total_remaining_hp = sum(c.hp for c in creatures)
            outcome = total_remaining_hp * ctr
            break
        ctr += 1

    ending_number_of_elves = sum(1 for c in creatures if c.race == "E")

    return (
        starting_number_of_elves,
        ending_number_of_elves,
        ctr,
        total_remaining_hp,
        outcome,
    )


print("Part 1")
starting_no, ending_no, ctr, total_remaining_hp, outcome = do_battle(3)
print(f"{ctr} * {total_remaining_hp} = {outcome}")


print("\nPart 2")
a, b, c = 3, 21, 40

while True:
    output = do_battle(b)
    starting_no, ending_no, ctr, total_remaining_hp, outcome = output
    if ending_no == starting_no:
        output = do_battle(b - 1)
        if output[0] != output[1]:
            print(f"Elf attack power: {b}")
            print(f"{ctr} * {total_remaining_hp} = {outcome}")
            break
        c = b - 1
        b = (a + b - 1) // 2
    else:
        a = b
        b = (b + c) // 2


# # d15.py ends here
