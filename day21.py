#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
import dataclasses
import itertools
from typing import Iterator


class GameWin(Exception):
    def __str__(self) -> str:
        if len(self.args) == 1:
            return (
                f"Game won by Player {self.args[0].num} with score {self.args[0].score}"
            )


@dataclasses.dataclass
class Player:
    num: int
    position: int
    score: int = 0
    max_score: int = 1000

    def move(self, dist: int) -> None:
        self.position = (self.position + dist) % 10 or 10
        self.score += self.position
        if self.score >= self.max_score:
            raise GameWin(self)


def deterministic_dice() -> Iterator[int]:
    return itertools.cycle(range(1, 101))


def part1(start: list[int]):
    players = [Player(i + 1, v) for i, v in enumerate(start)]
    dice = deterministic_dice()
    rolls = 0

    while True:
        try:
            for player in players:
                rolls += 3
                move = list(itertools.islice(dice, 3))
                player.move(sum(move))
                print(
                    "Player",
                    player.num,
                    "rolls",
                    move,
                    "and moves to space",
                    player.position,
                    "for a total score of",
                    player.score,
                )

        except GameWin as e:
            print(str(e))
            winner = e.args[0]
            break

    loser = [player for player in players if player is not winner][0]
    print("rolls:", rolls, "losing score:", loser.score)
    print("rolls * losing score =", rolls * loser.score)


if __name__ == "__main__":
    part1([5, 9])
