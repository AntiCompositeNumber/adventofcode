#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0


def load_data() -> list[int]:
    with open("day1input.txt") as f:
        return [int(line.strip()) for line in f]


def count_increases(data: list[int]) -> int:
    changes = 0
    for i, cur in enumerate(data):
        if i == 0:
            continue
        if cur > data[i - 1]:
            changes += 1

    return changes


def windowed_sum(data: list[int], window_size: int = 3) -> list[int]:
    sums = []
    for i in range(1, len(data) + 1):
        if i < window_size:
            continue
        cur_sum = sum(data[i - window_size : i])
        sums.append(cur_sum)
    return sums


def main():
    data = load_data()
    # Part 1
    print("Total measurements:", len(data))
    changes = count_increases(data)
    print("Changes:", changes)

    # Part 2
    windowed = windowed_sum(data)
    windowed_inc = count_increases(windowed)
    print("Increases (windoww_size=3):", windowed_inc)


if __name__ == "__main__":
    main()
