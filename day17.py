#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
from typing import NamedTuple, Optional


class Probe(NamedTuple):
    x: int
    y: int
    vx: int
    vy: int
    ymax: int = 0

    def step(self) -> Probe:
        x, y = self.x + self.vx, self.y + self.vy
        if self.vx > 0:
            vx = self.vx - 1
        elif self.vx < 0:
            vx = self.vx + 1
        else:
            vx = self.vx
        vy = self.vy - 1
        if y > self.ymax:
            ymax = y
        else:
            ymax = self.ymax
        return type(self)(x=x, y=y, vx=vx, vy=vy, ymax=ymax)

    def run(self, target: BBox) -> Optional[Probe]:
        probe = self
        while True:
            probe = probe.step()
            if probe in target:
                return probe
            elif probe.x > target.x2 or (probe.y < target.y1 and probe.vy < 0):
                return None


class BBox(NamedTuple):
    x1: int
    x2: int
    y1: int
    y2: int

    def __contains__(self, point: Probe) -> bool:
        if not isinstance(point, Probe):
            raise NotImplementedError(point)
        return (
            point.x >= self.x1
            and point.x <= self.x2
            and point.y >= self.y1
            and point.y <= self.y2
        )


def load_input(in_str: str):
    in_str = in_str.partition(": ")[2]
    x_str, y_str = in_str.split(", ")
    x_str = x_str.strip().replace("x=", "")
    y_str = y_str.strip().replace("y=", "")
    x1, x2 = [int(val) for val in x_str.split("..")]
    y1, y2 = [int(val) for val in y_str.split("..")]
    return BBox(x1, x2, y1, y2)


def part1(in_str: str = "target area: x=124..174, y=-123..-86") -> None:
    target = load_input(in_str)

    solutions = []
    for vx in range(0, target.x2):
        for vy in range(0, target.x2):
            probe = Probe(0, 0, vx, vy)
            probe = probe.run(target)
            if probe:
                solutions.append(probe)

    max_y = max(p.ymax for p in solutions)
    print("Highest Y value:", max_y)


def part2(in_str: str = "target area: x=124..174, y=-123..-86") -> None:
    target = load_input(in_str)
    min_min = min(*target)
    max_max = max(*target) + 1

    solutions = 0
    for vx in range(0, max_max):
        for vy in range(min_min, max_max):
            probe = Probe(0, 0, vx, vy)
            probe = probe.run(target)
            if probe:
                solutions += 1

    print("Total solutions:", solutions)


if __name__ == "__main__":
    part1()
    part2()
