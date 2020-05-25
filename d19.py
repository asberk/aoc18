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

    while (max_iters is None) or (n_iters <= max_iters):
        inst_no = registers[instruction_pointer]
        if (inst_no < 0) or (inst_no >= program_length):
            print(f"num iters: {n_iters}")
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
    print("final_state:", final_registers)
    print(f"Part_1: {p1_answer}")
    return


def part_two(max_iters=None):
    instruction_pointer, program = parse_input(puzzle_input)
    registers = [1] + [0] * 5
    initial_state = run_program(
        instruction_pointer, program, registers, max_iters=49,
    )
    C = initial_state[2]
    initial_state[3] = 9
    initial_state[5] = C + 1

    r0, r1, r2, ip, r4, r5 = initial_state
    while True:
        if (r2 % r1) == 0:
            r0 += r1
        r1 += 1
        if r1 > r2:
            ip = 13
            r4 = 1
            break
    intermediate_state = [r0, r1, r2, ip, r4, r5]
    final_state = run_program(
        instruction_pointer, program, intermediate_state, max_iters=max_iters
    )
    print("final_state:", final_state)
    print(f"Part_2: {final_state[0]}")
    return


if __name__ == "__main__":
    part_one()
    part_two(100)


# # d19.py ends here
