#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
import math
import collections
from typing import NamedTuple, Iterator


class Point(NamedTuple):
    x: int
    y: int

    def dist(self, other: Point) -> int:
        return math.isqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


def load_input(fn: str = "day15input.txt") -> dict[Point, int]:
    with open(fn) as f:
        return {
            Point(x, y): int(val)
            for y, line in enumerate(f)
            for x, val in enumerate(line.strip())
        }


def dijkstra(start_pos: Point, end_pos: Point, data: dict[Point, int]) -> int:
    unvisited = set(data)
    t_dist = dict.fromkeys(unvisited, math.inf)
    t_dist[start_pos] = 0
    cur = start_pos
    while unvisited:
        cur_dist = t_dist[cur]
        for neighbor in neighbors(cur, data):
            n_dist = cur_dist + data[neighbor]
            if t_dist[neighbor] > n_dist:
                t_dist[neighbor] = n_dist

        unvisited.remove(cur)
        if end_pos not in unvisited:
            return t_dist[end_pos]

        cur = sorted(unvisited, key=lambda p: t_dist[p])[0]


def neighbors(start_pos: Point, data: dict[Point, int]) -> Iterator[Point]:
    for n in (
        start_pos._replace(x=start_pos.x - 1),
        start_pos._replace(x=start_pos.x + 1),
        start_pos._replace(y=start_pos.y - 1),
        start_pos._replace(y=start_pos.y + 1),
    ):
        if n in data:
            yield n


def part1(fn: str = "day15input.txt") -> None:
    data = load_input(fn)
    start = Point(0, 0)
    end = Point(max(p.x for p in data), max(p.y for p in data))
    lowest_risk = dijkstra(start, end, data)
    print("Lowest risk:", lowest_risk)


class BigMap(collections.UserDict):
    scale_factor: int = 5

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.base_x = max(p.x for p in self.data) + 1
        self.base_y = max(p.y for p in self.data) + 1

    def __getitem__(self, point: Point) -> int:
        if point.x < self.base_x and point.y < self.base_y:
            return self.data[point]
        elif (
            point.x >= self.base_x * self.scale_factor
            or point.y >= self.base_y * self.scale_factor
        ):
            raise KeyError(point)

        base_val = self.data[Point(x=point.x % self.base_x, y=point.y % self.base_y)]
        inc = (base_val + point.x // self.base_x + point.y // self.base_y) % 9
        if inc == 0:
            inc = 9
        return inc

    def __contains__(self, point: Point) -> int:
        if (point.x < self.base_x and point.y < self.base_y) or (
            point.x < 0 or point.y < 0
        ):
            return point in self.data
        elif (
            point.x >= self.base_x * self.scale_factor
            or point.y >= self.base_y * self.scale_factor
        ):
            return False
        else:
            return Point(x=point.x % self.base_x, y=point.y % self.base_y) in self.data

    def __iter__(self) -> Iterator[Point]:
        for x in range(self.base_x * self.scale_factor):
            for y in range(self.base_y * self.scale_factor):
                point = Point(x, y)
                if point in self:
                    yield point


def astar(start_pos: Point, end_pos: Point, data: dict[Point, int]) -> int:
    open_set = {start_pos}

    g_score = collections.defaultdict(lambda: math.inf)
    g_score[start_pos] = 0

    f_score = collections.defaultdict(lambda: math.inf)
    f_score[start_pos] = start_pos.dist(end_pos)

    while open_set:
        cur = sorted(open_set, key=lambda p: g_score[p])[0]
        if cur == end_pos:
            return g_score[end_pos]

        open_set.remove(cur)
        for neighbor in neighbors(cur, data):
            n_dist = g_score[cur] + data[neighbor]
            if g_score[neighbor] > n_dist:
                g_score[neighbor] = n_dist
                f_score[neighbor] = n_dist + neighbor.dist(end_pos)

                open_set.add(neighbor)


def part2(fn: str = "day15input.txt") -> None:
    data = BigMap(load_input(fn))
    start = Point(0, 0)
    end = Point(max(p.x for p in data), max(p.y for p in data))
    lowest_risk = astar(start, end, data)
    print("Lowest risk:", lowest_risk)


if __name__ == "__main__":
    part1()
