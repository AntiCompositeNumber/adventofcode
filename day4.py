#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0


class Board(list):
    def match_call(self, call: int) -> None:
        for row in self:
            try:
                i = row.index(call)
            except ValueError:
                continue
            row[i] = -1

    def has_win(self) -> bool:
        # check the rows first, that's easy
        for row in self:
            if row.count(-1) == len(row):
                return True

        # now check the columns
        columns = len(self)
        for col in range(columns):
            if [row[col] for row in self].count(-1) == columns:
                return True

        return False

    def get_score(self, call: int) -> int:
        tot = sum(val for row in self for val in row if val >= 0)
        return tot * call

    def __repr__(self) -> str:
        return "\n".join(
            " ".join(f"{val:2}" if val > -1 else "XX" for val in row) for row in self
        )


def load_data() -> tuple[list[int], list[Board]]:
    with open("day4input.txt") as f:
        calls = [int(call.strip()) for call in next(f).split(",")]
        next(f)
        boards = []
        board = Board()
        for line in f:
            if board and line == "\n":
                # finished parsing a board
                boards.append(board)
                board = Board()
                continue
            row = [int(num.strip()) for num in line.split(" ") if num]
            board.append(row)
        boards.append(board)

        return calls, boards


def part_1():
    calls, boards = load_data()
    print("ROUNDS:", len(calls))
    for i, call in enumerate(calls):
        for board in boards:
            board.match_call(call)
            if board.has_win():
                print("ROUND", i + 1, "WINNER:", board.get_score(call))
                return


def part_2():
    calls, boards = load_data()
    for i, call in enumerate(calls):
        print(f"Round {i+1}: {len(boards)} boards, call: {call}")
        # if i == 13:
        #     breakpoint()
        for board in boards.copy():
            board.match_call(call)
            print(board, "\n")
            if board.has_win():
                boards.remove(board)
                if not boards:
                    print("ROUND", i + 1, "LOSER:", board.get_score(call))
                    return


if __name__ == "__main__":
    part_1()
    part_2()
