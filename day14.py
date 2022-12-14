#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
import enum
import functools
from typing import NamedTuple
from collections import UserDict


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_str(cls, pair: str) -> Point:
        x, _, y = pair.strip().partition(",")
        if not _:
            raise ValueError(pair)
        return cls(int(x), int(y))


class Tile(enum.Enum):
    AIR = enum.auto()
    ROCK = enum.auto()
    SAND = enum.auto()
    SAND_SOURCE = enum.auto()


class Scan(UserDict[Point, Tile]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if Tile.SAND_SOURCE not in self.values():
            self[Point(500, 0)] = Tile.SAND_SOURCE

    def __missing__(self, key: Point) -> Tile:
        return Tile.AIR

    @functools.cached_property
    def x_max(self) -> int:
        return max(point.x for point in self.data)

    @functools.cached_property
    def x_min(self) -> int:
        return min(point.x for point in self.data)

    @functools.cached_property
    def y_max(self) -> int:
        return max(point.y for point in self.data)

    @functools.cached_property
    def y_min(self) -> int:
        return min(point.y for point in self.data)

    def load_rock(self, line: str) -> None:
        raw_points = iter(line.split(" -> "))
        from_point = Point.from_str(next(raw_points))
        for raw_point in raw_points:
            to_point = Point.from_str(raw_point)

            if from_point.x == to_point.x:
                axis = "y"
            elif from_point.y == to_point.y:
                axis = "x"
            else:
                raise ValueError(from_point, to_point)

            if (start := getattr(from_point, axis)) < (end := getattr(to_point, axis)):
                r = range(start, end + 1)
            else:
                r = range(end, start + 1)

            for n in r:
                point = from_point._replace(**{axis: n})
                self[point] = Tile.ROCK

            from_point = to_point

    def pprint(self) -> None:
        out = ""
        for y in range(self.y_min, self.y_max + 1):
            for x in range(self.x_min, self.x_max + 1):
                match self[Point(x, y)]:
                    case Tile.AIR:
                        out += "."
                    case Tile.ROCK:
                        out += "#"
                    case Tile.SAND:
                        out += "o"
                    case Tile.SAND_SOURCE:
                        out += "+"
                    case _:
                        raise ValueError
            out += "\n"
        print(out)

    def add_sand(self, void: bool) -> bool:
        pos = next(point for point, tile in self.items() if tile is Tile.SAND_SOURCE)
        while True:
            if void and (pos.y > self.y_max):
                return False
            for possible_pos in [
                pos._replace(y=pos.y + 1),
                pos._replace(y=pos.y + 1, x=pos.x - 1),
                pos._replace(y=pos.y + 1, x=pos.x + 1),
            ]:
                if self[possible_pos] is Tile.AIR:
                    pos = possible_pos
                    break
            else:
                if self[pos] is Tile.SAND_SOURCE:
                    self[pos] = Tile.SAND
                    return False
                else:
                    self[pos] = Tile.SAND
                    return True

    def simulate(self, void: bool) -> None:
        while self.add_sand(void=void):
            pass

    @classmethod
    def load_input(cls, filename: str) -> Scan:
        scan = cls()
        with open(filename) as f:
            for line in f:
                scan.load_rock(line.strip())
        return scan


class FloorScan(Scan):
    def __missing__(self, key: Point) -> Tile:
        if key.y == self.y_max + 2:
            return Tile.ROCK
        return super().__missing__(key)


def part1(filename: str = "day14input.txt") -> None:
    scan = Scan.load_input(filename)
    scan.simulate(void=True)
    part1 = sum(True for val in scan.values() if val is Tile.SAND)
    print("PART 1:", part1)


def part2(filename: str = "day14input.txt") -> None:
    scan = FloorScan.load_input(filename)
    scan.simulate(void=False)
    part2 = sum(True for val in scan.values() if val is Tile.SAND)
    print("PART 2:", part2)


def main(filename: str = "day14input.txt") -> None:
    part1(filename)
    part2(filename)


if __name__ == "__main__":
    main()
