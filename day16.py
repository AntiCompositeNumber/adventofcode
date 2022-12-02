#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
import dataclasses
import math


@dataclasses.dataclass
class Packet:
    version: int
    type_id: int
    data: list = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Literal(Packet):
    data: list[int] = dataclasses.field(default_factory=list)

    def __index__(self) -> int:
        num = 0
        for word in self.data:
            num = (num << 4) + word
        return num


@dataclasses.dataclass
class Operator(Packet):
    length_type: int = -1
    data: list[Packet] = dataclasses.field(default_factory=list)

    def __index__(self) -> int:
        if self.type_id == 0:
            return sum(map(int, self.data))
        elif self.type_id == 1:
            return math.prod(map(int, self.data))
        elif self.type_id == 2:
            return min(map(int, self.data))
        elif self.type_id == 3:
            return max(map(int, self.data))
        elif self.type_id == 5:
            assert len(self.data) == 2
            return int(int(self.data[0]) > int(self.data[1]))
        elif self.type_id == 6:
            assert len(self.data) == 2
            return int(int(self.data[0]) < int(self.data[1]))
        elif self.type_id == 7:
            assert len(self.data) == 2
            return int(int(self.data[0]) == int(self.data[1]))
        raise NotImplementedError


def load_input() -> tuple[int, int]:
    with open("day16input.txt") as f:
        p = next(f).strip()
        return int(p, base=16), len(p) * 4


def make_packet(raw_packet: int, packet_len: int) -> tuple[Packet, int]:
    bit_pos = 3
    version = (raw_packet >> (packet_len - bit_pos)) & 0b111

    bit_pos += 3
    type_id = (raw_packet >> (packet_len - bit_pos)) & 0b111

    if type_id == 4:
        packet = Literal(version=version, type_id=type_id)
        while packet_len > bit_pos:
            bit_pos += 5
            word = (raw_packet >> (packet_len - bit_pos)) & 0b11111
            packet.data.append(word & 0b01111)
            if not word & 0b10000:
                break
    else:
        bit_pos += 1
        packet = Operator(version=version, type_id=type_id)
        packet.length_type = (raw_packet >> (packet_len - bit_pos)) & 0b1

        if packet.length_type == 0:
            bit_pos += 15
            subpacket_len = (raw_packet >> (packet_len - bit_pos)) & (2 ** 15 - 1)
            while bit_pos < packet_len:
                tail = (raw_packet >> (packet_len - bit_pos - subpacket_len)) & (
                    2 ** subpacket_len - 1
                )
                if not tail:
                    break
                subpacket, offset = make_packet(tail, subpacket_len)
                bit_pos += offset
                subpacket_len = subpacket_len - offset
                packet.data.append(subpacket)
        else:
            bit_pos += 11
            subpacket_count = (raw_packet >> (packet_len - bit_pos)) & (2 ** 11 - 1)
            for i in range(subpacket_count):
                tail = raw_packet & (2 ** (packet_len - bit_pos) - 1)
                if not tail:
                    break
                subpacket, offset = make_packet(tail, packet_len - bit_pos)
                bit_pos += offset
                packet.data.append(subpacket)

    return packet, bit_pos


def version_sum(packet: Packet) -> int:
    if isinstance(packet, Literal):
        return packet.version
    else:
        return sum(version_sum(subpacket) for subpacket in packet.data) + packet.version


def part1() -> None:
    raw_packet, packet_len = load_input()
    packet, offset = make_packet(raw_packet, packet_len)

    all_versions = version_sum(packet)
    print("Version sum:", all_versions)


def part2() -> None:
    raw_packet, packet_len = load_input()
    packet, offset = make_packet(raw_packet, packet_len)
    print("Value:", int(packet))
