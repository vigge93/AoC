#!/bin/pypy3
import time
from typing import TypedDict
from argparse import ArgumentParser, BooleanOptionalAction
import re

day = 14
part_1_example_answer: int | None = 12
part_2_example_answer: int | None = None

testing = False

class DataDict(TypedDict):
    pass
Data = set[tuple[tuple[int, int], tuple[int, int]]] # DataDict

def print_grid(data: Data):
    max_x = max([x for (x, _), _ in data])
    max_y = max([y for (_, y), _ in data])
    grid = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for (x, y), _ in data:
        grid[y][x] = "#"
    grid = ["".join(row) for row in grid]
    print(*grid, sep="\n")

def part_1(data: Data):
    w = 101
    h = 103
    if testing:
        w = 11
        h = 7
    steps = 100
    current_positions = data
    for _ in range(steps):
        new_positions: Data = set()
        for (x, y), (vx, vy) in current_positions:
            new_x = (x + vx) % w
            new_y = (y + vy) % h
            new_positions.add(((new_x, new_y), (vx, vy)))
        current_positions = new_positions
    q1, q2, q3, q4 = 0, 0, 0, 0
    for (x, y), _ in current_positions:
        if x < w // 2:
            if y < h // 2:
                q1 += 1
            if y > h // 2:
                q2 += 1
        if x > w // 2:
            if y < h // 2:
                q3 += 1
            if y > h // 2:
                q4 += 1
    return q1*q2*q3*q4

def part_2(data: Data):
    w = 101
    h = 103
    current_positions = data
    i = 0
    new_coords: set[tuple[int, int]] = set()
    while True:
        i += 1
        new_positions: Data = set()
        new_coords.clear()
        for (x, y), (vx, vy) in current_positions:
            new_x = (x + vx) % w
            new_y = (y + vy) % h
            new_positions.add(((new_x, new_y), (vx, vy)))
            new_coords.add((new_x, new_y))
        current_positions = new_positions
        candidate_cnt = 0
        for (x, y), _ in current_positions:
            if (x + 1, y) not in new_coords:
                continue
            if (x - 1, y) not in new_coords:
                continue
            if (x, y + 1) not in new_coords:
                continue
            if (x, y - 1) not in new_coords:
                continue
            candidate_cnt += 1
            if candidate_cnt > 3:
                break
        if candidate_cnt > 3:
            print_grid(current_positions)
            return i


def parse_data(file: str):
    data: Data = set()
    with open(file, "r") as f:
        for line in f:
            x, y, vx, vy = [int(n) for n in re.findall(r"-?\d+", line)]
            data.add(((x, y), (vx, vy)))
    return data


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--test", action=BooleanOptionalAction, default=False)
    
    args = parser.parse_args()
    
    if args.test:
        testing = True
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
