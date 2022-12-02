#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
from typing import NamedTuple


class Command(NamedTuple):
    direction: str
    value: int


class Position(NamedTuple):
    """
    Represents a position on an X-Y plane
    `x` is the horizontal position, with +oo in the "forward" direction
    `y` is the depth, with +oo in the "down" direction
    `aim` is a measure of angle, +oo is straight down, 0 is level, -oo is straight up
    """

    x: int = 0  # horizontal
    y: int = 0  # depth
    aim: int = 0  # angle

    def move(self, command: Command) -> Position:
        if command.direction == "forward":
            return self._replace(x=self.x + command.value)
        elif command.direction == "up":
            return self._replace(y=self.y - command.value)
        elif command.direction == "down":
            return self._replace(y=self.y + command.value)
        else:
            raise ValueError(command)

    def move_aim(self, command: Command) -> Position:
        if command.direction == "forward":
            return self._replace(
                x=self.x + command.value, y=self.y + self.aim * command.value
            )
        elif command.direction == "up":
            return self._replace(aim=self.aim - command.value)
        elif command.direction == "down":
            return self._replace(aim=self.aim + command.value)


def load_input():
    with open("day2input.txt") as f:
        data = []
        for line in f:
            direction, _, value = line.strip().partition(" ")
            data.append(Command(direction, int(value)))
        return data


def main():
    data = load_input()
    position = Position()
    for command in data:
        position = position.move_aim(command)

    print("Final:", position)
    print("x * y =", position.x * position.y)


if __name__ == "__main__":
    main()
