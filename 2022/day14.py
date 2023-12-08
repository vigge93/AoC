import time
from copy import deepcopy

day = 14

def part_1(wall):
    wall = deepcopy(wall)
    lowest = max(wall, key=lambda x: x[1])[1]
    void = False
    units = 0
    while not void:
        sand = (500, 0)
        resting = False
        while not resting and not void:
            if not (sand[0], sand[1]+1) in wall:
                sand = (sand[0], sand[1]+1)
            elif not (sand[0]-1, sand[1]+1) in wall:
                sand = (sand[0]-1, sand[1]+1)
            elif not (sand[0]+1, sand[1]+1) in wall:
                sand = (sand[0]+1, sand[1]+1)
            else:
                resting = True
            if sand[1] >= lowest:
                void = True
        if not void:
            units += 1
            wall.add(sand)
    return units

def part_2(wall):
    wall = deepcopy(wall)
    floor = max(wall, key=lambda x: x[1])[1] + 2
    first_rock = min(wall, key=lambda x: x[1] if x[0] == 500 else 1000)[1]
    units = 0
    sandX, sandY = 0, 0
    while sandY != 0 or sandX != 500:
        sandX = 500
        sandY = first_rock - 1
        resting = False
        while not resting:
            if (sandX, sandY+1) not in wall:
                sandY += 1
            elif (sandX-1, sandY+1) not in wall:
                sandX -= 1
                sandY += 1
            elif (sandX+1, sandY+1) not in wall:
                sandX += 1
                sandY += 1
            else:
                resting = True
            if sandY+1 == floor:
                resting = True
        units += 1
        wall.add((sandX, sandY))
        if sandX == 500:
            first_rock = min(sandY, first_rock)
    return units

def parse_data():
    data = set()
    with open(f'day{day}.txt', 'r') as f:
        for line in f:
            segments = line.strip().split('->')
            for i in range(len(segments)-1):
                s = [int(s) for s in segments[i].split(',')]
                e  = [int(s) for s in segments[i +1].split(',')]
                for x in range(min(s[0], e[0]), max(s[0], e[0])+1):
                    for y in range(min(s[1], e[1]), max(s[1], e[1])+1):
                        data.add((x, y))
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