import time

day = 10

def part_1(data):
    x  = 1
    cycle = 1
    score = 0
    for inst in data:
        if cycle > 220:
            break
        if inst[0] == 'addx':
            cycle += 1
            if (cycle-20) % 40 == 0:
                score += cycle*x
            x += int(inst[1])
        
        cycle += 1
        if (cycle-20) % 40 == 0:
            score += cycle*x
    return score


def part_2(data):
    def increase_cycle():
        nonlocal cycle, h_scan, res
        cycle += 1
        h_scan += 1
        if (cycle-1) % 40 == 0:
            res += '\n'
            h_scan = 0
    x  = 1
    res = '\n'
    cycle = 1
    h_scan = 0
    for inst in data:
        res += draw_pixel(x, h_scan)
        if inst[0] == 'addx':
            increase_cycle()
            res += draw_pixel(x, h_scan)
            x += int(inst[1])
        increase_cycle()
    return res

def draw_pixel(x, h_scan):
    if abs(x-h_scan) <= 1:
        return '#'  # '██'
    else:
        return '.'  # '░░'

def parse_data():
    data = []
    with open(f'day{day}.txt', 'r') as f:
        for line in f:
            data.append(line.strip().split())
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