#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

# import collections
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int
    z: int


class Cuboid(NamedTuple):
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int
    state: bool = True

    def __contains__(self, other) -> bool:
        if not isinstance(other, Point):
            return super().__contains__(other)

        return (
            other.x >= self.x1
            and other.x <= self.x2
            and other.y >= self.y1
            and other.y <= self.y2
            and other.z >= self.z1
            and other.z <= self.z2
        )

    def isdisjoint(self, other: Cuboid) -> bool:
        return (
            (
                (self.x1 < other.x1 and self.x2 < other.x1)
                or (self.x2 > other.x2 and self.x1 > other.x2)
            )
            and (
                (self.y1 < other.y1 and self.y2 < other.y1)
                or (self.y2 > other.y2 and self.y1 > other.y2)
            )
            and (
                (self.z1 < other.z1 and self.z2 < other.z1)
                or (self.z2 > other.z2 and self.z1 > other.z2)
            )
        )

    @staticmethod
    def sub_line(a1: int, a2: int, b1: int, b2: int) -> list[tuple[int, int]]:
        if (a1 < b1 and a2 < b2) or (b1 < a1 and b2 < a2):
            # No overlap
            return [(a1, a2)]
        elif a1 >= b1 and a2 <= b2:
            # complete overlap
            return []
        elif a1 <= b1 and a2 <= b2:
            # Overlap on the positive side of a
            return [(a1, b1)]
        elif b1 <= a1 and b2 <= a2:
            # Overlap on the negative side of a
            return [(b2, a2)]
        elif a1 < b1 and a2 > b2:
            # a is cut by b
            return [(a1, b1), (b2, a2)]
        else:
            raise ValueError(a1, a2, b1, b2)

    def difference(self, other: Cuboid) -> list[Cuboid]:
        if self.isdisjoint(other):
            return [self, other]

        xlines = self.sub_line(self.x1, self.x2, other.x1, other.x2)
        ylines = self.sub_line(self.y1, self.y2, other.y1, other.y2)
        zlines = self.sub_line(self.z1, self.z2, other.z1, other.z2)

        if not (xlines or ylines or zlines):
            # completely consumed
            return []
        elif len(xlines) == 1 and len(ylines) == 1 and len(zlines) == 1:
            # simple subtraction
            x1, x2 = xlines[0]
            y1, y2 = ylines[0]
            z1, z2 = zlines[0]
            return [type(self)(x1, x2, y1, y2, z1, z2, True)]

