#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
import math
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def load_input(fn: str = "day9input.txt") -> dict[Point, int]:
    with open(fn) as f:
        return {
            Point(int(x), int(y)): int(val)
            for y, row in enumerate(f)
            for x, val in enumerate(row.strip())
        }


def find_lows(data: dict[Point, int]) -> dict[Point, int]:
    lows = {
        point: val
        for point, val in data.items()
        if val
        < min(
            data.get(apoint, 10)  # Points on the edge are always lower than the edge
            for apoint in (
                point._replace(x=point.x - 1),
                point._replace(x=point.x + 1),
                point._replace(y=point.y - 1),
                point._replace(y=point.y + 1),
            )
        )
    }
    return lows


def part1(fn: str = "day9input.txt") -> None:
    data = load_input(fn)
    lows = find_lows(data)
    print("Total risks:", sum(val + 1 for val in lows.values()))


def walk_basin(
    point: Point, data: dict[Point, int], checked: set[Point] = set()
) -> set[Point]:
    basin = {point}
    checked.add(point)
    adjacents = (
        point._replace(x=point.x - 1),
        point._replace(x=point.x + 1),
        point._replace(y=point.y - 1),
        point._replace(y=point.y + 1),
    )
    for apoint in adjacents:
        if apoint in checked:
            continue
        checked.add(apoint)
        if data.get(apoint, 10) < 9:
            new_basins = walk_basin(apoint, data, checked)
            basin.update(new_basins)

    return basin


def part2(fn: str = "day9input.txt") -> None:
    data = load_input(fn)
    lows = find_lows(data)
    basins = [walk_basin(point, data, set()) for point in lows]
    largest = sorted((len(basin) for basin in basins), reverse=True)[:3]
    print("Product of largest basins:", math.prod(largest))


if __name__ == "__main__":
    part1()
    part2()
