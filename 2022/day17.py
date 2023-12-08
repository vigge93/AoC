import time
import math
from copy import deepcopy

day = 17

ROCKS = [
    [ # Horizontal line
        0b1111,
        0b0000,
        0b0000,
        0b0000
    ],
    [ # Cross
        0b0010,
        0b0111,
        0b0010,
        0b0000
    ],
    [ # Backward L
        0b0111,
        0b0001,
        0b0001,
        0b0000
    ],
    [ # Vertical line
        0b0001,
        0b0001,
        0b0001,
        0b0001
    ],
    [ # Square
        0b0011,
        0b0011,
        0b0000,
        0b0000
    ]
]


def part_1(data):
    room = []
    room.append(0b111111111)
    for _ in range(2022*4+1):
        room.append(0b100000001)
    floor = 0
    windIdx = 0
    for rockIdx in range(2022):
        rock = deepcopy(ROCKS[rockIdx % len(ROCKS)])
        y = floor + 4
        width = math.floor(math.log(max(rock), 2)) + 1
        offset = 1 + 5 - width
        rested = False
        rock = [r << offset for r in rock]
        while not rested:
            wind = data[windIdx % len(data)]
            windIdx += 1
            if wind == '<':
                rock = [r << 1 for r in rock]
                for h, line in enumerate(rock):
                    if (room[y+h] & line) != 0:
                        rock = [r >> 1 for r in rock]
                        break
            elif wind == '>':
                rock = [r >> 1 for r in rock]
                for h, line in enumerate(rock):
                    if (room[y+h] & line) != 0:
                        rock = [r << 1 for r in rock]
                        break
            y -= 1
            for h, line in enumerate(rock):
                if (room[y+h] & line) != 0:
                    y += 1
                    rested = True
                    break
        for h, line in enumerate(rock):
            room[y+h] = room[y+h] | line
            if (line != 0):
                floor = max(y + h, floor)
    return floor
def part_2(data):
    room = []
    iterations = 1_000_000_000_000
    room.append(0b111111111)
    for _ in range(10_000*4+1):
        room.append(0b100000001)
    floor = 0
    windIdx = 0
    hashes = set()
    hash_vals = {}
    for rockIdx in range(iterations):
        rock = deepcopy(ROCKS[rockIdx % len(ROCKS)])
        y = floor + 4
        width = math.floor(math.log(max(rock), 2)) + 1
        offset = 1 + 5 - width
        rested = False
        rock = [r << offset for r in rock]
        hash = get_hash(rockIdx % len(ROCKS), room, floor, windIdx % len(data))
        if hash in hashes:
            break
        hashes.add(hash)
        hash_vals[hash] = (rockIdx, floor)
        while not rested:
            wind = data[windIdx % len(data)]
            windIdx += 1
            if wind == '<':
                rock = [r << 1 for r in rock]
                for h, line in enumerate(rock):
                    if (room[y+h] & line) != 0:
                        rock = [r >> 1 for r in rock]
                        break
            elif wind == '>':
                rock = [r >> 1 for r in rock]
                for h, line in enumerate(rock):
                    if (room[y+h] & line) != 0:
                        rock = [r << 1 for r in rock]
                        break
            y -= 1
            for h, line in enumerate(rock):
                if (room[y+h] & line) != 0:
                    y += 1
                    rested = True
                    break
        for h, line in enumerate(rock):
            room[y+h] = room[y+h] | line
            if (line != 0):
                floor = max(y + h, floor)
    cycle_start_rock = hash_vals[hash][0]
    cycle_start_height = hash_vals[hash][1]
    rocks_per_cycle = rockIdx - cycle_start_rock
    height_per_cycle = floor - cycle_start_height
    cycles = (iterations - cycle_start_rock) // rocks_per_cycle
    # floor = height_per_cycle * cycles + cycle_start_height
    left = (iterations - cycle_start_rock) % rocks_per_cycle
    r_idx = rockIdx
    # left = iterations - cycles*rocks_per_cycle - cycle_start_rock
    for rockIdx in range(r_idx, r_idx + left):
        rock = deepcopy(ROCKS[rockIdx % len(ROCKS)])
        y = floor + 4
        width = math.floor(math.log(max(rock), 2)) + 1
        offset = 1 + 5 - width
        rested = False
        rock = [r << offset for r in rock]
        while not rested:
            wind = data[windIdx % len(data)]
            windIdx += 1
            if wind == '<':
                rock = [r << 1 for r in rock]
                for h, line in enumerate(rock):
                    if (room[y+h] & line) != 0:
                        rock = [r >> 1 for r in rock]
                        break
            elif wind == '>':
                rock = [r >> 1 for r in rock]
                for h, line in enumerate(rock):
                    if (room[y+h] & line) != 0:
                        rock = [r << 1 for r in rock]
                        break
            y -= 1
            for h, line in enumerate(rock):
                if (room[y+h] & line) != 0:
                    y += 1
                    rested = True
                    break
        for h, line in enumerate(rock):
            room[y+h] = room[y+h] | line
            if (line != 0):
                floor = max(y + h, floor)
    floor = floor - height_per_cycle
    floor = floor + height_per_cycle*cycles
    return floor

def get_hash(rockIdx, room, floor, windIdx):
    diffs = [-1]*7
    y = floor
    while -1 in diffs:
        row = room[y]
        tester = 0b10
        for x in range(7):
            if row & (tester<<x) != 0 and diffs[x] == -1:
                diffs[x] = floor - y
        y -= 1
    return (rockIdx, tuple(diffs), windIdx)
    



def parse_data():
    data = []
    with open(f'day{day}.txt', 'r') as f:
        line = f.read()
        data = list(line)
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