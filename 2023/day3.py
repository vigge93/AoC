import time
from copy import deepcopy

day = 3

def part_1(data):
    s = 0
    data = deepcopy(data)
    for _, row, col in data['symbols']:
        # Row above and below
        for num_row in range(row-1, row+2, 2):
            if num_row not in data['numbers']:
                continue
            indexes_to_remove = []
            for idx, number in enumerate(data['numbers'][num_row]):
                if number['start'] > col+1 or number['end'] < col -1:
                    continue
                s += number['number']
                indexes_to_remove.append(idx)
            for idx in sorted(indexes_to_remove, reverse=True):
                del data['numbers'][num_row][idx]
        
        if row not in data['numbers']:
            continue
        # Same row
        indexes_to_remove = []
        for idx, number in enumerate(data['numbers'][row]):
            if number['start'] == col+1 or number['end'] == col-1:
                s += number['number']
                indexes_to_remove.append(idx)
        for idx in sorted(indexes_to_remove, reverse=True):
                del data['numbers'][row][idx]
    return s

def part_2(data):
    s = 0
    for sym, row, col in data['symbols']:
        if sym != '*':
            continue
        adjacents = []
        # Row above and below
        for num_row in range(row-1, row+2, 2):
            if num_row not in data['numbers']:
                continue
            for number in data['numbers'][num_row]:
                if number['start'] > col+1 or number['end'] < col -1:
                    continue
                adjacents.append(number['number'])
        
        if row in data['numbers']:
            # Same row
            for number in data['numbers'][row]:
                if number['start'] == col+1 or number['end'] == col-1:
                    adjacents.append(number['number'])

        if len(adjacents) == 2:
            s += adjacents[0] * adjacents[1]
    return s

def parse_data():
    data = {
        'symbols': [],
        'numbers': {}
    }
    with open(f'day{day}.txt', 'r') as f:
        for row, line in enumerate(f):
            num = ''
            num_start = -1
            for col, symbol in enumerate(line):
                if symbol.isnumeric():
                    if not num:
                        num_start = col
                    num += symbol
                else:
                    if num:
                        if row not in data['numbers']:
                            data['numbers'][row] = []
                        data['numbers'][row].append({
                            'number': int(num),
                            'start': num_start,
                            'end': col-1,
                            'row': row
                        })
                        num = ''
                        num_start = -1
                    if symbol not in ('.', '\n'):
                        data['symbols'].append((symbol, row, col))
            
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