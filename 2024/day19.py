#!/bin/pypy3
import time
from argparse import ArgumentParser, BooleanOptionalAction
from functools import cache
from typing import TypedDict

day = 19
part_1_example_answer: int | None = 6
part_2_example_answer: int | None = 16


class DataDict(TypedDict):
    towels: list[str]
    designs: list[str]


Data = DataDict


def factory(towels: list[str]):
    @cache
    def design_possible(design: str) -> int:
        if not design:
            return 1
        s = 0
        for towel in towels:
            if design.startswith(towel):
                s += design_possible(design.removeprefix(towel))
        return s

    return design_possible


def part_1_and_2(data: Data):
    s1 = 0
    s2 = 0
    design_possible = factory(data["towels"])
    for design in data["designs"]:
        designs = design_possible(design)
        if designs:
            s1 += 1
            s2 += designs
    return s1, s2


def parse_data(file: str):
    data: Data = {"designs": [], "towels": []}
    with open(file, "r") as f:
        data["towels"] = f.readline().strip().split(", ")
        f.readline()
        for line in f:
            data["designs"].append(line.strip())
    return data


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--test", action=BooleanOptionalAction, default=False)

    args = parser.parse_args()

    if args.test:
        if part_1_example_answer is not None or part_2_example_answer is not None:  # type: ignore
            data = parse_data(f"day{day}.xexample-1-and-2.txt")
            p1, p2 = part_1_and_2(data)
            if p1 != part_1_example_answer:
                print(
                    f"Wrong answer to part 1: answer: {p1}, expected: {part_1_example_answer}"
                )
            else:
                print("Example part 1 passed!")
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
        p1, p2 = part_1_and_2(data)
        end_time = time.perf_counter_ns()
        print(
            f"""=== Day {day:02} ===\n"""
            f"""  · Loading data\n"""
            f"""  · Elapsed: {(data_time - start_time)/10**6:.3f} ms\n\n"""
            f"""  · Part 1: {p1}\n"""
            f"""  · Elapsed: {(end_time - data_time)/10**6:.3f} ms\n\n"""
            f"""  · Part 2: {p2}\n"""
            f"""  · Elapsed: 0 ms\n\n"""
            f"""  · Total elapsed: {(end_time - start_time)/10**6:.3f} ms"""
        )
