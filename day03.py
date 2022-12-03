#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

import string
import itertools
from collections.abc import Iterator


def load_input(filename: str = "day03input.txt") -> Iterator[str]:
    with open(filename) as f:
        for line in f:
            yield line.strip()


def priority(item: str) -> int:
    return string.ascii_letters.find(item) + 1


def compartment_dupes(line: str) -> str:
    hlen = len(line) // 2
    a, b = set(line[hlen:]), set(line[:hlen])
    dupes = a & b
    return dupes.pop()  # Only one duplicate expected


def elf_dupes(lines: list[str]) -> str:
    sets = [set(line) for line in lines]
    dupes = sets[0].intersection(*sets[1:])
    return dupes.pop()  # Still only one duplicate expected


def part1() -> None:
    total = sum(priority(compartment_dupes(line)) for line in load_input())
    print("PART 1 total:", total)


def part2() -> None:
    data = load_input()
    total = 0
    while lines := list(itertools.islice(data, 3)):
        total += priority(elf_dupes(lines))

    print("PART 2 total:", total)


def main() -> None:
    part1()
    part2()


if __name__ == "__main__":
    main()
