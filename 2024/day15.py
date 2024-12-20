#!/bin/python
import time
from typing import TypedDict
from argparse import ArgumentParser, BooleanOptionalAction
from enum import Enum, auto

day = 15
part_1_example_answer: int | None = 10092
part_2_example_answer: int | None = 9021

class GridObj(Enum):
    WALL = auto()
    CRATE = auto()
    CRATE_L = auto()
    CRATE_R = auto()

class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()
    
direction_map = {
    '^': Direction.UP,
    '>': Direction.RIGHT,
    'v': Direction.DOWN,
    '<': Direction.LEFT,
}

class DataDict(TypedDict):
    grid: dict[tuple[int, int], GridObj]
    moves: list[Direction]
    robot: tuple[int, int]
    
Data = DataDict

def print_grid(data: dict[tuple[int, int], GridObj], robot: tuple[int, int]):
    max_x = max([x for (x, _) in data])
    max_y = max([y for (_, y) in data])
    grid = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for (x, y) in data:
        if data[(x, y)] ==GridObj.WALL:
            grid[y][x] = "#"
        elif data[(x, y)] == GridObj.CRATE:
            grid[y][x] = "O"
        elif data[(x, y)] == GridObj.CRATE_L:
            grid[y][x] = "["
        elif data[(x, y)] == GridObj.CRATE_R:
            grid[y][x] = "]"
    grid[robot[1]][robot[0]] = "@"
    grid = ["".join(row) for row in grid]
    print(*grid, sep="\n")

def part_1(data: Data):
    moves = data["moves"]
    grid = data["grid"].copy()
    robot = data["robot"]
    
    for move in moves:
        (x, y) = robot
        dx, dy = 0, 0
        if move == Direction.UP:
            dy = -1
        elif move == Direction.RIGHT:
            dx = 1
        elif move == Direction.DOWN:
            dy = 1
        elif move == Direction.LEFT:
            dx = -1
        new_robot = (x + dx, y + dy)
        if not new_robot in grid:
            robot = new_robot
            continue
        
        if grid[new_robot] == GridObj.WALL:
            continue

        next_crate = new_robot
        while next_crate in grid and grid[next_crate] == GridObj.CRATE:
            next_crate = (next_crate[0] + dx, next_crate[1] + dy)
        
        if next_crate in grid and grid[next_crate] == GridObj.WALL:
            continue
        
        grid[next_crate] = GridObj.CRATE
        del grid[new_robot]
        robot = new_robot
    s = 0
    for (x, y), obj in grid.items():
        if obj == GridObj.CRATE:
            s += 100*y + x
    return s

def can_push(box: tuple[int, int], dy: int, grid: dict[tuple[int, int], GridObj]) -> bool:
    x, y = box
    y = y + dy
    if (x, y) not in grid:
        return True
    if grid[(x, y)] == GridObj.WALL:
        return False
    if grid[(x, y)] == GridObj.CRATE_R:
        r = can_push((x, y), dy, grid)
        l = can_push((x-1, y), dy, grid)
        return r and l
    if grid[(x, y)] == GridObj.CRATE_L:
        l = can_push((x, y), dy, grid)
        r = can_push((x+1, y), dy, grid)
        return r and l
    return False

def push(box: tuple[int, int], obj: GridObj, dy: int, grid: dict[tuple[int, int], GridObj]):
    x, y = box
    y = y + dy
    if not (x, y) in grid:
        pass
    elif grid[(x, y)] == GridObj.CRATE_R:
        push((x, y), grid[(x, y)], dy, grid)
        push((x-1, y), grid[(x-1, y)], dy, grid)
    elif grid[(x, y)] == GridObj.CRATE_L:
        push((x, y), grid[(x, y)], dy, grid)
        push((x+1, y), grid[(x+1, y)], dy, grid)
    grid[(x, y)] = obj
    del grid[box]
    
def part_2(data: Data):
    moves = data["moves"]
    grid = data["grid"]
    new_grid: dict[tuple[int, int], GridObj] = {}
    robot = data["robot"]
    
    robot = (robot[0] * 2, robot[1])
    for (x, y), obj in grid.items():
        x = 2*x
        if obj == GridObj.WALL:
            new_grid[(x, y)] = obj
            new_grid[(x+1, y)] = obj
        elif obj == GridObj.CRATE:
            new_grid[(x, y)] = GridObj.CRATE_L
            new_grid[(x+1, y)] = GridObj.CRATE_R
    
    grid = new_grid
    for move in moves:
        x, y = robot
        dx, dy = 0, 0
        if move == Direction.UP:
            dy = -1
        elif move == Direction.RIGHT:
            dx = 1
        elif move == Direction.DOWN:
            dy = 1
        elif move == Direction.LEFT:
            dx = -1
        
        new_robot = (x + dx, y + dy)
        if not new_robot in grid:
            robot = new_robot
            continue
        
        if grid[new_robot] == GridObj.WALL:
            continue

        if dy == 0:
            next_crate = new_robot
            while next_crate in grid and grid[next_crate] in (GridObj.CRATE_L, GridObj.CRATE_R):
                next_crate = (next_crate[0] + dx, next_crate[1])
            
            if next_crate in grid and grid[next_crate] == GridObj.WALL:
                continue
            
            while next_crate != new_robot:
                grid[next_crate] = grid[(next_crate[0] - dx, next_crate[1])]
                next_crate = (next_crate[0] - dx, next_crate[1])
            del grid[new_robot]
        else:
            if not can_push(robot, dy, grid):
                continue
            next_crate = new_robot
            next_crate_t = grid[next_crate]
            push(next_crate, next_crate_t, dy, grid)
            if next_crate_t == GridObj.CRATE_R:
                next_crate = (next_crate[0]-1, next_crate[1])
                push(next_crate, grid[next_crate], dy, grid)
            if next_crate_t == GridObj.CRATE_L:
                next_crate = (next_crate[0]+1, next_crate[1])
                push(next_crate, grid[next_crate], dy, grid)
            
        robot = new_robot

    s = 0
    for (x, y), obj in grid.items():
        if obj == GridObj.CRATE_L:
            s += 100*y + x
    return s


def parse_data(file: str):
    data: Data = {"grid": {}, "moves": [], "robot": (-1, -1)}
    grid = True
    with open(file, "r") as f:
        for y, line in enumerate(f):
            if not line.strip():
                grid = False
                continue
            if grid:
                for x, obj in enumerate(line.strip()):
                    if obj == '#':
                        data["grid"][(x, y)] = GridObj.WALL
                    elif obj == 'O':
                        data["grid"][(x, y)] = GridObj.CRATE
                    elif obj == '@':
                        data["robot"] = (x, y)
            else:
                data["moves"].extend([direction_map[d] for d in line.strip()])
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
