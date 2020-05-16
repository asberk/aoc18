from time import time

t0 = time()

puzzle_input = "110201"

score = "37"
elf1 = 0
elf2 = 1
while puzzle_input not in score[-7:]:
    score += str(int(score[elf1]) + int(score[elf2]))
    elf1 = (elf1 + int(score[elf1]) + 1) % len(score)
    elf2 = (elf2 + int(score[elf2]) + 1) % len(score)

print("Part 1:", score[int(puzzle_input) : int(puzzle_input) + 10])
print("Part 2:", score.index(puzzle_input))
t1 = time()
print(f"Total time: {t1 - t0:.1f} sec")
