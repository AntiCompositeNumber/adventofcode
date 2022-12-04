#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from typing import NamedTuple
from collections.abc import Iterator


class Range(NamedTuple):
    start: int
    end: int

    def fully_contains(self, other: "Range") -> bool:
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other: "Range") -> bool:
        if self.start <= other.start:
            return self.end >= other.start
        elif self.start >= other.start:
            return self.start <= other.end
        else:
            raise ValueError

    @classmethod
    def from_str(cls, rangestr: str) -> "Range":
        start, end = rangestr.split("-")
        return cls(int(start), int(end))


def str_to_pair(pair: str) -> tuple[Range, Range]:
    a, b = pair.strip().split(",")
    return Range.from_str(a), Range.from_str(b)


def load_input(filename: str = "day04input.txt") -> Iterator[tuple[Range, Range]]:
    with open(filename) as f:
        for line in f:
            yield str_to_pair(line)


def main() -> None:
    part1 = sum(a.fully_contains(b) or b.fully_contains(a) for a, b in load_input())
    print("PART 1 total:", part1)

    part2 = sum(a.overlaps(b) for a, b in load_input())
    print("PART 2 total:", part2)


if __name__ == "__main__":
    main()
