#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations


def load_input(filename: str):
    with open(filename) as f:
        for line in f:
            yield line.strip()


def main(filename: str = "input.txt") -> None:
    ...


if __name__ == "__main__":
    main()
