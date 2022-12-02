#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations


def load_input(fn: str = "day10input.txt") -> list[str]:
    with open(fn) as f:
        return [line.strip() for line in f]


def find_error(line: str) -> str:
    closing = {"(": ")", "[": "]", "{": "}", "<": ">"}
    expected = []
    for char in line:
        if char in closing:
            expected.append(closing[char])
        elif char == expected[-1]:
            expected.pop()
        else:
            return char
    return ""


def part1(fn: str = "day10input.txt") -> None:
    lines = load_input(fn)
    errors = [err for line in lines if (err := find_error(line))]
    points = {")": 3, "]": 57, "}": 1197, ">": 25137}

    print("Errors:", len(errors), "Score:", sum(points[err] for err in errors))


def complete_line(line: str) -> str:
    closing = {"(": ")", "[": "]", "{": "}", "<": ">"}
    expected = []
    for char in line:
        if char in closing:
            expected.append(closing[char])
        elif char == expected[-1]:
            expected.pop()
        else:
            return ""

    return "".join(reversed(expected))


def score_completion(comp: str) -> int:
    score = 0
    points = {")": 1, "]": 2, "}": 3, ">": 4}
    for char in comp:
        score = score * 5 + points[char]

    return score


def part2(fn: str = "day10input.txt") -> None:
    lines = load_input(fn)
    ends = (end for line in lines if (end := complete_line(line)))
    scores = sorted(score_completion(end) for end in ends)
    score = scores[len(scores) // 2]
    print("Median completion score:", score)


if __name__ == "__main__":
    part1()
    part2()
