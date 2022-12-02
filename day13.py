#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Fold(NamedTuple):
    direction: str
    value: int


def load_input(fn: str = "day13input.txt") -> tuple[set[Point], list[Fold]]:
    points, folds = set(), []
    with open(fn) as f:
        for line in f:
            if line == "\n":
                break

            x, y = line.strip().split(",")
            points.add(Point(x=int(x), y=int(y)))

        for line in f:
            direction, sep, val = line.strip().rpartition("=")
            folds.append(Fold(direction=direction[-1], value=int(val)))

    return points, folds


def fold_points(points: set[Point], fold: Fold) -> set[Point]:
    new_points = set()
    for point in points:
        pos = getattr(point, fold.direction)
        if pos < fold.value:
            new_points.add(point)
            continue
        new_pos = fold.value - (pos - fold.value)
        new_points.add(point._replace(**{fold.direction: new_pos}))

    return new_points


def print_points(points: set[Point]) -> None:
    xrange = range(0, max(point.x for point in points) + 1)
    yrange = range(0, max(point.y for point in points) + 1)
    out = "\n".join(
        "".join("\u2588" if Point(x, y) in points else " " for x in xrange)
        for y in yrange
    )
    print(out)


def part1(fn: str = "day13input.txt") -> None:
    points, folds = load_input(fn)
    new_points = fold_points(points, folds[0])

    print("After first fold:", len(new_points), "dots visible")


def part2(fn: str = "day13input.txt") -> None:
    points, folds = load_input(fn)
    for fold in folds:
        points = fold_points(points, fold)

    print_points(points)


if __name__ == "__main__":
    part1()
