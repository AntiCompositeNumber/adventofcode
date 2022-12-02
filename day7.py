#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations


def load_input() -> list[int]:
    with open("day7input.txt") as f:
        return [int(num.strip()) for num in next(f).split(",")]


def part1() -> None:
    positions = load_input()
    # positions = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    targets = {
        target: sum(abs(target - position) for position in positions)
        for target in range(min(positions), max(positions) + 1)
    }
    min_fuel = min(targets.values())
    best_target = next(target for target, fuel in targets.items() if fuel == min_fuel)
    print(f"Position {best_target}: {min_fuel} fuel")


def fuel_cost(position: int, target: int) -> int:
    dist = abs(position - target)
    # Triangular numbers ftw!
    cost = dist * (dist + 1) // 2
    return cost


def part2() -> None:
    positions = load_input()
    # positions = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    targets = {
        target: sum(fuel_cost(position, target) for position in positions)
        for target in range(min(positions), max(positions) + 1)
    }
    min_fuel = min(targets.values())
    best_target = next(target for target, fuel in targets.items() if fuel == min_fuel)
    print(f"Position {best_target}: {min_fuel} fuel")


if __name__ == "__main__":
    part2()
