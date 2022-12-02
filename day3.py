#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from typing import Iterable, Literal, Callable

Bit = Literal[0, 1]


def load_input() -> list[str]:
    with open("day3input.txt") as f:
        return [line.strip() for line in f]


def make_streams(data: list[str]) -> list[list[Bit]]:
    streams = [[int(num[cur], base=2) for num in data] for cur in range(len(data[0]))]
    return streams


def most_common(stream: Iterable[Bit]) -> Bit:
    return int(sum(stream) >= (len(stream) / 2))


def least_common(stream: list[Bit]) -> Bit:
    return most_common(stream) ^ 1


def combine_bits(bits: Iterable[Bit]) -> int:
    # Is this a hack? Yes. Do I care? not really
    return int("".join(str(bit) for bit in bits), base=2)


def bit_filter(data: list[str], streams: list[list[Bit]], condition: Callable) -> int:
    filtered_data = data.copy()
    for bit_pos in range(len(data[0])):
        stream = make_streams(filtered_data)[bit_pos]
        keep_bit = condition(stream)
        filtered_data = [
            num for num in filtered_data if int(num[bit_pos], base=2) == keep_bit
        ]
        if len(filtered_data) == 1:
            return int(filtered_data[0], base=2)
    else:
        raise Exception("ran out of bits")


def main():
    data = load_input()
    streams = make_streams(data)
    gamma = combine_bits(most_common(stream) for stream in streams)
    epsilon = combine_bits(least_common(stream) for stream in streams)
    print("Gamma:", gamma)
    print("Epsilon:", epsilon)
    print("Power:", gamma * epsilon)

    o2 = bit_filter(data, streams, most_common)
    co2 = bit_filter(data, streams, least_common)
    print("O2:", o2)
    print("CO2:", co2)
    print("Life support:", o2 * co2)


if __name__ == "__main__":
    main()
