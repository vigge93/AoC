import time

def part_1(data):
    return max(data)

def part_2(data):
    max1 = max(data)
    data.remove(max1)
    max2 = max(data)
    data.remove(max2)
    max3 = max(data)
    data.remove(max3)
    return max1 + max2 + max3

def parse_data():
    data = []
    with open('day1.txt', 'r') as f:
        s = 0
        for line in f:
            if line.strip() == '':
                data.append(s)
                s = 0
                continue
            s += int(line.strip())
    return data

if __name__ == '__main__':
    start_time = time.perf_counter_ns()
    data = parse_data()
    p1 = part_1(data)
    p2 = part_2(data)
    end_time = time.perf_counter_ns()
    print('=== Day 01 ===')
    print(f'  · Part 1: {p1}')
    print(f'  · Part 2: {p2}')
    print(f"  · Elapsed: {(end_time - start_time)/10**6:.3f} ms")
