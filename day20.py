#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
import collections
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Image(collections.UserDict):
    r: int = 1

    def __init__(self, *args, default: bool = False, algo: str = "", **kwargs):
        super().__init__(*args, **kwargs)
        self.default = default
        self.algo = algo

    def grid_number(self, center: Point) -> int:
        ret = 0
        for y in range(center.y - self.r, center.y + self.r + 1):
            for x in range(center.x - self.r, center.x + self.r + 1):
                point = Point(x, y)
                ret = (ret << 1) | self.get(point, self.default)

        return ret

    def enhance(self) -> Image:
        new_img = type(self)(
            default=self.default ^ (self.algo[0] == "#"), algo=self.algo
        )
        xmax = max(p.x for p in self)
        ymax = max(p.y for p in self)
        xmin = min(p.x for p in self)
        ymin = min(p.y for p in self)

        for y in range(ymin - self.r, ymax + self.r + 1):
            for x in range(xmin - self.r, xmax + self.r + 1):
                point = Point(x, y)
                i = self.grid_number(point)
                new_img[point] = self.algo[i] == "#"

        return new_img

    def __str__(self) -> str:
        xmax = max(p.x for p in self)
        ymax = max(p.y for p in self)
        xmin = min(p.x for p in self)
        ymin = min(p.y for p in self)

        return "\n".join(
            "".join(
                "#" if self.get(Point(x, y), self.default) else "."
                for x in range(xmin - 3 * self.r, xmax + 3 * self.r + 1)
            )
            for y in range(ymin - 3 * self.r, ymax + 3 * self.r + 1)
        )


def load_input(fn: str) -> Image:
    with open(fn) as f:
        img = Image(algo=next(f).strip())
        next(f)
        for y, line in enumerate(f):
            for x, val in enumerate(line.strip()):
                img[Point(x, y)] = val == "#"

    return img


def main(fn: str = "day20input.txt", passes: int = 2) -> None:
    img = load_input(fn)
    # print(str(img))
    for i in range(passes):
        img = img.enhance()
        # print("")
        # print(str(img))

    print(sum(img.values()), "pixels lit after", passes, "passes")


if __name__ == "__main__":
    main(passes=2)
    main(passes=50)
