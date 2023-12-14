import time
from itertools import combinations

day = 13

def find_mirror(data):
    l_idx = 0
    for r_idx in range(l_idx + 1, len(data), 2):
        mirror = True
        for off in range(0, (r_idx - l_idx)//2 + 1):
            if data[l_idx + off] != data[r_idx - off]:
                mirror = False
                break
        if mirror:
            return l_idx + (r_idx - l_idx)//2 + 1
    
    r_idx = len(data) - 1
    for l_idx in range(r_idx - 1, -1, -2):
        mirror = True
        for off in range(0, (r_idx - l_idx)//2 + 1):
            if data[l_idx + off] != data[r_idx - off]:
                mirror = False
                break
        if mirror:
            return l_idx + (r_idx - l_idx)//2 + 1
    return 0

def find_smudge_mirror(data):
    l_idx = 0
    for r_idx in range(l_idx + 1, len(data), 2):
        mirror = True
        smudge_fixed = False
        for off in range(0, (r_idx - l_idx)//2 + 1):
            if data[l_idx + off] != data[r_idx - off]:
                if len(list(filter(lambda i: i[0] != i[1], zip(data[l_idx + off], data[r_idx - off])))) == 1 and not smudge_fixed:
                    smudge_fixed = True
                    continue
                mirror = False
                break
        if mirror and smudge_fixed:
            return l_idx + (r_idx - l_idx)//2 + 1
    
    r_idx = len(data) - 1
    for l_idx in range(r_idx - 1, -1, -2):
        mirror = True
        smudge_fixed = False
        for off in range(0, (r_idx - l_idx)//2 + 1):
            if data[l_idx + off] != data[r_idx - off]:
                if len(list(filter(lambda i: i[0] != i[1], zip(data[l_idx + off], data[r_idx - off])))) == 1 and not smudge_fixed:
                    smudge_fixed = True
                    continue
                mirror = False
                break
        if mirror and smudge_fixed:
            return l_idx + (r_idx - l_idx)//2 + 1
    return 0


def part_1(data):
    hor_mirrors = []
    vert_mirrors = []
    for grid in data:
        # Horizontal
        hor_mirrors.append(find_mirror(grid['rows']))
        vert_mirrors.append(find_mirror(grid['cols']))
    return sum(vert_mirrors) + sum(hor_mirrors)*100
        
def part_2(data):
    hor_mirrors = []
    vert_mirrors = []
    for grid in data:
        # Horizontal
        hor_mirrors.append(find_smudge_mirror(grid['rows']))
        vert_mirrors.append(find_smudge_mirror(grid['cols']))
    return sum(vert_mirrors) + sum(hor_mirrors)*100

def parse_data():
    data = []
    grid = {
        'rows': [],
        'cols': []
    }
    with open(f'day{day}.txt', 'r') as f:
        for line in f:
            if line.strip() == '':
                for i in range(len(grid['rows'][0])):
                    col = ''
                    for j in range(len(grid['rows'])):
                        col += grid['rows'][j][i]
                    grid['cols'].append(col)
                data.append(grid)
                grid = {
                    'rows': [],
                    'cols': []
                }
                continue
            grid['rows'].append(line.strip())
        for i in range(len(grid['rows'][0])):
            col = ''
            for j in range(len(grid['rows'])):
                col += grid['rows'][j][i]
            grid['cols'].append(col)
        data.append(grid)
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