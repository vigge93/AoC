import time

day = 3

def part_1(data):
    alph = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    priority = 0
    for sack in data:
        common: set = sack['left'].intersection(sack['right'])
        priority += alph.find(common.pop()) + 1
    return priority


def part_2(data):
    alph = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    priority = 0
    for i in range(0, len(data), 3):
        common = data[i]['left'].union(data[i]['right'])
        for j in range(1,3):
            common = common.intersection(data[i+j]['left'].union(data[i+j]['right']))
        priority += alph.find(common.pop()) + 1
    return priority


def parse_data():
    data = []
    with open(f'day{day}.txt', 'r') as f:
        for line in f:
            line = line.strip()
            l = line[:int(len(line)/2)]
            r = line[int(len(line)/2):]
            data.append({'left': set(l), 'right': set(r)})
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