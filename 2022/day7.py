import time
from functools import cache
from copy import deepcopy

day = 7

def calcDirsize(dir):
    sum = 0
    for key, value in dir.items():
        if key == '..': continue
        if isinstance(value, int):
            sum += value
        else:
            sum += calcDirsize(value)
    dir['.size'] = sum
    return sum

def sumSmall(dir, max):
    sum = 0
    for key, value in dir.items():
        if key == '..': continue
        if isinstance(value, int): continue
        sum += sumSmall(value, max)
    if dir['.size'] <= max:
        sum += dir['.size']
    return sum


def findSmall(dir, min):
    smaller = None
    if dir['.size'] < min: return None
    for key, value in dir.items():
        if key == '..': continue
        if isinstance(value, int): continue
        smaller_c = findSmall(value, min)
        if smaller_c is not None and (smaller is None or smaller_c < smaller):
            smaller = smaller_c
    if smaller:
        return smaller
    else:
        return dir['.size']

def part_1(data):
    data = deepcopy(data)
    calcDirsize(data['/'])
    return sumSmall(data['/'], 100000)

def part_2(data):
    calcDirsize(data['/'])
    total = 70000000
    unused = total - data['/']['.size']
    required = 30000000
    to_del = required - unused
    return findSmall(data['/'], to_del)



def parse_data():
    data = {'/': {'..': None}}
    currentDir = None
    with open(f'day{day}.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('$'):
                if 'cd' in line:
                    parts = line.split()
                    if parts[2] == '/':
                        currentDir = data['/']
                    else:
                        currentDir = currentDir[parts[2]]
                elif 'ls' in line:
                    pass
            else:
                parts = line.split()
                if parts[0] == 'dir':
                    if parts[1] not in currentDir:
                        currentDir[parts[1]] = {'..': currentDir}
                else:
                    if parts[1] not in currentDir:
                        currentDir[parts[1]] = int(parts[0])
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