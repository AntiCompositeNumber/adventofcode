#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from enum import IntEnum
from typing import NamedTuple


class Shape(IntEnum):
    ROCK = 1
    A = 1
    X = 1
    PAPER = 2
    B = 2
    Y = 2
    SCISSORS = 3
    C = 3
    Z = 3

    def loses_against(self, other: "Shape") -> bool:
        cls = type(self)
        if self is other:
            return False
        elif self is cls.ROCK:
            return other is cls.PAPER
        elif self is cls.PAPER:
            return other is cls.SCISSORS
        elif self is cls.SCISSORS:
            return other is cls.ROCK
        return NotImplemented

    def wins_against(self, other: "Shape") -> bool:
        if self is other:
            return False
        else:
            return not self.loses_against(other)


class Result(IntEnum):
    LOSS = 0
    X = 0
    DRAW = 3
    Y = 3
    WIN = 6
    Z = 6


class Round(NamedTuple):
    opponent: Shape
    player: Shape

    def result(self) -> Result:
        if self.opponent == self.player:
            return Result.DRAW
        elif self.opponent.loses_against(self.player):
            return Result.WIN
        else:
            return Result.LOSS

    def score(self) -> int:
        return self.player + self.result()

    @classmethod
    def from_line(cls, line: str) -> "Round":
        opponent, _, player = line.strip().partition(" ")
        return cls(opponent=getattr(Shape, opponent), player=getattr(Shape, player))


class ResultRound(NamedTuple):
    opponent: Shape
    result: Result

    def player(self) -> Shape:
        if self.result is Result.DRAW:
            return self.opponent

        for shape in [Shape.ROCK, Shape.PAPER, Shape.SCISSORS]:
            if self.result is Result.WIN:
                if shape.wins_against(self.opponent):
                    return shape
            else:
                if shape.loses_against(self.opponent):
                    return shape

    def score(self) -> int:
        return self.player() + self.result

    @classmethod
    def from_line(cls, line: str) -> "ResultRound":
        opponent, _, result = line.strip().partition(" ")
        return cls(opponent=getattr(Shape, opponent), result=getattr(Result, result))


def test():
    testdata = [
        (Round(Shape.ROCK, Shape.ROCK), 3 + 1),
        (Round(Shape.PAPER, Shape.ROCK), 0 + 1),
        (Round(Shape.SCISSORS, Shape.ROCK), 6 + 1),
        (Round(Shape.ROCK, Shape.PAPER), 6 + 2),
        (Round(Shape.PAPER, Shape.PAPER), 3 + 2),
        (Round(Shape.SCISSORS, Shape.PAPER), 0 + 2),
        (Round(Shape.ROCK, Shape.SCISSORS), 0 + 3),
        (Round(Shape.PAPER, Shape.SCISSORS), 6 + 3),
        (Round(Shape.SCISSORS, Shape.SCISSORS), 3 + 3),
    ]
    for r, score in testdata:
        if r.score() != score:
            print(r, r.score(), score)


def test_resultround_player():
    for shape in [Shape.ROCK, Shape.PAPER, Shape.SCISSORS]:
        for result in [Result.WIN, Result.DRAW, Result.LOSS]:
            print(shape, result, ResultRound(shape, result).player())


def main():
    part1 = [Round.from_line(line) for line in load_input()]
    total = sum(r.score() for r in part1)
    print("PART 1: Total score:", total)

    part2 = [ResultRound.from_line(line) for line in load_input()]
    total2 = sum(r.score() for r in part2)
    print("PART 2: Total score:", total2)


def load_input():
    with open("day02input.txt") as f:
        yield from f


if __name__ == "__main__":
    pass
