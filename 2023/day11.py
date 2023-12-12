import time
from itertools import combinations
from functools import cache

day = 11

@cache
def get_x_off(x, x_coords):
    return x - len(list(filter(lambda _x: _x <= x, x_coords)))

@cache
def get_y_off(y, y_coords):
    return y - len(list(filter(lambda _y: _y <= y, y_coords)))

def part_1(data):
    x_coords = frozenset(map(lambda galaxy: galaxy[0], data))
    y_coords = frozenset(map(lambda galaxy: galaxy[1], data))
    stretched_data = set()
    for galaxy in data:
        x_off = get_x_off(galaxy[0], x_coords)
        y_off = get_y_off(galaxy[1], y_coords)
        stretched_data.add((galaxy[0] + x_off, galaxy[1] + y_off))
    s = 0
    for galaxy_1, galaxy_2 in combinations(stretched_data, 2):
        s += abs(galaxy_1[0] - galaxy_2[0]) + abs(galaxy_1[1] - galaxy_2[1])
    return s

def part_2(data):
    scale = 999_999
    x_coords = frozenset(map(lambda galaxy: galaxy[0], data))
    y_coords = frozenset(map(lambda galaxy: galaxy[1], data))
    stretched_data = set()
    for galaxy in data:
        x_off = get_x_off(galaxy[0], x_coords)
        y_off = get_y_off(galaxy[1], y_coords)
        stretched_data.add((galaxy[0] + x_off*scale, galaxy[1] + y_off*scale))
    s = 0
    for galaxy_1, galaxy_2 in combinations(stretched_data, 2):
        s += abs(galaxy_1[0] - galaxy_2[0]) + abs(galaxy_1[1] - galaxy_2[1])
    return s

def parse_data():
    data = set()
    with open(f'day{day}.txt', 'r') as f:
        for y, line in enumerate(f):
            for x, spot in enumerate(line.strip()):
                if spot == "#":
                    data.add((x, y))
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