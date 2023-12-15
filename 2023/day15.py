import time
from functools import reduce

day = 15

def hash_str(string):
    hash_ = 0
    for char in string:
        hash_ += ord(char)
        hash_ *= 17
    hash_ %= 256
    return hash_

def part_1(data):
    return sum(map(hash_str, data))

def part_2(data):
    boxes = {}
    for step in data:
        if '-' in step:
            label = step[:-1]
            box = hash_str(label)
            if box in boxes and label in boxes[box]:
                del boxes[box][label]
        else:
            label, lens = step.split('=')
            box = hash_str(label)
            lens = int(lens)
            if box not in boxes:
                boxes[box] = {}
            boxes[box][label] = lens
    s = 0
    for box_num, box in boxes.items():
        for lens_idx, lens in enumerate(box):
            s += box[lens] * (lens_idx + 1) * (box_num + 1)
    return s


def parse_data():
    data = []
    with open(f'day{day}.txt', 'r') as f:
        line = f.readline()
        data = line.split(',')
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