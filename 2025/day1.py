#!/bin/python
import time
from argparse import ArgumentParser, BooleanOptionalAction
from typing import TypedDict

day = 1
part_1_example_answer: int | None = 3
part_2_example_answer: int | None = 6


class DataDict(TypedDict):
    pass


Data = list  # DataDict


def part_1(data: Data):
    s = 50
    n_zero = 0
    for line in data:
        s += line[0] * line[1]
        s = s % 100
        if s == 0:
            n_zero += 1
    return n_zero


def part_2(data: Data):
    s = 50
    n_zero = 0
    for line in data:
        rot = line[1]
        min_zeros = rot // 100
        rot = rot % 100
        s += line[0] * rot
        if (s <= 0 or s >= 100) and abs(s) != rot:
            n_zero += 1
        n_zero += min_zeros
        s = s % 100
    return n_zero


def parse_data(file: str):
    data: Data = []
    with open(file, "r") as f:
        for line in f:
            if line[0] == "L":
                data.append((-1, int(line[1:])))
            else:
                data.append((1, int(line[1:])))
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
