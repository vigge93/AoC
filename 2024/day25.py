#!/bin/python
import time
from argparse import ArgumentParser, BooleanOptionalAction
from typing import TypedDict

day = 25
part_1_example_answer: int | None = 3
part_2_example_answer: int | None = None


class DataDict(TypedDict):
    keys: list[list[int]]
    locks: list[list[int]]
    


Data = DataDict


def part_1(data: Data):
    max_height = 7
    s = 0
    for key in data["keys"]:
        for lock in data["locks"]:
            fits = True
            for col in range(len(key)):
                if key[col] + lock[col] > max_height:
                    fits = False
                    break
            if fits:
                s += 1
    return s


def part_2(data: Data):
    pass


def parse_data(file: str):
    data: Data = {"keys": [], "locks": []}
    with open(file, "r") as f:
        i = 0
        key = False
        key_lock: list[int] = []
        for line in f:
            if not line.strip():
                i = 0
                if key:
                    data["keys"].append(key_lock)
                else:
                    data["locks"].append(key_lock)
                key_lock = []
                continue
            if i == 0:
                if line[0] == "#":
                    key = False
                else:
                    key = True
                key_lock = [0] * len(line.strip())
                
            for idx, col in enumerate(line.strip()):
                if col == "#":
                    key_lock[idx] += 1
            i += 1
        if key:
            data["keys"].append(key_lock)
        else:
            data["locks"].append(key_lock)
    print(data)
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
