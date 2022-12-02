#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
import collections
import math
from typing import Union, Iterator

SnailfishNum = Union[int, list]
FlatNum = dict[str, tuple[Union[int, str], Union[int, str]]]


def load_input(fn: str = "day18input.txt") -> Iterator[SnailfishNum]:
    with open(fn) as f:
        for line in f:
            # screw it
            yield FlatNum(eval(line.strip()))


def right_of(astr: str, bstr: str) -> bool:
    if astr == bstr:
        return False
    for a, b in zip(astr, bstr):
        if b > a:
            return True
        elif b < a:
            return False
    return False
    # return len(astr) < len(bstr)


def left_of(astr: str, bstr: str) -> bool:
    if astr == bstr:
        return False
    for a, b in zip(astr, bstr):
        if b < a:
            return True
        elif b > a:
            return False
    return False
    # return len(astr) > len(bstr)


class FlatNum(collections.UserDict):
    def __init__(self, num: SnailfishNum = None) -> FlatNum:
        super().__init__()
        if num:
            self.flatten(num)

    def __repr__(self) -> str:
        if self.data:
            return self._itemrepr("")
        return "[]"

    def _itemrepr(self, key: str) -> str:
        item0 = self.data.get(key + "0")
        item1 = self.data.get(key + "1")
        if item0 is None:
            item0 = self._itemrepr(key + "0")
        else:
            item0 = str(item0)

        if item1 is None:
            item1 = self._itemrepr(key + "1")
        else:
            item1 = str(item1)

        return f"[{item0},{item1}]"

    def flatten(self, num: SnailfishNum, pos: str = "") -> None:
        for i, n in enumerate(num):
            if isinstance(n, list):
                self.flatten(n, pos + str(i))
            else:
                self.data[pos + str(i)] = n

    def can_explode(self) -> bool:
        return any(len(k) >= 5 for k in self.data)

    def explode(self):
        keys = sorted(k[:-1] for k in self.data if len(k) >= 5)
        for expl_key in keys:
            if isinstance(self.data[expl_key + "0"], int) and isinstance(
                self.data[expl_key + "1"], int
            ):
                break
        else:
            raise ValueError(self)

        # print(expl_key, self.data)
        try:
            left_key = sorted(
                (k for k in self.data if left_of(expl_key, k)), reverse=True
            )[0]
            self.data[left_key] = self.data[left_key] + self.data[expl_key + "0"]
        except IndexError:
            # print(self.data[expl_key + "0"])
            pass

        try:
            right_key = sorted(k for k in self.data if right_of(expl_key, k))[0]
            self.data[right_key] = self.data[right_key] + self.data[expl_key + "1"]
        except IndexError:
            # print(self.data[expl_key + "1"])
            pass

        self.data[expl_key] = 0
        del self.data[expl_key + "0"]
        del self.data[expl_key + "1"]

    def can_split(self) -> bool:
        return any(v >= 10 for v in self.data.values())

    def split(self):
        split_key, split_val = sorted(
            (t for t in self.data.items() if t[1] >= 10), key=lambda t: t[0]
        )[0]
        val = split_val / 2
        self.data[split_key + "0"] = math.floor(val)
        self.data[split_key + "1"] = math.ceil(val)
        del self.data[split_key]

    def reduce(self):
        while True:
            # print(self)
            if self.can_explode():
                self.explode()
            elif self.can_split():
                self.split()
            else:
                break

    def __add__(self, other: FlatNum) -> FlatNum:
        if other == 0:
            return self
        if not isinstance(other, type(self)):
            return NotImplemented
        res = type(self)()
        for k, v in self.data.items():
            res["0" + k] = v

        for k, v in other.data.items():
            res["1" + k] = v

        res.reduce()
        return res

    def __iadd__(self, other: FlatNum) -> None:
        self.data = self.__add__(other).data

    def __radd__(self, other) -> FlatNum:
        return self.__add__(other)

    def magnitude(self, key: str = "") -> int:
        item0 = self.data.get(key + "0")
        item1 = self.data.get(key + "1")
        if item0 is None:
            item0 = self.magnitude(key + "0")

        if item1 is None:
            item1 = self.magnitude(key + "1")

        return item0 * 3 + item1 * 2


def part1(fn: str = "day18input.txt") -> None:
    total = sum(load_input(fn))
    print(total.magnitude())


def part2(fn: str = "day18input.txt") -> None:
    nums = list(load_input(fn))
    maxmag = max((a + b).magnitude() for a in nums for b in nums if a != b)
    print("Largest magnitude:", maxmag)
