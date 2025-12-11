#!../venv/bin/python
from functools import cache
import time
from argparse import ArgumentParser, BooleanOptionalAction
from typing import TypedDict

day = 11
part_1_example_answer: int | None = 5
part_2_example_answer: int | None = 2


class DataDict(TypedDict):
    pass


Data = dict[str, set[str]]  # DataDict


def find_paths_factory(data: Data):
    @cache
    def find_paths(current: str, goal: str, required: frozenset[str]) -> int:
        if current == goal:
            if required:
                return 0
            return 1
        s = 0
        for next in data[current]:
            s += find_paths(next, goal, required - {next})
        return s

    return find_paths

def part_1(data: Data):
    find_paths = find_paths_factory(data)
    return find_paths("you", "out", frozenset())


def part_2(data: Data):
    find_paths = find_paths_factory(data)
    return find_paths("svr", "out", frozenset({"fft", "dac"}))


def parse_data(file: str):
    data: Data = {}
    with open(file, "r") as f:
        for line in f:
            i, o = line.split(":")
            o = o.split()
            data[i] = set(o)
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
