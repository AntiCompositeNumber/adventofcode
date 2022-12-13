#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
import itertools
from typing import NamedTuple, Union
from collections.abc import Iterator

PacketList = list[Union["PacketList", int]]


class Packet(PacketList):
    def __lt__(self, other: PacketList) -> bool:
        return bool(compare(self, other))

    def __gt__(self, other: PacketList) -> bool:
        return bool(compare(other, self))


class Pair(NamedTuple):
    left: PacketList
    right: PacketList

    def correct_order(self) -> bool:
        # print(self)
        res = compare(self.left, self.right)
        # print(res, "\n")
        # breakpoint()
        return bool(res)

    def flip(self) -> Pair:
        return self._replace(left=self.right, right=self.left)


def compare(left: PacketList, right: PacketList) -> bool | None:
    for lval, rval in itertools.zip_longest(left, right, fillvalue=-1):
        # no support for PEP 634 in mypy quite yet (next version)
        # print("Compare", lval, "vs", rval)
        match lval, rval:
            case _, -1:
                return False
            case -1, _:
                return True
            case int(), int():
                if lval == rval:
                    continue
                return lval < rval  # type: ignore
            case list(), list():
                res = compare(lval, rval)  # type: ignore
            case list(), int():
                res = compare(lval, [rval])  # type: ignore
            case int(), list():
                res = compare([lval], rval)  # type: ignore
            case _:
                raise TypeError(lval, rval)
        if res is None:
            continue
        else:
            return res
    return None


def load_paired_input(filename: str) -> Iterator[Pair]:
    with open(filename) as f:
        for raw_pair in f.read().split("\n\n"):
            raw_left, raw_right = raw_pair.strip().split("\n")
            yield Pair(Packet(eval(raw_left)), Packet(eval(raw_right)))  # Hush.


def load_full_input(filename: str) -> Iterator[Packet]:
    with open(filename) as f:
        for line in f:
            if line == "\n":
                continue
            yield Packet(eval(line.strip()))  # 🦢👌 Shut.

    yield Packet([[2]])
    yield Packet([[6]])


def main(filename: str = "day13input.txt") -> None:
    part1 = sum(
        i + 1
        for i, pair in enumerate(load_paired_input(filename))
        if pair.correct_order()
    )
    print("PART 1:", part1)

    ordered = sorted(load_full_input(filename))
    part2 = (ordered.index(Packet([[2]])) + 1) * (ordered.index(Packet([[6]])) + 1)
    print("PART 2:", part2)


if __name__ == "__main__":
    main()
