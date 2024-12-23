#!/bin/python
import time
from argparse import ArgumentParser, BooleanOptionalAction
from typing import TypedDict

day = 18
part_1_example_answer: int | None = 22
part_2_example_answer: tuple[int, int] | None = (6, 1)


class DataDict(TypedDict):
    pass


Data = list[tuple[int, int]]  # DataDict

testing = False


def a_star(grid: set[tuple[int, int]], start: tuple[int, int], goal: tuple[int, int]):
    open_set = {start}
    closed_set: set[tuple[int, int]] = set()
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    g_score = {start: 0}
    g_score_open = {start}

    while len(open_set) > 0:
        g_score_get: Callable[[tuple[int, int]], int] = g_score.get  # type: ignore
        current = min(g_score_open, key=g_score_get)

        if current == goal:
            return g_score[current], reconstruct_path(came_from, goal)
        open_set.remove(current)
        g_score_open.remove(current)
        closed_set.add(current)

        neighbors: set[tuple[int, int]] = set()
        cx, cy = current
        if (cx + 1, cy) in grid:
            n = (cx + 1, cy)
            if n not in closed_set:
                neighbors.add(n)
        if (cx - 1, cy) in grid:
            n = (cx - 1, cy)
            if n not in closed_set:
                neighbors.add(n)
        if (cx, cy + 1) in grid:
            n = (cx, cy + 1)
            if n not in closed_set:
                neighbors.add(n)
        if (cx, cy - 1) in grid:
            n = (cx, cy - 1)
            if n not in closed_set:
                neighbors.add(n)

        for neighbor in neighbors:
            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                came_from[neighbor] = current

                open_set.add(neighbor)
                g_score_open.add(neighbor)
    return None


def reconstruct_path(
    came_from: dict[tuple[int, int], tuple[int, int]], goal: tuple[int, int]
):
    path = [goal]
    current = goal
    while current in came_from:
        current = came_from[current]
        path.insert(0, current)
    return path


def part_1(data: Data) -> int:
    grid_size = 70
    steps = 1024
    if testing:
        grid_size = 6
        steps = 12
    grid = {(x, y) for x in range(grid_size + 1) for y in range(grid_size + 1)}
    for byte in data[:steps]:
        grid.remove(byte)
    return a_star(grid, (0, 0), (grid_size, grid_size))[0]


def part_2(data: Data):
    grid_size = 70
    steps = 1024
    if testing:
        grid_size = 6
        steps = 12
    goal = (grid_size, grid_size)
    grid = {(x, y) for x in range(grid_size + 1) for y in range(grid_size + 1)}
    for byte in data[:steps]:
        grid.remove(byte)
    r = a_star(grid, (0, 0), goal)
    if not r:
        return -1
    _, path = r
    path_set = set(path)
    for byte in data[steps:]:
        grid.remove(byte)
        if byte in path_set:
            blocked_idx = path.index(byte)
            start = path[blocked_idx - 1]
            res = a_star(grid, start, goal)
            if not res:
                return byte
            _, new_path = res
            path_set.difference_update(path[blocked_idx:])
            path_set.update(new_path)
            path = path[: blocked_idx - 1] + new_path
    return -1


def parse_data(file: str):
    data: Data = []
    with open(file, "r") as f:
        for line in f:
            data.append(tuple([int(x) for x in line.strip().split(",")]))  # type: ignore
    return data


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--test", action=BooleanOptionalAction, default=False)

    args = parser.parse_args()

    if args.test:
        testing = True
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
