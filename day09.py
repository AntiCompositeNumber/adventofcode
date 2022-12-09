#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from typing import NamedTuple, Literal, cast
from collections import UserList
from collections.abc import Iterator


class Point(NamedTuple):
    x: int
    y: int

    def axis_move(self, axis: str, distance: int) -> "Point":
        return self._replace(**{axis: getattr(self, axis) + distance})


class Move(NamedTuple):
    direction: Literal["U", "D", "L", "R"]
    steps: int

    @classmethod
    def from_line(cls, line: str) -> "Move":
        direction, _, steps = line.partition(" ")
        if (not _) or direction not in "UDLR":
            raise ValueError(line)
        return cls(cast(Literal["U", "D", "L", "R"], direction), int(steps))


class Rope:
    """Original solution to Part 1. Does not generalize well."""

    def __init__(self):
        self._head = Point(0, 0)
        self.tail_history = set()
        self.tail = Point(0, 0)

    @property
    def head(self) -> Point:
        return self._head

    @head.setter
    def head(self, val: Point) -> None:
        self._head = val
        self.move_tail()

    @property
    def tail(self) -> Point:
        return self._tail

    @tail.setter
    def tail(self, val: Point) -> None:
        self.tail_history.add(val)
        self._tail = val

    def __repr__(self):
        return (
            f"{type(self).__name__}(head={self.head!r}, tail={self.tail!r}, "
            f"tail_history={self.tail_history!r})"
        )

    def move_head(self, move: Move) -> None:
        match move.direction:
            case "U":
                axis = "y"
                step = 1
            case "D":
                axis = "y"
                step = -1
            case "L":
                axis = "x"
                step = -1
            case "R":
                axis = "x"
                step = 1
            case _:
                raise TypeError(move)

        for i in range(move.steps):
            self.head = self.head.axis_move(axis, step)

    def move_tail(self) -> None:
        x_dist = self.head.x - self.tail.x
        y_dist = self.head.y - self.tail.y

        x_step = 1 if x_dist > 0 else -1
        y_step = 1 if y_dist > 0 else -1
        if abs(x_dist) <= 1 and abs(y_dist) <= 1:
            # touching, do nothing
            return
        elif x_dist == 0:
            self.tail = self.tail.axis_move("y", y_step)
        elif y_dist == 0:
            self.tail = self.tail.axis_move("x", x_step)
        else:
            self.tail = self.tail.axis_move("x", x_step).axis_move("y", y_step)

    def chart(
        self, x_min: int = 0, y_min: int = 0, x_max: int = 5, y_max: int = 4
    ) -> None:
        out = ""
        for y in range(y_max, y_min - 1, -1):
            for x in range(x_min, x_max + 1):
                cur = Point(x, y)
                if self.head == cur:
                    out += "H"
                elif self.tail == cur:
                    out += "T"
                else:
                    out += "."
            out += "\n"
        print(out)

    def chart_history(
        self, x_min: int = 0, y_min: int = 0, x_max: int = 5, y_max: int = 4
    ) -> None:
        out = ""
        for y in range(y_max, y_min - 1, -1):
            for x in range(x_min, x_max + 1):
                cur = Point(x, y)
                if cur in self.tail_history:
                    out += "#"
                else:
                    out += "."
            out += "\n"
        print(out)


class LongRope(UserList[Point]):
    def __init__(self):
        self.tail_history: set[Point] = set()

    @classmethod
    def new(cls, length: int = 10):
        rope = cls()
        rope.data = [Point(0, 0) for i in range(length)]
        rope.tail_history = {rope.data[-1]}
        return rope

    def __setitem__(self, i, item) -> None:
        self.data[i] = item
        if i == -1 or i == len(self.data) - 1:
            self.tail_history.add(item)

    def __repr__(self):
        return (
            f"{type(self).__name__}(data={self.data!r}, "
            f"tail_history={self.tail_history!r})"
        )

    def move_head(self, move: Move) -> None:
        match move.direction:
            case "U":
                axis = "y"
                step = 1
            case "D":
                axis = "y"
                step = -1
            case "L":
                axis = "x"
                step = -1
            case "R":
                axis = "x"
                step = 1
            case _:
                raise TypeError(move)

        for i in range(move.steps):
            self[0] = self[0].axis_move(axis, step)
            self.propegate_move()

        # self.chart()  # XXX
        # breakpoint()

    def propegate_move(self) -> None:
        for i in range(1, len(self)):
            self.move_knot(i)

    def move_knot(self, knot: int) -> None:
        prev = knot - 1
        x_dist = self[prev].x - self[knot].x
        y_dist = self[prev].y - self[knot].y

        x_step = 1 if x_dist > 0 else -1
        y_step = 1 if y_dist > 0 else -1
        if abs(x_dist) <= 1 and abs(y_dist) <= 1:
            # touching, do nothing
            return
        elif x_dist == 0:
            self[knot] = self[knot].axis_move("y", y_step)
        elif y_dist == 0:
            self[knot] = self[knot].axis_move("x", x_step)
        else:
            self[knot] = self[knot].axis_move("x", x_step).axis_move("y", y_step)

    def chart(
        self, x_min: int = -11, y_min: int = -5, x_max: int = 14, y_max: int = 15
    ) -> None:
        out = ""
        for y in range(y_max, y_min - 1, -1):
            for x in range(x_min, x_max + 1):
                cur = Point(x, y)
                if cur in self:
                    curpos = self.index(cur)
                    if curpos == 0:
                        out += "H"
                    else:
                        out += str(curpos)
                else:
                    out += "."
            out += "\n"
        print(out)

    def chart_history(
        self, x_min: int = -11, y_min: int = -5, x_max: int = 14, y_max: int = 15
    ) -> None:
        out = ""
        for y in range(y_max, y_min - 1, -1):
            for x in range(x_min, x_max + 1):
                cur = Point(x, y)
                if cur in self.tail_history:
                    out += "#"
                else:
                    out += "."
            out += "\n"
        print(out)


def load_input(filename: str) -> Iterator[Move]:
    with open(filename) as f:
        for line in f:
            yield Move.from_line(line.strip())


def part1(filename: str = "day09input.txt") -> None:
    moves = load_input(filename)
    rope = Rope()
    for move in moves:
        rope.move_head(move)

    part1 = len(rope.tail_history)
    print("PART 1:", part1)


def part1alt(filename: str = "day09input.txt") -> None:
    moves = load_input(filename)
    rope = LongRope.new(length=2)
    for move in moves:
        rope.move_head(move)

    part1 = len(rope.tail_history)
    print("PART 1 (redux):", part1)


def part2(filename: str = "day09input.txt") -> None:
    moves = load_input(filename)
    rope = LongRope.new(length=10)
    for move in moves:
        rope.move_head(move)

    total = len(rope.tail_history)
    print("PART 2:", total)


def main() -> None:
    part1()
    part1alt()
    part2()


if __name__ == "__main__":
    main()
