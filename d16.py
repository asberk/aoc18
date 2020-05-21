"""
d16

Day 16 of AoC '18

Author: Aaron Berk <aberk@math.ubc.ca>
Copyright © 2020, Aaron Berk, all rights reserved.
Created: 17 May 2020

"""
from time import time
import pandas as pd
import numpy as np
from util import read


def create_address_validator(register_max=4):
    def _valid_register_address(*args):
        for x in args:
            assert x >= 0, f"Unknown register address {x}."
            assert x < register_max, f"Unknown register address {x}."
        return

    return _valid_register_address


class Instruction:
    def __init__(self, op, regA=True, regB=True, op_name=None, register_max=4):
        self.op = op
        if regA == "r":
            regA = True
        elif regA == "i":
            regA = False
        if regB == "r":
            regB = True
        elif regB == "i":
            regB = False
        self.regA = regA
        self.regB = regB
        self.op_name = op_name
        self._validate_address = create_address_validator(register_max)

    def __call__(self, registers, A, B, C):
        if self.regA and self.regB:
            self._validate_address(A, B, C)
            registers[C] = self.op(registers[A], registers[B])
        elif self.regA:
            self._validate_address(A, C)
            registers[C] = self.op(registers[A], B)
        elif self.regB:
            self._validate_address(B, C)
            registers[C] = self.op(A, registers[B])
        else:
            registers[C] = self.op(A, B)
        return registers

    def __repr__(self):
        riA = "r" if self.regA else "i"
        riB = "r" if self.regB else "i"
        if self.op_name is not None:
            return f"Instruction({self.op_name}, {riA}, {riB})"
        return f"Instruction({riA}, {riB})"


op_dict = {
    "add": lambda x, y: x + y,
    "mul": lambda x, y: x * y,
    "ban": lambda x, y: x & y,
    "bor": lambda x, y: x | y,
    "set": lambda x, y: x,
    "gt": lambda x, y: 1 if x > y else 0,
    "eq": lambda x, y: 1 if x == y else 0,
}


def create_instructions(register_max=4):

    instructions = {
        k1
        + k2: Instruction(
            op_dict[k1],
            regA=True,
            regB=k2 == "r",
            op_name=k1,
            register_max=register_max,
        )
        for k1 in ["add", "mul", "ban", "bor"]
        for k2 in ["r", "i"]
    }

    for regA in ["r", "i"]:
        for regB in ["r", "i"]:
            if (regA == "i") and (regB == "i"):
                continue
            for k1 in ["gt", "eq"]:
                instructions[k1 + regA + regB] = Instruction(
                    op_dict[k1],
                    regA=regA == "r",
                    regB=regB == "r",
                    op_name=k1,
                    register_max=register_max,
                )

    for regA in ["r", "i"]:
        instructions["set" + regA] = Instruction(
            op_dict["set"],
            regA=regA == "r",
            regB=False,
            op_name="set",
            register_max=register_max,
        )
    return instructions


def parse_line(line):
    """
    parse_line(line)

    Examples:
    parse_line("Before: [2, 1, 2, 2]")
    parse_line("15 1 2 3")
    parse_line("After:  [2, 1, 2, 0]")

    Returns
    -------
    result : list
        A list of the numbers in the line.
    """
    string = "".join([x for x in line if x.isdigit() or x == " "])
    result = [int(x) for x in string.split()]
    return result


def parse_bunch(bunch):
    start_register = bunch[0]
    instructions = bunch[1]
    final_register = bunch[2]

    assert "Before" in start_register, f"Unexpected bunch {bunch}"
    assert "After" in final_register, f"Unexpected bunch {bunch}"
    start_register = parse_line(start_register)
    instructions = parse_line(instructions)
    final_register = parse_line(final_register)
    return start_register, instructions, final_register


def try_instruction_on_bunch(inst: Instruction, bunch):
    reg_init, inst_line, reg_final = parse_bunch(bunch)
    reg_out = inst(reg_init, *inst_line[1:])
    if reg_out == reg_final:
        return True
    return False


def get_opcode_from_bunch(bunch):
    return int(bunch[1].split()[0])


def part_one(puzzle_input, instructions, op_codes, bunches):
    t0 = time()

    results = []
    results_counter = []

    for i, bunch in enumerate(bunches):
        results_counter.append(0)
        results.append([])
        for j, (inst_name, inst) in enumerate(instructions.items()):
            if try_instruction_on_bunch(inst, bunch):
                results_counter[-1] += 1
                results[-1].append(inst_name)

    p1_ans = sum(1 for x in results_counter if x >= 3)
    t1 = time()
    print("Part 1")
    print(p1_ans)
    print(f"Duration: {t1 - t0:.3f} sec")
    return results, results_counter


def check_column(col):
    if (col > 0).sum() == 1:
        val = col.loc[col > 0]
        return (val.index[0], val.name)
    return False


def go_through_columns(dframe):
    for j in range(dframe.shape[1]):
        col = dframe.iloc[:, j]
        pair = check_column(col)
        if pair is False:
            continue
        return pair, dframe.drop(index=pair[0], columns=pair[1])
    return None, dframe


def get_pairings(op_codes, instructions, results, results_counter):
    num_samples = len(op_codes)
    inst_names = list(instructions.keys())
    inst_idx = {key: i for i, key in enumerate(inst_names)}
    num_features = len(inst_names)

    sparse_matrix = np.zeros((num_samples, num_features))
    for i, result in enumerate(results):
        for inst_name in result:
            sparse_matrix[i, inst_idx[inst_name]] = 1

    df = pd.DataFrame(sparse_matrix, columns=inst_names)
    df["opcode"] = op_codes

    op_code_means = df.groupby(["opcode"]).sum()

    pairings = list(
        set(
            (opc, res[0])
            for opc, rc, res in zip(op_codes, results_counter, results)
            if rc == 1
        )
    )

    for pair in pairings:
        op_code_means = op_code_means.drop(index=pair[0], columns=pair[1])

    while op_code_means.shape[0] > 0:
        new_pair, op_code_means = go_through_columns(op_code_means)
        if new_pair is not None:
            pairings.append(new_pair)

    pairings = dict(sorted(pairings, key=lambda x: x[0]))
    return pairings


def part_two(puzzle_input, instructions, op_codes, results, results_counter):
    t2 = time()
    pairings = get_pairings(op_codes, instructions, results, results_counter)
    # print(pairings)
    p2_input = puzzle_input[3094:]

    registers = [0] * 4
    for line in p2_input:
        parsed_line = parse_line(line)
        inst = instructions[pairings[parsed_line[0]]]
        registers = inst(registers, *parsed_line[1:])
    t3 = time()

    print("\nPart 2")
    print(registers[0])
    print(f"Duration: {t3 - t2:.3f} sec")
    return


def main():

    instructions = create_instructions()
    puzzle_input = read("16")
    bunches = [puzzle_input[4 * k : 4 * (k + 1) - 1] for k in range(773)]
    op_codes = [get_opcode_from_bunch(bunch) for bunch in bunches]

    results, results_counter = part_one(
        puzzle_input, instructions, op_codes, bunches
    )
    part_two(puzzle_input, instructions, op_codes, results, results_counter)
    return


if __name__ == "__main__":
    main()


# # d16.py ends here
