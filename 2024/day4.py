#!/bin/python
import time
from typing import TypedDict
from argparse import ArgumentParser, BooleanOptionalAction
from collections import defaultdict

day = 4
part_1_example_answer: int | None = 18
part_2_example_answer: int | None = 9


class DataDict(TypedDict):
    pass
type Data = defaultdict[tuple[int, int], str] # DataDict

chars = ["X", "M", "A", "S"]

def find_m(data: Data, x: int, y: int):
    ms: list[tuple[int, int]] = []
    for y_off in range(-1, 2):
        for x_off in range(-1, 2):
            new_x = x + x_off
            new_y = y + y_off
            if data[(new_x, new_y)] == "M":
                ms.append((x_off, y_off))
    return ms
             
def find_xmas(data: Data, x: int, y: int, char_idx: int, x_off: int, y_off: int) -> int:
    if char_idx == len(chars) - 1:
        return 1
    next_char = chars[char_idx + 1]
    new_x = x + x_off
    new_y = y + y_off
    
    if data[(new_x, new_y)] == next_char:
        return find_xmas(data, new_x, new_y, char_idx + 1, x_off, y_off)

    return 0            


def part_1(data: Data):
    s = 0
    for (x, y), char in dict(data).items():
        if char == "X":
            ms = find_m(data, x, y)
            for x_off, y_off in ms:
                s += find_xmas(data, x + x_off, y + y_off, 1, x_off, y_off)
    return s

def part_2(data: Data):
    s = 0
    x_set = {"S", "M"}
    for (x, y), char in dict(data).items():
        if char == "A":            
            x1_1 = data[(x-1, y-1)]
            x1_2 = data[(x+1, y+1)]
            x2_1 = data[(x+1, y-1)]
            x2_2 = data[(x-1, y+1)]
            if {x1_1, x1_2} == x_set and {x2_1, x2_2} == x_set:
                s += 1
    return s

def parse_data(file: str):
    data: Data = defaultdict(str)
    with open(file, "r") as f:
        for y, line in enumerate(f):
            line = line.strip()
            for x, char in enumerate(line):
                data[(x, y)] = char
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
