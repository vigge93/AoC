#!../venv/bin/python
import time
from argparse import ArgumentParser, BooleanOptionalAction
from typing import TypedDict
from functools import cache

day = 7
part_1_example_answer: int | None = 21
part_2_example_answer: int | None = 40


class DataDict(TypedDict):
    tachyon: tuple[int, int]
    splitters: set[tuple[int, int]]

Data = DataDict


def move_tach_p1(tach: tuple[int, int], max_y: int, splitters: set[tuple[int, int]], visited: set[tuple[int, int]]) -> int:
    while tach[1] <= max_y:
        if tach in visited:
            return 1
        visited.add(tach)
        tach = (tach[0], tach[1] + 1)
        if tach in splitters:
            s: int = 0
            s += move_tach_p1((tach[0] - 1, tach[1]), max_y, splitters, visited)
            s += move_tach_p1((tach[0] + 1, tach[1]), max_y, splitters, visited)
            return s
    return 1

def move_tach_p2_factory(max_y: int, splitters: set[tuple[int, int]]):
    @cache
    def move_tach_p2(tach: tuple[int, int]) -> int:
        while tach[1] <= max_y:
            tach = (tach[0], tach[1] + 1)
            if tach in splitters:
                s: int = 0
                s += move_tach_p2((tach[0] - 1, tach[1]))
                s += move_tach_p2((tach[0] + 1, tach[1]))
                return s
        return 1
    return move_tach_p2


def part_1(data: Data):
    max_y = 0
    for splitter in data["splitters"]:
        if splitter[1] > max_y:
            max_y = splitter[1]
    visited: set[tuple[int, int]] = set()
    return move_tach_p1(data["tachyon"], max_y, data["splitters"], visited) - 1


def part_2(data: Data):
    max_y = 0
    for splitter in data["splitters"]:
        if splitter[1] > max_y:
            max_y = splitter[1]
    move_tach_p2 = move_tach_p2_factory(max_y, data["splitters"])
    return move_tach_p2(data["tachyon"])


def parse_data(file: str):
    data: Data = {
        "tachyon": (0, 0),
        "splitters": set()
    }
    with open(file, "r") as f:
        for y, line in enumerate(f):
            for x, cell in enumerate(line.strip()):
                if cell == "S":
                    data["tachyon"] = (x, y)
                elif cell == "^":
                    data["splitters"].add((x, y))
    return data


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--test", action=BooleanOptionalAction, default=False)

    args = parser.parse_args()

    if args.test:
        if part_1_example_answer is not None:  # type: ignore
            data = parse_data(f"day{day}.xexample-1.txt")
            p1 = part_1(data)
            if p1 != part_1_example_answer:
                print(
                    f"Wrong answer to part 1: answer: {p1}, expected: {part_1_example_answer}"
                )
            else:
                print("Example part 1 passed!")
        if part_2_example_answer is not None:  # type: ignore
            data = parse_data(f"day{day}.xexample-2.txt")
            p2 = part_2(data)
            if p2 != part_2_example_answer:
                print(
                    f"Wrong answer to part 2: answer: {p2}, expected: {part_2_example_answer}"
                )
            else:
                print("Example part 2 passed!")
    else:
        start_time = time.perf_counter_ns()
        data = parse_data(f"day{day}.txt")
        data_time = time.perf_counter_ns()
        p1 = part_1(data)
        p1_time = time.perf_counter_ns()
        p2 = part_2(data)
        end_time = time.perf_counter_ns()
        print(
            f"""=== Day {day:02} ===\n"""
            f"""  · Loading data\n"""
            f"""  · Elapsed: {(data_time - start_time)/10**6:.3f} ms\n\n"""
            f"""  · Part 1: {p1}\n"""
            f"""  · Elapsed: {(p1_time - data_time)/10**6:.3f} ms\n\n"""
            f"""  · Part 2: {p2}\n"""
            f"""  · Elapsed: {(end_time - p1_time)/10**6:.3f} ms\n\n"""
            f"""  · Total elapsed: {(end_time - start_time)/10**6:.3f} ms"""
        )
