#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations


def load_input(fn: str = "day12input.txt") -> dict[str, list[str]]:
    data = {}
    with open(fn) as f:
        for line in f:
            a, b = line.strip().split("-")
            data.setdefault(a, []).append(b)
            data.setdefault(b, []).append(a)

    return data


def find_paths(
    data: dict[str, list[str]],
    start: str,
    current_path: list[str],
    all_paths: list[list[str]],
    double_back: bool = False,
) -> None:
    current_path.append(start)
    options = data[start]

    for option in options:
        this_path = current_path.copy()
        if option == "start":
            continue
        elif option.islower() and option in this_path:
            if double_back:
                find_paths(data, option, this_path, all_paths, double_back=False)
            else:
                continue
        elif option == "end":
            this_path.append(option)
            all_paths.append(this_path)
        else:
            find_paths(data, option, this_path, all_paths, double_back=double_back)


def part1(fn: str = "day12input.txt") -> None:
    data = load_input(fn)
    all_paths = []
    find_paths(data, "start", [], all_paths)
    print("Total paths:", len(all_paths))


def part2(fn: str = "day12input.txt") -> None:
    data = load_input(fn)
    all_paths = []
    find_paths(data, "start", [], all_paths, double_back=True)
    print("Total paths:", len(all_paths))


if __name__ == "__main__":
    part1()
