#!/usr/bin/python3
# coding: utf-8
# SPDX-License-Identifier: Apache-2.0

import re
from typing import NamedTuple, Union, cast
from collections.abc import Iterator


class File(NamedTuple):
    name: str
    size: int

    def pprint(self) -> str:
        return f"- {self.name} (file, size={self.size})\n"


class Directory(NamedTuple):
    name: str
    contents: list["BaseFile"]
    parent: Union["Directory", None]

    @property
    def size(self) -> int:
        return sum(file.size for file in self.contents)

    @classmethod
    def new(cls, name: str, parent: Union["Directory", None] = None) -> "Directory":
        return cls(name=name, contents=[], parent=parent)

    def pprint(self) -> str:
        out = f"- {self.name} (dir)\n"
        out += "\n".join(
            "  " + line for item in self.contents for line in item.pprint().splitlines()
        )
        return out

    def find_dir(self, name: str) -> "Directory":
        return next(
            item
            for item in self.contents
            if item.name == name and isinstance(item, Directory)
        )

    def lte_size(self, maxsize: int) -> Iterator[int]:
        for item in self.contents:
            if isinstance(item, Directory):
                if item.size <= maxsize:
                    yield item.size
                yield from item.lte_size(maxsize)

    def gte_size(self, minsize: int) -> Iterator[int]:
        for item in self.contents:
            if isinstance(item, Directory):
                if item.size > minsize:
                    yield item.size
                yield from item.gte_size(minsize)


BaseFile = File | Directory


def load_input(filename: str = "day07input.txt") -> Iterator[str]:
    with open(filename) as f:
        for line in f:
            yield line.strip()


def build_tree(data: Iterator[str]):
    root = Directory.new("/")
    cwd = root
    next(data)  # skip `cd /`
    for line in data:
        if match := re.match(r"\$ cd ([\w.]+)", line):
            if match[1] == "..":
                cwd = cast(Directory, cwd.parent)
            else:
                new_dir = cwd.find_dir(match[1])
                cwd = new_dir
        elif re.match(r"$ ls", line):
            continue
        elif match := re.match(r"(dir|\d+) ([\w.]+)", line):
            if match[1] == "dir":
                new_file: BaseFile = Directory.new(match[2], cwd)
            else:
                new_file = File(match[2], size=int(match[1]))
            cwd.contents.append(new_file)

    return root


def main(filename: str):
    data = load_input(filename)
    root = build_tree(data)
    part1 = sum(root.lte_size(100000))
    print("PART 1:", part1)

    disk_total = 70000000
    update_size = 30000000
    needed_space = update_size - (disk_total - root.size)
    part2 = min(root.gte_size(needed_space))
    print("PART 2:", part2)


if __name__ == "__main__":
    main("day07input.txt")
