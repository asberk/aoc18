"""
d19

Day 19 of AoC '18

Author: Aaron Berk <aberk@math.ubc.ca>
Copyright © 2020, Aaron Berk, all rights reserved.
Created: 20 May 2020
"""
import pdb
import matplotlib.pyplot as plt
from util import read
from d16 import create_instructions

puzzle_input = read("19")
instructions = create_instructions(register_max=6)


def parse_input_line(line):
    line = line.split()
    for i in range(1, len(line)):
        line[i] = int(line[i])
    return line


def parse_input(program):
    instruction_pointer = int(program[0].split()[-1])
    program = [parse_input_line(line) for line in program[1:]]
    return instruction_pointer, program


def invalid_instruction_pointer(instruction_pointer, program_length, registers):
    if registers[instruction_pointer] < 0:
        return True
    if registers[instruction_pointer] >= program_length:
        return True
    return False


def run_program(
    instruction_pointer,
    program,
    registers=None,
    track_register_history=None,
    max_iters=None,
):
    if registers is None:
        registers = [0] * 6

    program_length = len(program)
    n_iters = 0

    if track_register_history is not None:
        register_history = []
        history = []

    while (n_iters is None) or (n_iters <= max_iters):
        inst_no = registers[instruction_pointer]
        if (inst_no < 0) or (inst_no >= program_length):
            print(f"n_iters: {n_iters}")
            if track_register_history is not None:
                return registers, register_history, history
            return registers
        if track_register_history is not None:
            register_history.append(tuple(registers))
            history.append(", ".join(str(x) for x in registers))
            history.append(" ".join(str(x) for x in program[inst_no]))
        op_name, A, B, C = program[inst_no]
        registers = instructions[op_name](registers, A, B, C)
        if track_register_history is not None:
            register_history.append(tuple(registers))
            history.append(", ".join(str(x) for x in registers))
        registers[instruction_pointer] += 1
        n_iters += 1
    print("Max iterations exceeded.")
    if track_register_history is not None:
        return registers, register_history, history
    return registers


def part_one():
    instruction_pointer, program = parse_input(puzzle_input)
    final_registers = run_program(instruction_pointer, program)
    p1_answer = final_registers[0]
    print("final_register:", final_registers)
    print(f"Part 1: {p1_answer}")
    return


def part_two(max_iters=None):
    instruction_pointer, program = parse_input(puzzle_input)
    registers = [1] + [0] * 5
    final_registers, register_history, history = run_program(
        instruction_pointer,
        program,
        registers,
        track_register_history=True,
        max_iters=50,
    )

    # Option 2
    registers = [0, 1, 10551282, 9, 0, 10551282 + 1]
    final_registers, register_history, history = run_program(
        instruction_pointer,
        program,
        registers,
        track_register_history=False,
        max_iters=max_iters,
    )
    print(f"Part 2: {final_registers[instruction_pointer]}")
    return register_history, history, instruction_pointer, program


if __name__ == "__main__":
    # part_one()
    register_history, history, instruction_pointer, program = part_two(100000)
    treg_hist = tuple(zip(*register_history))

    fig, ax = plt.subplots(2, 3, figsize=(15, 6), sharex=True)
    ax = ax.ravel()
    for i, entry in enumerate(treg_hist):
        ax[i].plot(entry[:200])
        ax[i].set_title(f"{i}")
        ax[i].set_ylim(-1, min(1000, max(entry[:200])))
    plt.show(fig)
    plt.close(fig)

    subset = [
        reg_entries
        for reg_entries, val in zip(register_history, treg_hist[4])
        if val != 0
    ]
    tsubset = tuple(zip(*subset))

    fig, ax = plt.subplots(2, 3, figsize=(15, 6), sharex=True)
    ax = ax.ravel()
    for i, entry in enumerate(tsubset):
        ax[i].plot(entry[35:1000])
        ax[i].set_title(f"{i}")
        ax[i].set_ylim(-1, min(1000, max(entry[35:1000])))
    plt.show(fig)
    plt.close(fig)
    del fig, ax

    len(program)

# # d19.py ends here
