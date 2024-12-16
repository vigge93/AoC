import time
from typing import TypedDict
from argparse import ArgumentParser, BooleanOptionalAction
from enum import IntEnum
from typing import Callable
from functools import cache

day = 16
part_1_example_answer: int | None = 11048
part_2_example_answer: int | None = 64

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class DataDict(TypedDict):
    grid: set[tuple[int, int]]
    start: tuple[int, int, int]
    goal: tuple[int, int]
    
Data = DataDict

TURN_COST = 1000
MOVE_COST = 1

def a_star(grid: set[tuple[int, int]], start: tuple[int, int, int], goal: tuple[int, int]):
    open_set = {start}
    closed_set: set[tuple[int, int, int]] = set()
    g_score = {start: 0}
    g_score_open = {start}

    while len(open_set) > 0:
        g_score_get: Callable[[tuple[int, int, int]], int] = g_score.get # type: ignore
        current = min(g_score_open, key=g_score_get)

        if (current[0], current[1]) == goal:
            return g_score[current]
        open_set.remove(current)
        g_score_open.remove(current)
        closed_set.add(current)

        neighbors: set[tuple[int, int, int]] = set()
        cx, cy, _ = current
        if (cx + 1, cy) in grid:
            n = (cx + 1, cy, Direction.RIGHT)
            if n not in closed_set:
                neighbors.add(n)
        if (cx - 1, cy) in grid:
            n = (cx - 1, cy, Direction.LEFT)
            if n not in closed_set:
                neighbors.add(n)
        if (cx, cy + 1) in grid:
            n = (cx, cy + 1, Direction.DOWN)
            if n not in closed_set:
                neighbors.add(n)
        if (cx, cy -1) in grid:
            n = (cx, cy - 1, Direction.UP)
            if n not in closed_set:
                neighbors.add(n)

        for neighbor in neighbors:
            turns = abs(current[2] - neighbor[2]) % 2
            tentative_g_score = g_score[current] + MOVE_COST + TURN_COST*turns

            if neighbor not in g_score \
                    or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score

                open_set.add(neighbor)
                g_score_open.add(neighbor)
    return None

def floodfill_factory(grid: set[tuple[int, int]], max_cost: int):
    visited: dict[tuple[int, int, int], int] = {}

    @cache
    def floodfill(current: tuple[int, int, int], current_cost: int, goal: tuple[int, int]) -> list[list[tuple[int, int]]]:
        if (current[0], current[1]) == goal:
            return [[goal]]
        if current in visited and visited[current] < current_cost:
            return []
        visited[current] = current_cost
        neighbors: list[tuple[int, int, int]] = []
        cx, cy, _ = current
        if (cx + 1, cy) in grid:
            neighbors.append((cx + 1, cy, Direction.RIGHT))
        if (cx - 1, cy) in grid:
            neighbors.append((cx - 1, cy, Direction.LEFT))
        if (cx, cy + 1) in grid:
            neighbors.append((cx, cy + 1, Direction.DOWN))
        if (cx, cy -1) in grid:
            neighbors.append((cx, cy - 1, Direction.UP))
        ret_paths: list[list[tuple[int, int]]] = []
        for neighbor in neighbors:
            turns = (current[2] - neighbor[2]) % 4
            if turns == 2:
                continue
            turns = turns % 2
            move_cost = MOVE_COST + TURN_COST*turns
            if (current_cost + move_cost) > max_cost:
                continue
            paths = floodfill(neighbor, current_cost + move_cost, goal)
            for path in paths:
                ret_paths.append([(current[0], current[1])] + path)
        return ret_paths

    return floodfill
def part_1(data: Data):
    grid = data["grid"]
    goal = data["goal"]
    start = data["start"]
    return a_star(grid, start, goal)

def part_2(data: Data):
    if not p1:
        print("Must run part 1 first!")
        return
    floodfill = floodfill_factory(data["grid"], p1)
    goal = data["goal"]
    start = data["start"]
    
    tiles: set[tuple[int, int]] = set()
    
    paths = floodfill(start, 0, goal)
    for path in paths:
        tiles.update(set(path))
    return len(tiles)

def parse_data(file: str):
    data: Data = {"grid": set(), "start": (-1, -1, -1), "goal": (-1, -1)}
    with open(file, "r") as f:
        for y, line in enumerate(f):
            for x, cell in enumerate(line.strip()):
                if cell != '#':
                    data["grid"].add((x, y))
                if cell == "S":
                    data["start"] = (x, y, Direction.RIGHT)
                if cell == "E":
                    data["goal"] = (x, y)
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
