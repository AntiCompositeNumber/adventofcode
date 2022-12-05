#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

import re
from typing import NamedTuple


class Move(NamedTuple):
    count: int
    from_stack: int
    to_stack: int


def load_input(filename: str = "day05input.txt") -> tuple[list[list[str]], list[Move]]:
    stacks = [list() for i in range(9)]
    moves = []

    with open(filename) as f:
        # first parse the annoying drawing
        data_cols = [(i * 4) - 3 for i in range(1, 10)]
        for row in f:
            if row.startswith(" "):
                break
            for col, char in enumerate(row):
                if col in data_cols and char != " ":
                    stacks[data_cols.index(col)].append(char)

        next(f)  # skip blank row
        for row in f:
            match = re.match(r"move (\d+) from (\d+) to (\d+)", row)
            moves.append(Move(*[int(a) for a in match.groups()]))

    for stack in stacks:
        stack.reverse()

    return stacks, moves


def part1() -> None:
    stacks, moves = load_input()
    for move in moves:
        for i in range(move.count):
            stacks[move.to_stack - 1].append(stacks[move.from_stack - 1].pop())

    tops = "".join(stack[-1] for stack in stacks)
    print("PART 1:", tops)


def part2() -> None:
    stacks, moves = load_input()
    for move in moves:
        partial = stacks[move.from_stack - 1][-move.count :]
        stacks[move.to_stack - 1].extend(partial)
        del stacks[move.from_stack - 1][-move.count :]

    tops = "".join(stack[-1] for stack in stacks)
    print("PART 2:", tops)


def main() -> None:
    part1()
    part2()


if __name__ == "__main__":
    main()
