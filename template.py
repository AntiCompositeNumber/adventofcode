#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0


def load_input(filename: str = "input.txt"):
    with open(filename) as f:
        for line in f:
            yield line.strip()


def main():
    ...


if __name__ == "__main__":
    main()
