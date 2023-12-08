import time

day = 6

def part_1(data):
    for i in range(0, len(data)-4):
        markers = set(data[i:i+4])
        if len(markers) == 4:
            break
    return i + 4

def part_2(data):
    for i in range(0, len(data)-14):
        markers = set(data[i:i+14])
        if len(markers) == 14:
            break
    return i + 14

def parse_data():
    with open(f'day{day}.txt', 'r') as f:
        data = f.read()
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