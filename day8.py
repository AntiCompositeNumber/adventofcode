#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations


def load_input() -> list[tuple[list[str], list[str]]]:
    with open("day8input.txt") as f:
        return [
            tuple(
                [word.strip() for word in group.split(" ")]
                for group in line.split(" | ")
            )
            for line in f
        ]


def part1() -> None:
    unique_lens = {2: 1, 3: 7, 4: 4, 7: 8}
    data = load_input()
    uniques = [word for line in data for word in line[1] if len(word) in unique_lens]
    print(len(uniques))


outputs_for_len = {
    2: [1],
    3: [7],
    4: [4],
    5: [2, 3, 5],
    6: [0, 6, 9],
    7: [8],
}

letters = {
    0: {"a", "b", "c", "e", "f", "g"},
    1: {"c", "f"},
    2: {"a", "c", "d", "e", "g"},
    3: {"a", "c", "d", "f", "g"},
    4: {"b", "c", "d", "f"},
    5: {"a", "b", "d", "f", "g"},
    6: {"a", "b", "d", "e", "f", "g"},
    7: {"a", "c", "f"},
    8: {"a", "b", "c", "d", "e", "f", "g"},
    9: {"a", "b", "c", "d", "f", "g"},
}

digits = {frozenset(v): str(k) for k, v in letters.items()}


def make_map(signals: list[str]) -> dict[str, set[str]]:
    signals = [set(word) for word in signals]
    signal_lens = {}
    for word in signals:
        signal_lens.setdefault(len(word), []).append(word)
    known_map = {}

    # First, take care of the uniques
    # len == 2 -> 1 and len == 3 -> 7. The only overlap between them is line 'a'
    cf = signal_lens[2][0]
    acf = signal_lens[3][0]
    bcdf = signal_lens[4][0]
    abcdefg = signal_lens[7][0]
    known_map["a"] = (acf - cf).pop()

    # intersection between all values with len 5 is {g, d, a}
    adg = signal_lens[5][0].intersection(*signal_lens[5][1:])

    # intersection between all values with len 6 is {g, f, b, a}
    abfg = signal_lens[6][0].intersection(*signal_lens[6][1:])

    bdf = adg ^ abfg
    set_c = bcdf - bdf
    known_map["c"] = list(set_c)[0]
    known_map["f"] = (cf - set_c).pop()

    set_e = abcdefg - bcdf - abfg
    known_map["e"] = list(set_e)[0]

    acdeg = next(word for word in signal_lens[5] if set_e & word)
    set_b = abcdefg - acdeg - cf
    known_map["b"] = list(set_b)[0]
    known_map["d"] = (bdf - set_b - cf).pop()
    known_map["g"] = abcdefg.difference(known_map.values()).pop()

    return {v: k for k, v in known_map.items()}


def decode_disp(signals: list[str], outputs: list[str]) -> int:
    disp_map = make_map(signals)
    decoded_outputs = [
        digits[frozenset(disp_map[letter] for letter in word)] for word in outputs
    ]
    return int("".join(decoded_outputs))


def part2() -> None:
    data = load_input()
    decoded = [decode_disp(*disp) for disp in data]
    print("Total:", sum(decoded))


if __name__ == "__main__":
    part2()
