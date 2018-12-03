def read(day):
    with open(f'inputs/{day}.txt') as fp:
        return [x[:-1] for x in fp.readlines()]
