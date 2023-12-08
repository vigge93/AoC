import time
import math

day = 9

def part_1(data):
    visited = {(0,0)}
    H = {'x': 0, 'y': 0}
    T = {'x': 0, 'y': 0}
    for move in data:
        H[move[0]] += move[1]
        if ((H['x']-T['x'])**2 + (H['y'] - T['y'])**2)**0.5 >= 2:
            if H['x'] - T['x'] != 0:
                T['x'] += int(math.copysign(1, H['x'] - T['x']))
            if H['y'] - T['y'] != 0:
                T['y'] += int(math.copysign(1, H['y'] - T['y']))
        visited.add((T['y'], T['x']))
    return len(visited)

def part_2(data):
    visited = {(0,0)}
    H = {'x': 0, 'y': 0}
    T = [{'x': 0, 'y': 0} for _ in range(9)]
    for move in data:
        H[move[0]] += move[1]
        prev_knot = H
        for knot in T:
            if max(abs(prev_knot['x']-knot['x']), abs(prev_knot['y'] - knot['y'])) > 1:
                if prev_knot['x'] - knot['x'] != 0:
                    knot['x'] += int(math.copysign(1, prev_knot['x'] - knot['x']))
                if prev_knot['y'] - knot['y'] != 0:
                    knot['y'] += int(math.copysign(1, prev_knot['y'] - knot['y']))
            prev_knot = knot
        visited.add((T[-1]['y'], T[-1]['x']))
    return len(visited)

def parse_data():
    data = []
    with open(f'day{day}.txt', 'r') as f:
        for line in f:
            move = line.strip().split()
            move[1] = int(move[1])
            if move[0] == 'U':
                move[0] = 'y'
                move[1] *= -1
            elif move[0] == 'D':
                move[0] = 'y'
            elif move[0] == 'L':
                move[0] = 'x'
                move[1] *= -1
            elif move[0] == 'R':
                move[0] = 'x'
            for _ in range(abs(move[1])):
                data.append((move[0], int(math.copysign(1, move[1]))))
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