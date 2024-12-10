import time
from typing import TypedDict
from argparse import ArgumentParser, BooleanOptionalAction
from functools import cache


day = 10
part_1_example_answer: int | None = 36
part_2_example_answer: int | None = 81


class DataDict(TypedDict):
    grid: dict[tuple[int, int], int]
    heads: set[tuple[int, int]]
    tails: set[tuple[int, int]]
Data = DataDict

def floodfill_factory(grid: dict[tuple[int, int], int]):

    @cache
    def floodfill(current: tuple[int, int], goal: tuple[int, int]) -> int:
        if current == goal:
            return 1
        s = 0
        for i in (-1, 1):
            node = (current[0] + i, current[1])
            if node in grid and grid[current] == grid[node] - 1:
                s += floodfill(node, goal)
            node = (current[0], current[1]+i)
            if node in grid and grid[current] == grid[node] - 1:
                s += floodfill(node, goal)
        return s

    return floodfill

def part_1(data: Data):
    s = 0
    for head in data["heads"]:
        for tail in data["tails"]:
            if ffill(head, tail):
                s += 1
    return s

def part_2(data: Data):
    s = 0
    for head in data["heads"]:
        for tail in data["tails"]:
            s += ffill(head, tail)
    return s


def parse_data(file: str):
    data: Data = {"grid": {}, "heads": set(), "tails": set()}
    with open(file, "r") as f:
        for y, line in enumerate(f):
            for x, pos in enumerate(line.strip()):
                data["grid"][(x, y)] = int(pos)
                if int(pos) == 0:
                    data["heads"].add((x, y))
                if int(pos) == 9:
                    data["tails"].add((x, y))
    global ffill
    ffill = floodfill_factory(data["grid"])
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
