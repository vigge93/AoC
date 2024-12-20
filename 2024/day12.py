#!/bin/python
import time
from typing import TypedDict
from argparse import ArgumentParser, BooleanOptionalAction
from collections import defaultdict

day = 12
part_1_example_answer: int | None = 1930
part_2_example_answer: int | None = 1206


class DataDict(TypedDict):
    pass
Data = dict[tuple[int, int], str] # DataDict

def floodfill(grid: Data, current: tuple[int, int], visited: set[tuple[int, int]]):
    visited.add(current)
    for i in (-1, 1):
        node = (current[0] + i, current[1])
        if node in grid and grid[current] == grid[node] and node not in visited:
            visited.update(floodfill(grid, node, visited))
        node = (current[0], current[1]+i)
        if node in grid and grid[current] == grid[node] and node not in visited:
            visited.update(floodfill(grid, node, visited))
    return visited

regions: list[set[tuple[int, int]]] = []

def part_1(data: Data):
    regions: list[set[tuple[int, int]]] = []
    candidates = data.copy()
    while candidates:
        candidate = next(iter(candidates.keys()))
        region = floodfill(data, candidate, set())
        for field in region:
            del candidates[field]
        regions.append(region)
    s = 0
    for region in regions:
        area = len(region)
        perimeter = area*4
        for field in region:
            for off in (-1, 1):
                if (field[0] + off, field[1]) in region:
                    perimeter -= 1
                if (field[0], field[1] + off) in region:
                    perimeter -= 1
        s += area * perimeter
    return s

def part_2(data: Data):
    regions: list[set[tuple[int, int]]] = []
    candidates = data.copy()
    while candidates:
        candidate = next(iter(candidates.keys()))
        region = floodfill(data, candidate, set())
        for field in region:
            del candidates[field]
        regions.append(region)
    s = 0
    for region in regions:
        area = len(region)
        perimeters: defaultdict[int, set[tuple[int, int]]] = defaultdict(set)
        tot_perimeter = 0
        for field in region:
            for off in (-1, 1):
                if (field[0] + off, field[1]) not in region:
                    new = True
                    for n in (-1, 1):
                        if (field[0] + off, field[1] + n) in perimeters[off + 1]:
                            if new:
                                new = False
                            else:
                                tot_perimeter -= 1
                    if new:
                        tot_perimeter += 1
                    perimeters[off + 1].add((field[0] + off, field[1]))
                if (field[0], field[1] + off) not in region:
                    new = True
                    for n in (-1, 1):
                        if (field[0] + n, field[1] + off) in perimeters[off]:
                            if new:
                                new = False
                            else:
                                tot_perimeter -= 1
                    if new:
                        tot_perimeter += 1
                    perimeters[off].add((field[0], field[1] + off))
        s += area*tot_perimeter
    return s

def parse_data(file: str):
    data: Data = {}
    with open(file, "r") as f:
        for y, line in enumerate(f):
            for x, field in enumerate(line.strip()):
                data[(x, y)] = field
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
