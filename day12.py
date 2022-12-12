#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
import string
import math
import collections
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def dist(self, other: Point) -> int:
        return math.isqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class HeightMap(collections.UserDict[Point, int]):
    def __init__(
        self, *args, start: Point | None = None, end: Point | None = None
    ) -> None:
        self.start = start
        self.end = end

        super().__init__(*args)

    def __repr__(self) -> str:
        return (
            f"{type(self).__qualname__}(start={self.start!r}, "
            f"end={self.end!r}, data={self.data!r})"
        )

    def adjacent(self, point: Point, max_step: int = 1) -> list[Point]:
        return [
            new_point
            for new_point in (
                point._replace(x=point.x - 1),
                point._replace(x=point.x + 1),
                point._replace(y=point.y - 1),
                point._replace(y=point.y + 1),
            )
            if new_point in self and self[new_point] >= self[point] - max_step
        ]

    def dijkstra(self, starts: set[Point] = set()) -> float:
        if self.start is None or self.end is None:
            raise ValueError
        if not starts:
            starts = {self.start}

        # For part 2, easiest to solve backwards.
        unvisited = set(self.keys())
        t_dist = dict.fromkeys(unvisited, math.inf)
        t_dist[self.end] = 0
        cur = self.end
        while unvisited:
            cur_dist = t_dist[cur]
            for neighbor in self.adjacent(cur):
                n_dist = cur_dist + 1
                if t_dist[neighbor] > n_dist:
                    t_dist[neighbor] = n_dist

            unvisited.remove(cur)
            if starts.isdisjoint(unvisited):
                return min(t_dist[start] for start in starts)

            cur = sorted(unvisited, key=lambda p: t_dist[p])[0]

        raise ValueError("No path found")


def load_input(filename: str) -> HeightMap:
    heightmap = HeightMap()
    with open(filename) as f:
        for y, line in enumerate(f):
            for x, heightstr in enumerate(line.strip()):
                point = Point(x, y)
                match heightstr:
                    case "S":
                        height = 0
                        heightmap.start = point
                    case "E":
                        height = 25
                        heightmap.end = point
                    case _:
                        height = string.ascii_lowercase.find(heightstr)
                heightmap[point] = height
    return heightmap


def main(filename: str = "day12input.txt") -> None:
    heightmap = load_input(filename)
    part1 = heightmap.dijkstra()
    print("PART 1:", part1)

    part2 = heightmap.dijkstra(
        {point for point, height in heightmap.items() if height == 0}
    )
    print("PART 2:", part2)


if __name__ == "__main__":
    main()
