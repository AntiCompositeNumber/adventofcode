#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
import collections


def load_input(fn: str = "day14input.txt") -> tuple[list[str], dict[str, str]]:
    with open(fn) as f:
        template = list(next(f).strip())
        next(f)
        rules = {}
        for line in f:
            k, v = line.strip().split(" -> ")
            rules[k] = v

        return template, rules


def make_chains(rules: dict[str, str], polymer: list[str]) -> list[str]:
    new_poly = []
    for i, elem in enumerate(polymer):
        new_poly.append(elem)
        try:
            next_elem = polymer[i + 1]
        except IndexError:
            break
        new_elem = rules.get(elem + next_elem, "")
        if new_elem:
            new_poly.append(new_elem)

    return new_poly


def part1(fn: str = "day14input.txt") -> None:
    poly, rules = load_input(fn)
    for i in range(10):
        poly = make_chains(rules, poly)

    counter = collections.Counter(poly)
    counts = counter.most_common()
    most_common = counts[0][1]
    least_common = counts[-1][1]
    print("Qmost - Qleast =", most_common - least_common)


def make_pairs(template: list[str], rules: dict[str, str]) -> collections.Counter[str]:
    counter = collections.Counter()
    for i, elem in enumerate(template):
        try:
            next_elem = template[i + 1]
        except IndexError:
            break

        counter[elem + next_elem] += 1

    return counter


def pair_chains(
    counter: collections.Counter[str], rules: dict[str, str]
) -> collections.Counter[str]:
    new_counter = collections.Counter()
    for pair, count in counter.items():
        new_elem = rules.get(pair, "")
        if new_elem:
            new_counter[pair[0] + new_elem] += count
            new_counter[new_elem + pair[1]] += count
        else:
            new_counter[pair] += count

    return new_counter


def part2(fn: str = "day14input.txt", steps: int = 40) -> None:
    template, rules = load_input(fn)
    pairs = make_pairs(template, rules)

    for step in range(steps):
        pairs = pair_chains(pairs, rules)

    double_counter = collections.Counter()
    for pair, count in pairs.items():
        double_counter[pair[0]] += count
        double_counter[pair[1]] += count

    # The first and last elements of the template aren't double-counted
    double_counter[template[0]] += 1
    double_counter[template[-1]] += 1

    counts = double_counter.most_common()
    most_common = counts[0][1]
    least_common = counts[-1][1]
    print("Qmost - Qleast =", (most_common - least_common) // 2, f"(steps={steps})")


if __name__ == "__main__":
    part1()
