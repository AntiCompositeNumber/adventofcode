#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
from typing import NamedTuple, Iterable


class Point(NamedTuple):
    x: int
    y: int

    def adjacents(self) -> Iterable[Point]:
        for newx in range(self.x - 1, self.x + 2):
            for newy in range(self.y - 1, self.y + 2):
                yield type(self)(newx, newy)


def load_input(fn: str = "day11input.txt") -> dict[Point, int]:
    with open(fn) as f:
        return {
            Point(int(x), int(y)): int(val)
            for y, row in enumerate(f)
            for x, val in enumerate(row.strip())
        }


def do_step(data: dict[Point, int]) -> int:
    flashes = 0
    for point in data:
        data[point] += 1

    while any(val > 9 for val in data.values()):
        for point, val in data.items():
            if val > 9:
                for adj in point.adjacents():
                    adj_val = data.get(adj, -1)
                    if adj_val > -1:
                        data[adj] += 1
                data[point] = -1
                flashes += 1

    for point, val in data.items():
        if val == -1:
            data[point] = 0

    return flashes


def part1(fn: str = "day11input.txt") -> None:
    data = load_input(fn)
    total = sum(do_step(data) for i in range(100))
    print("Flashes after 100 steps:", total)


def part2(fn: str = "day11input.txt") -> None:
    data = load_input(fn)
    target, steps = len(data), 0

    while True:
        steps += 1
        if do_step(data) >= target:
            break

    print("Synchronized after", steps, "steps")


if __name__ == "__main__":
    part1()
    part2()
