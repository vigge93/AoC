import time
from typing import TypedDict
from argparse import ArgumentParser, BooleanOptionalAction
from enum import IntEnum
from collections import defaultdict
from copy import deepcopy
from tqdm import tqdm

day = 6
part_1_example_answer: int | None = 41
part_2_example_answer: int | None = 6


class DataDict(TypedDict):
    grid: dict[tuple[int, int], str]
    guard: tuple[int, int]


class Dir(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

def part_1(data):
    grid = data["grid"]
    guard = data["guard"]
    visited: set[tuple[int, int]] = set()
    direction = Dir.NORTH
    while guard in grid:
        visited.add(guard)
        step_x, step_y = direction_mapping[direction]
        next_pos = (guard[0] + step_x, guard[1] + step_y)
        if next_pos in grid and grid[next_pos] == "#":
            direction = Dir((direction + 1) % 4)
        else:
            guard = next_pos
    return len(visited)

def part_2(data):    
    grid = data["grid"]
    guard = data["guard"]
    visited: set[tuple[int, int]] = set()
    direction = Dir.NORTH
    while guard in grid:
        visited.add(guard)
        step_x, step_y = direction_mapping[direction]
        next_pos = (guard[0] + step_x, guard[1] + step_y)
        if next_pos in grid and grid[next_pos] == "#":
            direction = Dir((direction + 1) % 4)
        else:
            guard = next_pos
    
    s = 0
    for block in tqdm(visited):
        guard = data["guard"]
        changed = False
        if block != guard and grid[block] != "#":
            changed = True
            grid[block] = "#"
        visited: defaultdict[tuple[int, int], set[int]] = defaultdict(set)
        direction = Dir.NORTH
        while guard in grid:
            if direction in visited[guard]:
                s += 1
                break
            visited[guard].add(direction)
            step_x, step_y = direction_mapping[direction]
            next_pos = (guard[0] + step_x, guard[1] + step_y)
            if next_pos in grid and grid[next_pos] == "#":
                direction = Dir((direction + 1) % 4)
            else:
                guard = next_pos
        if changed:
            grid[block] = "."
    return s

direction_mapping = {
    Dir.NORTH: (0, -1),
    Dir.EAST: (1, 0),
    Dir.SOUTH: (0, 1),
    Dir.WEST: (-1, 0)
}

def parse_data(file: str):
    data = {"grid": {}, "guard": (-1, -1)}
    with open(file, "r") as f:
        for y, line in enumerate(f):
            for x, pos in enumerate(line.strip()):
                if pos == "^":
                    data["guard"] = (x, y)
                    data["grid"][(x, y)] = "."
                else:
                    data["grid"][(x, y)] = pos
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
