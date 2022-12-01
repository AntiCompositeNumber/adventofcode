#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0


def load_input():
    with open("day01input.txt") as f:
        for line in f:
            yield line.strip()


def main():
    totals = []
    cur = 0
    for line in load_input():
        if line:
            cur += int(line)
        else:
            totals.append(cur)
            cur = 0

    print("Max:", max(totals))
    top3 = sorted(totals)[-3:]
    print("Top 3:", sum(top3))


if __name__ == "__main__":
    main()
