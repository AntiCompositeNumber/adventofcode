#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import re
import collections
import math
import operator
import functools
from collections.abc import Callable

WorryLevel = int
MonkeyId = int

Operation = Callable[[WorryLevel], WorryLevel]


@dataclasses.dataclass
class Monkey:
    items: collections.deque[WorryLevel]
    operation: Operation
    test: int
    test_true: MonkeyId
    test_false: MonkeyId
    count: int = 0

    def turn(
        self, monkeys: list[Monkey], worried: bool = False, lcm: int | None = None
    ) -> None:
        while self.items:
            item = self.items.popleft()
            item = self.operation(item)
            if not worried:
                item = math.floor(item / 3)
            if lcm is not None:
                # We only need to test for divisibility.
                # Anything divisible by the lcm has more data than we need
                # to calculate divisibility by self.test.
                # That data can be thrown away.
                item = item % lcm

            if (item % self.test) == 0:
                target = self.test_true
            else:
                target = self.test_false
            monkeys[target].items.append(item)
            self.count += 1


def load_input(filename: str) -> list[Monkey]:
    regex = r"""Monkey (\d):
  Starting items: ([\d ,]+)
  Operation: new = old (.*?)
  Test: divisible by (\d+)
    If true: throw to monkey (\d)
    If false: throw to monkey (\d)"""
    monkeys = []
    with open(filename) as f:
        for raw_monkey in f.read().split("\n\n"):
            match = re.match(regex, raw_monkey)
            if not match:
                raise ValueError
            match match[3].split():
                case ["*", "old"]:
                    operation: Operation = functools.partial(pow, exp=2)
                case ["*", op_val]:
                    operation = functools.partial(operator.mul, int(op_val))
                case ["+", op_val]:
                    operation = functools.partial(operator.add, int(op_val))
                case _:
                    raise ValueError

            monkeys.append(
                Monkey(
                    items=collections.deque(
                        WorryLevel(x) for x in match[2].split(", ")
                    ),
                    operation=operation,
                    test=int(match[4]),
                    test_true=MonkeyId(match[5]),
                    test_false=MonkeyId(match[6]),
                )
            )

    return monkeys


def part1(filename="day11input.txt") -> None:
    monkeys = load_input(filename)
    for i in range(20):
        for monkey in monkeys:
            monkey.turn(monkeys)

    top_two = sorted(monkey.count for monkey in monkeys)[-2:]
    monkey_business = top_two[0] * top_two[1]
    print("PART 1:", monkey_business)


def part2(filename="day11input.txt") -> None:
    monkeys = load_input(filename)
    lcm = math.lcm(*[monkey.test for monkey in monkeys])
    for i in range(10000):
        for monkey in monkeys:
            monkey.turn(monkeys, worried=True, lcm=lcm)

    top_two = sorted(monkey.count for monkey in monkeys)[-2:]
    monkey_business = top_two[0] * top_two[1]
    print("PART 1:", monkey_business)


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
