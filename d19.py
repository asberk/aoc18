"""
d19

Day 19 of AoC '18

Author: Aaron Berk <aberk@math.ubc.ca>
Copyright © 2020, Aaron Berk, all rights reserved.
Created: 20 May 2020
"""
import pdb
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


def run_program(instruction_pointer, program, registers=None):
    if registers is None:
        registers = [0] * 6

    program_length = len(program)
    n_iters = 0

    while True:
        inst_no = registers[instruction_pointer]
        if (inst_no < 0) or (inst_no >= program_length):
            print(f"n_iters: {n_iters}")
            return registers
        op_name, A, B, C = program[inst_no]
        registers = instructions[op_name](registers, A, B, C)
        registers[instruction_pointer] += 1
        n_iters += 1


def part_one():
    instruction_pointer, program = parse_input(puzzle_input)
    final_registers = run_program(instruction_pointer, program)
    p1_answer = final_registers[0]
    print("final_register:", final_registers)
    print(f"Part 1: {p1_answer}")
    return


def part_two():
    instruction_pointer, program = parse_input(puzzle_input)
    registers = [1] + [0] * 5
    p2_answer = run_program(instruction_pointer, program, registers)
    print(f"Part 2: {p2_answer}")
    return


if __name__ == "__main__":
    part_one()
    # part_two()

# # d19.py ends here
