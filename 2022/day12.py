import time
from collections import deque

day = 12

def bfs(grid, start, goal):
    available_nodes = frozenset(grid.keys())
    explored = {start: 0}
    Q = deque()
    Q.append(start)
    while Q:
        v = Q.popleft()
        if v == goal or grid[v] == goal:
            return explored[v]
        for i in (-1, 1):
            node = (v[0] + i, v[1])
            if node not in explored and node in available_nodes:
                if grid[v] <= grid[node] + 1:
                    explored[node] = explored[v] + 1
                    Q.append(node)
        for j in (-1, 1):
            node = (v[0], v[1]+j)
            if node not in explored and node in available_nodes:
                if grid[v] <= grid[node] + 1:
                    explored[node] = explored[v] + 1
                    Q.append(node)
            

def part_1(data):
    grid = data['grid']
    start = data['start']
    end = data['end']
    path = bfs(grid, end, start)
    return path

def part_2(data):
    grid = data['grid']
    end = data['end']
    path = bfs(grid, end, 0)
    return path

def parse_data():
    data = {'grid': {}}
    with open(f'day{day}.txt', 'r') as f:
        for y, line in enumerate(f):
            for x, elevation in enumerate(line.strip()):
                if elevation == 'S':
                    data['start'] = (x, y)
                    elevation = 'a'
                elif elevation == 'E':
                    data['end'] = (x, y)
                    elevation = 'z'
                data['grid'][(x, y)] = ord(elevation) - ord('a')
    return data

if __name__ == '__main__':
    start_time = time.perf_counter_ns()
    data = parse_data()
    p1 = part_1(data)
    p2 = part_2(data)
    end_time = time.perf_counter_ns()
    print(f'=== Day {day:02} ===')
    print(f'  · Part 1: {p1}')
    print(f'  · Part 2: {p2}')
    print(f"  · Elapsed: {(end_time - start_time)/10**6:.3f} ms")