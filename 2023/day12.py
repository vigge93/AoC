import time
from copy import deepcopy
from functools import cache
from multiprocessing import Pool


day = 12

@cache
def recurse_memoize(springs, schematic) -> int:
    if not schematic:
        for springIdx in range(len(springs)):
            spring = springs[springIdx]
            for subSpringIdx in range(len(spring)):
                if spring[subSpringIdx] == '#':
                    return 0
        return 1
    next_schematic = schematic[0]
    found = False
    s = 0
    # Find empty spot for next spring:
    prev_s = '.'
    for springIdx in range(len(springs)):
        spring = springs[springIdx]
        if len(spring) < next_schematic:
            if "#" in spring:
                break
            continue
        for subSpringIdx in range(len(spring)):
            if (len(spring) - subSpringIdx) < next_schematic:
                prev_s = spring[subSpringIdx]
                break
            if prev_s == '#':
                break
            if (len(spring) - subSpringIdx) >= next_schematic + 1 and spring[subSpringIdx + next_schematic] == '#':
                prev_s = spring[subSpringIdx]
                continue
            prev_s = spring[subSpringIdx]
            if any(map(lambda s: '#' in s, springs[:springIdx])):
                prev_s = "#"
                break
            found = True
            new_springs = deepcopy(springs)
            new_springs = (new_springs[springIdx][subSpringIdx+next_schematic+1:],) + new_springs[springIdx+1:]
            s += recurse_memoize(new_springs, schematic[1:])
    if not found:
        return 0
    else:
        return s

def part_1(data):
    s = 0
    for springs, schematic in data['part1']:
        s += recurse_memoize(springs, schematic)
    return s

def part_2(data):
    p = Pool()
    sums = p.starmap(recurse_memoize, data['part2'])  
    return sum(sums)

def parse_data():
    data = {
        'part1': [],
        'part2': []
    }
    with open(f'day{day}.txt', 'r') as f:
        for line in f:
            springs_1, schematic_1 = line.strip().split()
            springs_2 = '?'.join([springs_1]*5)
            schematic_2 = ','.join([schematic_1]*5)
            schematic_1 = tuple([int(n) for n in schematic_1.split(',')])
            springs_1 = springs_1.strip().strip('.').split('.')
            schematic_2 = tuple([int(n) for n in schematic_2.split(',')])
            springs_2 = springs_2.strip().strip('.').split('.')
            data['part1'].append((tuple([tuple(spring) for spring in springs_1 if spring]), schematic_1))
            data['part2'].append((tuple([tuple(spring) for spring in springs_2 if spring]), schematic_2))
    return data

if __name__ == '__main__':
    start_time = time.perf_counter_ns()
    data = parse_data()
    data_time = time.perf_counter_ns()
    p1 = part_1(data)
    p1_time = time.perf_counter_ns()
    p2 = part_2(data)
    end_time = time.perf_counter_ns()
    print(recurse_memoize.cache_info())
    print(f'''=== Day {day:02} ===\n'''
    f'''  · Loading data\n'''
    f'''  · Elapsed: {(data_time - start_time)/10**6:.3f} ms\n\n'''
    f'''  · Part 1: {p1}\n'''
    f'''  · Elapsed: {(p1_time - data_time)/10**6:.3f} ms\n\n'''
    f'''  · Part 2: {p2}\n'''
    f'''  · Elapsed: {(end_time - p1_time)/10**6:.3f} ms\n\n'''
    f'''  · Total elapsed: {(end_time - start_time)/10**6:.3f} ms''')