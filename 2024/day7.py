#!/bin/pypy3
import time
from argparse import ArgumentParser, BooleanOptionalAction
from typing import Callable, TypedDict

day = 7
part_1_example_answer: int | None = 3749
part_2_example_answer: int | None = 11387


class DataDict(TypedDict):
    pass


Data = list[tuple[int, list[int]]]


def operator_search_factory(operations: list[Callable[[int, int], int]]):

    def find_operators(val: int, operators: list[int], target: int) -> bool:
        if not operators:
            return val == target
        next_val = operators[0]
        for operation in operations:
            v = operation(val, next_val)
            if v <= target:
                res = find_operators(v, operators[1:], target)
                if res:
                    return res
        return False

    return find_operators


def part_1(data: Data):
    s = 0
    add: Callable[[int, int], int] = lambda x, y: x + y
    mul: Callable[[int, int], int] = lambda x, y: x * y
    for calibration in data:
        target, operators = calibration
        checker = operator_search_factory([add, mul])
        valid = checker(operators[0], operators[1:], target)
        if valid:
            s += target
    return s


def part_2(data: Data):
    s = 0
    add: Callable[[int, int], int] = lambda x, y: x + y
    mul: Callable[[int, int], int] = lambda x, y: x * y
    concat: Callable[[int, int], int] = lambda x, y: int(str(x) + str(y))
    for calibration in data:
        target, operators = calibration
        checker = operator_search_factory([add, mul, concat])
        valid = checker(operators[0], operators[1:], target)
        if valid:
            s += target
    return s


def parse_data(file: str):
    data: Data = []
    with open(file, "r") as f:
        for line in f:
            target, operators_s = line.strip().split(":")
            operators = [int(x) for x in operators_s.split()]
            data.append((int(target), operators))
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
