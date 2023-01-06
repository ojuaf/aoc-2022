#!/usr/bin/env python3


MAXS = [None, None]


def load_input():
    blizzards = []
    borders = set()
    start = None
    end = None
    global MAXS

    with open('input') as fd:
        lines = fd.readlines()
        for y, line in enumerate(lines):
            for x, value in enumerate(line.strip()):
                if value == '#':
                    borders.add((y, x))
                elif value == '<':
                    blizzards.append([(y, x), (0, -1)])
                elif value == '>':
                    blizzards.append([(y, x), (0, 1)])
                elif value == '^':
                    blizzards.append([(y, x), (-1, 0)])
                elif value == 'v':
                    blizzards.append([(y, x), (1, 0)])
                elif y == 0:
                    start = (y, x)
                elif y == len(lines) - 1:
                    end = (y, x)
                else:
                    pass
            else:
                MAXS[1] = x
        else:
            MAXS[0] = y

    borders.add((-1, start[1]))
    borders.add((y+1, end[1]))

    return blizzards, borders, start, end


def move(position, d, borders):
    next_position = list(i + j for i, j in zip(position, d))

    if tuple(next_position) in borders:
        index = [i for i, k in enumerate(d) if k != 0][0]
        next_position[index] = (next_position[index] + d[index]) % MAXS[index]
    return tuple(next_position)


def process_blizzards(blizzards, borders):
    for i, blizzard in enumerate(blizzards):
        next_position = move(blizzard[0], blizzard[1], borders)
        blizzards[i][0] = next_position


def get_neighbors(position):
    adjacents = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbors = []
    for a in adjacents:
        neighbors.append(tuple(i + j for i, j in zip(position, a)))
    return neighbors


def process_elf(positions, blizzards, borders):
    next_positions = set()
    blizzards_positions = get_blizzard_positions(blizzards)
    for position in positions:
        neighbors = get_neighbors(position)
        neighbors.append(position)
        for neighbor in neighbors:
            if neighbor not in blizzards_positions and neighbor not in borders:
                next_positions.add(neighbor)
    return next_positions


def get_blizzard_positions(blizzards):
    return set(blizzard[0] for blizzard in blizzards)


def get_shortest_path(blizzards, borders, start, end):
    positions = set([start])
    count = 0
    while True:
        process_blizzards(blizzards, borders)
        positions = process_elf(positions, blizzards, borders)
        count += 1
        if end in positions:
            break
    return count


def part1():
    blizzards, borders, start, end = load_input()

    result = get_shortest_path(blizzards, borders, start, end)

    print("Result 1: ", result)


def part2():
    blizzards, borders, start, end = load_input()

    cycles = 0
    cycles += get_shortest_path(blizzards, borders, start, end)
    cycles += get_shortest_path(blizzards, borders, end, start)
    cycles += get_shortest_path(blizzards, borders, start, end)
    result = cycles

    print("Result 2: ", result)


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
