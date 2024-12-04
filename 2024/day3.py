import time
from typing import TypedDict
from argparse import ArgumentParser, BooleanOptionalAction
import re

day = 3
part_1_example_answer: int | None = 161
part_2_example_answer: int | None = 48


class DataDict(TypedDict):
    pass
type Data = str # DataDict


def part_1(data: Data):
    s = 0
    for match in re.finditer(r"mul\(([0-9]+),([0-9]+)\)", data):
        s += int(match[1])*int(match[2])
    return s


def part_2(data: Data):
    s = 0
    enabled = True
    for match in re.finditer(r"(?:do\(\)|don't\(\)|mul\(([0-9]+),([0-9]+)\))", data):
        if match[0] == "don't()":
            enabled = False
        elif match[0] == "do()":
            enabled = True
        elif enabled:
            s += int(match[1])*int(match[2])
    return s


def parse_data(file: str):
    data: Data = ""
    with open(file, "r") as f:
        data = f.read()
    return data


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--test", action=BooleanOptionalAction, default=False)
    
    args = parser.parse_args()
    
    if args.test:
        if part_1_example_answer is not None: # type: ignore
            data = parse_data(f"day{day}.xexample-1.txt")
            p1 = part_1(data)
            if p1 != part_1_example_answer:
                print(f"Wrong answer to part 1: answer: {p1}, expected: {part_1_example_answer}")
            else:
                print("Example part 1 passed!")
        if part_2_example_answer is not None: # type: ignore
            data = parse_data(f"day{day}.xexample-2.txt")
            p2 = part_2(data)
            if p2 != part_2_example_answer:
                print(f"Wrong answer to part 2: answer: {p2}, expected: {part_2_example_answer}")
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
