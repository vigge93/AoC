import time
from functools import cache

day = 18

def part_1(cubes):
    sides = len(cubes)*6
    for x, y, z in cubes:
        for off in (-1, 1):
            if (x + off, y, z) in cubes:
                sides -= 1
            if (x, y + off, z) in cubes:
                sides -= 1
            if (x, y, z + off) in cubes:
                sides -= 1
    return sides                    


def part_2(cubes):
    sides = len(cubes)*6
    maxX, maxY, maxZ = max(cubes)
    pointOutside = (maxX + 1, maxY, maxZ)
    outside = set()
    trapped = set()
    for cube in cubes:
        for off in range(-1, 2, 2):
            xSide = (cube[0] + off, cube[1], cube[2])
            ySide = (cube[0], cube[1] + off, cube[2])
            zSide = (cube[0], cube[1], cube[2] + off)
            if xSide in cubes:
                sides -= 1
            elif xSide in trapped:
                sides -= 1
            elif xSide not in outside:
                isOutside, visited = bfs(cubes, xSide, pointOutside)
                if not isOutside:
                    sides -= 1
                    trapped.update(visited)
                else:
                    outside.update(visited)
            
            if ySide in cubes:
                sides -= 1
            elif ySide in trapped:
                sides -= 1
            elif ySide not in outside:
                isOutside, visited = bfs(cubes, ySide, pointOutside)
                if not isOutside:
                    sides -= 1
                    trapped.update(visited)
                else:
                    outside.update(visited)
            
            if zSide in cubes:
                sides -= 1
            elif zSide in trapped:
                sides -= 1
            elif zSide not in outside:
                isOutside, visited = bfs(cubes, zSide, pointOutside)
                if not isOutside:
                    sides -= 1
                    trapped.update(visited)
                else:
                    outside.update(visited)
    return sides 

def bfs(cubes, start, goal):
    explored = {start}
    Q = []
    Q.append(start)
    while Q:
        print(len(Q))
        v = Q.pop(0)
        if v == goal:
            return True, explored
        for i in (-1, 1):
            nodes = [
                (v[0] + i, v[1], v[2]),
                (v[0], v[1] + i, v[2]),
                (v[0], v[1], v[2] + i)
            ]
            for node in nodes:
                if node not in explored and node not in cubes:
                    explored.add(node)
                    Q.append(node)
    return False, explored

def parse_data():
    data = set()
    with open(f'day{day}.txt', 'r') as f:
        for line in f:
            coords = tuple(map(int, line.strip().split(',')))
            data.add(coords)
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