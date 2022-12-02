#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from typing import NamedTuple, Iterator


class Line(NamedTuple):
    x0: int
    y0: int
    x1: int
    y1: int


class Point(NamedTuple):
    x: int
    y: int


class Chart(dict):
    def inc(self, point) -> None:
        self[point] = self.get(point, 0) + 1

    def plot_constant(self, line) -> None:
        """Only plot horizontal or vertical lines"""
        if line.x0 == line.x1 or line.y0 == line.y1:
            self.plot_line(line)

    def plot_line(self, line) -> None:
        if line.x0 == line.x1:
            if line.y0 < line.y1:
                yrange = range(line.y0, line.y1 + 1)
            else:
                yrange = range(line.y0, line.y1 - 1, -1)
            xrange = [line.x0] * len(yrange)
        elif line.y0 == line.y1:
            if line.x0 < line.x1:
                xrange = range(line.x0, line.x1 + 1)
            else:
                xrange = range(line.x0, line.x1 - 1, -1)
            yrange = [line.y0] * len(xrange)
        elif abs((line.y1 - line.y0) / (line.x1 - line.x0)) == 1:
            if line.y0 < line.y1:
                yrange = range(line.y0, line.y1 + 1)
            else:
                yrange = range(line.y0, line.y1 - 1, -1)
            if line.x0 < line.x1:
                xrange = range(line.x0, line.x1 + 1)
            else:
                xrange = range(line.x0, line.x1 - 1, -1)
        else:
            return

        for x, y in zip(xrange, yrange):
            p = Point(x, y)
            self[p] = self.get(p, 0) + 1

    def intersections(self) -> int:
        return len([val for val in self.values() if val >= 2])

    def __repr__(self) -> str:
        xmax = max(p.x for p in self) + 1
        ymax = max(p.y for p in self) + 1
        return "\n".join(
            "".join(str(self.get(Point(x, y), ".")) for x in range(xmax))
            for y in range(ymax)
        )


def load_input() -> Iterator[Line]:
    with open("day5input.txt") as f:
        for line in f:
            p0, p1 = line.split(" -> ")
            (x0, y0), (x1, y1) = p0.split(","), p1.split(",")
            yield Line(*[int(p.strip()) for p in [x0, y0, x1, y1]])


def part1():
    chart = Chart()
    for line in load_input():
        chart.plot_constant(line)

    print("DANGER:", chart.intersections(), "overlaps")


def part2():
    chart = Chart()
    for line in load_input():
        chart.plot_line(line)

    print("DANGER:", chart.intersections(), "overlaps")


if __name__ == "__main__":
    part2()
