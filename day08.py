#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0


import functools
from typing import NamedTuple
from collections import UserDict


class Point(NamedTuple):
    x: int
    y: int


class HeightMap(UserDict[Point, int]):
    @functools.cached_property
    def x_max(self) -> int:
        return max(point.x for point in self.keys())

    @functools.cached_property
    def y_max(self) -> int:
        return max(point.y for point in self.keys())

    def point_is_visible(self, point: Point) -> bool:
        return (
            point.x == 0
            or point.y == 0
            or point.x == self.x_max
            or point.y == self.y_max
            or self.visible_axis(point, "x", 0)
            or self.visible_axis(point, "x", self.x_max)
            or self.visible_axis(point, "y", 0)
            or self.visible_axis(point, "y", self.y_max)
        )

    def visible_axis(self, starting_point: Point, axis: str, stop: int) -> bool:
        if getattr(starting_point, axis) < stop:
            step = 1
        else:
            step = -1
        point = starting_point
        max_val = self[starting_point]
        for i, j in enumerate(
            range(getattr(starting_point, axis) + step, stop + step, step)
        ):
            point = point._replace(**{axis: j})
            if self[point] >= max_val:
                return False
        return True

    def visible_distance(self, starting_point: Point, axis: str, stop: int) -> int:
        if getattr(starting_point, axis) < stop:
            step = 1
        else:
            step = -1
        point = starting_point
        max_val = self[starting_point]
        i = -1
        for i, j in enumerate(
            range(getattr(starting_point, axis) + step, stop + step, step)
        ):
            point = point._replace(**{axis: j})
            if self[point] >= max_val:
                break
        return i + 1

    def scenic_score(self, point: Point) -> int:
        return (
            self.visible_distance(point, "x", 0)
            * self.visible_distance(point, "x", self.x_max)
            * self.visible_distance(point, "y", 0)
            * self.visible_distance(point, "y", self.y_max)
        )

    def pprint(self) -> None:
        out = "\n".join(
            "".join(str(self[Point(x, y)]) for x in range(0, self.x_max + 1))
            for y in range(0, self.y_max + 1)
        )
        print(out)

    def pprint_vis(self) -> None:
        out = "\n".join(
            "".join(
                str(int(self.point_is_visible(Point(x, y))))
                for x in range(0, self.x_max + 1)
            )
            for y in range(0, self.y_max + 1)
        )
        print(out)


def load_input(filename: str) -> HeightMap:
    with open(filename) as f:
        return HeightMap(
            (Point(x, y), int(val))
            for y, line in enumerate(f)
            for x, val in enumerate(line.strip())
        )


def main(filename: str = "day08input.txt") -> None:
    data = load_input(filename)
    part1 = sum(data.point_is_visible(point) for point in data)
    print("PART 1:", part1)

    part2 = max(data.scenic_score(point) for point in data)
    print("PART 2:", part2)


if __name__ == "__main__":
    main()
