#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
import collections
import math
import itertools
from typing import NamedTuple, Iterator


class RelativePoint(NamedTuple):
    x: int
    y: int
    z: int
    relative_to: Scanner = None

    def distance(self, other: RelativePoint) -> float:
        if not isinstance(other, RelativePoint):
            raise TypeError(other)
        elif self.relative_to is not other.relative_to:
            raise TypeError(
                "Can not calculate distance between points"
                " relative to different positions"
            )
        return math.dist(self[:3], other[:3])

    def manhattan(self, other: RelativePoint) -> int:
        if not isinstance(other, RelativePoint):
            raise TypeError(other)
        elif self.relative_to is not other.relative_to:
            raise TypeError(
                "Can not calculate distance between points"
                " relative to different positions"
            )
        return sum(abs(t[0] - t[1]) for t in zip(self[:3], other[:3]))

    def resolve(self) -> RelativePoint:
        if (
            not self.relative_to
            or self.relative_to.position.relative_to is self.relative_to
        ):
            return self
        origin = self.relative_to.position
        res = self.rotate(self.relative_to.orientation[0]).scale(
            self.relative_to.orientation[1]
        )
        return type(self)(
            x=origin.x - res.x,
            y=origin.y - res.y,
            z=origin.z - res.z,
            relative_to=origin.relative_to,
        ).resolve()

    def rotate_z(self, turns: int) -> RelativePoint:
        if turns == 0:
            return self
        c, s = [(1, 0), (0, 1), (-1, 0), (0, -1)][turns % 4]
        return self._replace(x=self.x * c - self.y * s, y=self.x * s + self.y * c)

    def rotate_x(self, turns: int) -> RelativePoint:
        if turns == 0:
            return self

        c, s = [(1, 0), (0, 1), (-1, 0), (0, -1)][turns % 4]
        return self._replace(y=self.y * c - self.z * s, z=self.y * s + self.z * c)

    def rotate_y(self, turns: int) -> RelativePoint:
        if turns == 0:
            return self

        c, s = [(1, 0), (0, 1), (-1, 0), (0, -1)][turns % 4]
        return self._replace(z=self.z * c - self.x * s, x=self.z * s + self.x * c)

    def rotate(self, turns: tuple[int]) -> RelativePoint:
        return self.rotate_x(turns[0]).rotate_y(turns[1]).rotate_z(turns[2])

    def scale(self, factors: tuple[int]) -> RelativePoint:
        return self._replace(
            x=self.x * factors[0], y=self.y * factors[1], z=self.z * factors[2]
        )


class Scanner(collections.UserList):
    def __init__(self, *args, scanner_id: int, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.scanner_id: int = scanner_id
        self.distance_map: dict[RelativePoint, dict[float, RelativePoint]] = {}
        self.position: RelativePoint = RelativePoint(0, 0, 0, relative_to=self)
        self.orientation: tuple[tuple[int, int, int], tuple[int, int, int]] = (
            (0, 0, 0),
            (1, 1, 1),
        )

    def __repr__(self) -> str:
        if self.data:
            data = "[...]"
        else:
            data = "[]"

        if self.distance_map:
            distmap = ", distance_map={...}"
        else:
            distmap = ""
        return (
            f"{type(self).__qualname__}({data}, scanner_id={self.scanner_id}{distmap})"
        )

    def __hash__(self) -> int:
        return id(self)

    def gen_map(self) -> None:
        for point in self.data:
            point_map = {}
            for other in self.data:
                if other != point:
                    point_map[point.distance(other)] = other
            self.distance_map[point] = point_map

    def match(self, other: Scanner):
        if not self.distance_map:
            self.gen_map()
        if not other.distance_map:
            other.gen_map()

        point_matches = {}
        for spoint, smap in self.distance_map.items():
            counts = collections.Counter(
                omap[dist]
                for omap in other.distance_map.values()
                for dist in smap
                if dist in omap
            )
            mc = counts.most_common(1)
            if mc:
                point_matches[spoint] = mc[0][0]
        return point_matches

    def rel_position(self, relative_to: Scanner) -> None:
        matches = relative_to.match(self)
        if len(matches) < 12 or relative_to.position.relative_to is self:
            return False
        # print(self.scanner_id, relative_to.scanner_id, len(matches))
        for mul in itertools.product([1, -1], repeat=3):
            for rot in itertools.product(range(4), repeat=3):
                s = set(
                    tuple(
                        sum(p)
                        for p in zip(item[0][:3], item[1].rotate(rot).scale(mul)[:3])
                    )
                    for item in matches.items()
                )
                if len(s) == 1:
                    pos = s.pop()
                    pos = RelativePoint(
                        x=pos[0], y=pos[1], z=pos[2], relative_to=relative_to
                    )
                    break
            else:
                continue
            break
        else:
            return False
        self.position = pos
        self.orientation = (rot, mul)
        return True


def load_input(fn: str = "day19input.txt") -> Iterator[Scanner]:
    with open(fn) as f:
        for line in f:
            if line.startswith("---"):
                scanner = Scanner(scanner_id=int(line.split(" ")[2]))
            elif line == "\n":
                yield scanner
            else:
                x, y, z = line.strip().split(",")
                scanner.append(
                    RelativePoint(int(x), int(y), int(z), relative_to=scanner)
                )
        yield scanner


def main(fn: str = "day19input.txt") -> None:
    data = list(load_input(fn))
    to_check = collections.deque(data.copy())
    scanner0 = to_check.popleft()
    beacons = set(scanner0)

    while to_check:
        scanner = to_check.popleft()
        if scanner.position.relative_to is not scanner:
            pass
            # print(scanner.scanner_id, scanner.position.relative_to.scanner_id)
        if scanner.position.resolve().relative_to is scanner0:
            # print(scanner.scanner_id)
            beacons.update(set(beacon.resolve() for beacon in scanner))
            continue
        for other in data:
            if scanner.position.relative_to is not other and scanner.rel_position(
                other
            ):
                break
        to_check.append(scanner)

    print(len(beacons), "beacons found")

    scanners = [scanner.position.resolve() for scanner in data]
    largest_dist = max(
        scanner.manhattan(other)
        for scanner, other in itertools.combinations(scanners, 2)
    )
    print("Largest distance between scanners:", largest_dist)
