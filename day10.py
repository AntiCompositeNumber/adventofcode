#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

import dataclasses
from collections.abc import Iterator


@dataclasses.dataclass
class CPU:
    x: int = 1
    counter: int = 0
    strengths: list[int] = dataclasses.field(default_factory=list)
    output: str = ""

    def execute(self, instruction: str) -> None:
        self.cycle()

        # Execute new instruction
        match instruction.split():
            case ["noop"]:
                return
            case ["addx", val]:
                self.cycle()
                self.x += int(val)
            case _:
                raise ValueError(instruction)

    def cycle(self) -> None:
        self.counter += 1

        if (self.counter - 20) % 40 == 0:
            self.monitor_signal_strength()

        self.draw_pixel()

    def monitor_signal_strength(self) -> None:
        self.strengths.append(self.x * self.counter)

    def draw_pixel(self) -> None:
        visible_pixels = [self.x - 1, self.x, self.x + 1]
        cur_pixel = (self.counter - 1) % 40
        if cur_pixel in visible_pixels:
            self.output += "\u2588"
        else:
            self.output += " "

        if cur_pixel == 39:
            self.output += "\n"


def load_input(filename: str) -> Iterator[str]:
    with open(filename) as f:
        for line in f:
            yield line.strip()


def main(filename: str = "day10input.txt"):
    cpu = CPU()
    for line in load_input(filename):
        cpu.execute(line)

    print("PART 1:", sum(cpu.strengths))
    print("PART 2:")
    print(cpu.output)


if __name__ == "__main__":
    main()
