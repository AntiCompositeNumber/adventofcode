#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

import collections


def load_input(filename: str = "day06input.txt") -> str:
    with open(filename) as f:
        for line in f:
            return line.strip()


def check_marker(stream: str, marker_len: int) -> int:
    buffer = collections.deque()
    for i, char in enumerate(stream):
        buffer.append(char)
        if len(buffer) > marker_len:
            buffer.popleft()
        if len(buffer) == marker_len and len(set(buffer)) == marker_len:
            return i + 1
    raise ValueError


def main() -> None:
    data = load_input()
    packet_marker = check_marker(data, marker_len=4)
    print("PART 1:", packet_marker)

    message_marker = check_marker(data, marker_len=14)
    print("PART 2:", message_marker)


if __name__ == "__main__":
    main()
