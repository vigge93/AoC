import time

day = 4

def part_1(data):
    overlap = 0
    for pair in data:
        if pair[0] <= pair[1] or pair[1] <= pair[0]:
            overlap += 1
    return overlap

def part_2(data):
    overlap = 0
    for pair in data:
        if not pair[0].isdisjoint(pair[1]):
            overlap += 1
    return overlap

def parse_data():
    data = []
    with open(f'day{day}.txt', 'r') as f:
        for line in f:
            l, r = line.strip().split(',')
            l1, l2 = l.split('-')
            r1, r2 = r.split('-')
            l = [x for x in range(int(l1), int(l2)+1)]
            r = [x for x in range(int(r1), int(r2)+1)]
            data.append((set(l), set(r)))
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