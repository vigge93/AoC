import time
from dataclasses import dataclass
from copy import deepcopy

day = 14

@dataclass
class Rock:
    type: str
    x: int
    y: int
    
def print_grid(data):
    max_x = max([x for x, y in data])
    max_y = max([y for x, y in data])
    grid = [['.' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for (x, y), rock in data.items():
        grid[y][x] = rock
    grid = [''.join(row) for row in grid]
    print(*grid, sep='\n')

def roll_north(data):
    for (x, y), rock in sorted(data.copy().items()):
        if rock == '#':
            continue
        collision = False
        for prev_y in range(y - 1, -1, -1):
            if (x, prev_y) in data:
                del data[(x, y)]
                data[(x, prev_y + 1)] = rock
                collision = True
                break
        if not collision:
            del data[(x, y)]
            data[(x, 0)] = rock
            
def roll_south(data, max_y):
    for (x, y), rock in sorted(data.copy().items(), reverse=True):
        if rock == '#':
            continue
        collision = False
        for prev_y in range(y+1, max_y + 1):
            if (x, prev_y) in data:
                del data[(x, y)]
                data[(x, prev_y - 1)] = rock
                collision = True
                break
        if not collision:
            del data[(x, y)]
            data[(x, max_y)] = rock

def roll_west(data):
    for (x, y), rock in sorted(data.copy().items()):
        if rock == '#':
            continue
        collision = False
        for prev_x in range(x - 1, -1, -1):
            if (prev_x, y) in data:
                del data[(x, y)]
                data[(prev_x + 1, y)] = rock
                collision = True
                break
        if not collision:
            del data[(x, y)]
            data[(0, y)] = rock

def roll_east(data, max_x):
    for (x, y), rock in sorted(data.copy().items(), reverse=True):
        if rock == '#':
            continue
        collision = False
        for prev_x in range(x + 1, max_x + 1):
            if (prev_x, y) in data:
                del data[(x, y)]
                data[(prev_x - 1, y)] = rock
                collision = True
                break
        if not collision:
            del data[(x, y)]
            data[(max_x, y)] = rock

def part_1(data: dict[tuple[int, int], str]):
    # print_grid(data)
    data = deepcopy(data)
    max_y = max([y for x, y in data])
    roll_north(data)
    load = 0
    for (x, y), rock in data.items():
        if rock == '#':
            continue
        load += max_y - y + 1
    return load


def hash_dict(data):
        hash_ = 0
        for pair in data.items():
            hash_ ^= hash(pair)
        return hash_
    
def part_2(data: dict[tuple[int, int], str]):
    max_y = max([y for x, y in data])
    max_x = max([x for x, y in data])
    states = {}
    total_steps = 1_000_000_000
    steps_left = 0
    for idx in range(total_steps):
        roll_north(data)
        roll_west(data)
        roll_south(data, max_y)
        roll_east(data, max_x)
        state = hash_dict(data)
        if state in states:
            steps_left = ((total_steps - states[state]) % (idx - states[state])) - 1
            break
        states[state] = idx
    for _ in range(steps_left):
        roll_north(data)
        roll_west(data)
        roll_south(data, max_y)
        roll_east(data, max_x)
    load = 0
    for (x, y), rock in data.items():
        if rock == '#':
            continue
        load += max_y - y + 1
    return load

def parse_data():
    data = {}

    with open(f'day{day}.txt', 'r') as f:
        for y, line in enumerate(f):
            for x, char in enumerate(line):
                if char in ('#', 'O'):
                    data[(x, y)] = char
    return data

if __name__ == '__main__':
    start_time = time.perf_counter_ns()
    data = parse_data()
    data_time = time.perf_counter_ns()
    p1 = part_1(data)
    p1_time = time.perf_counter_ns()
    p2 = part_2(data)
    end_time = time.perf_counter_ns()
    print(f'''=== Day {day:02} ===\n'''
    f'''  · Loading data\n'''
    f'''  · Elapsed: {(data_time - start_time)/10**6:.3f} ms\n\n'''
    f'''  · Part 1: {p1}\n'''
    f'''  · Elapsed: {(p1_time - data_time)/10**6:.3f} ms\n\n'''
    f'''  · Part 2: {p2}\n'''
    f'''  · Elapsed: {(end_time - p1_time)/10**6:.3f} ms\n\n'''
    f'''  · Total elapsed: {(end_time - start_time)/10**6:.3f} ms''')