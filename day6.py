#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
import itertools
import collections


def load_data() -> list[int]:
    with open("day6input.txt") as f:
        return [int(num.strip()) for num in next(f).split(",")]


def lanternfish_day(age: int) -> list[int]:
    if age == 0:
        return [6, 8]
    return [age - 1]


def part1() -> None:
    data = [3, 4, 3, 1, 2]
    # data = load_data()
    for day in range(80):
        data = itertools.chain.from_iterable(map(lanternfish_day, data))

    print(f"Day {day + 1}: {len(list(data))} lanternfish")


def part2() -> None:
    data = load_data()
    # data = [3, 4, 3, 1, 2]
    days = 256

    state = collections.deque(data.count(i) for i in range(9))
    # print("Day:", 0, "Fish:", sum(state), "State:", state)
    for day in range(days):
        today = state.popleft()
        state[6] += today
        state.append(today)
        # print("Day:", day + 1, "Fish:", sum(state), "State:", state)

    print("Day:", day + 1, "Fish:", sum(state))


if __name__ == "__main__":
    part2()
