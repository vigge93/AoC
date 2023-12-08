import time

day = 25

SNAFU_TO_TEN = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
TEN_TO_SNAFU = {2: '2', 1: '1', 0: '0', -1: '-', -2: '='}
    # 1: '01',
    # 2: '02',
    # 3: '1=',
    # 4: '1-',
    # 5: '10',
    # 6: '11',
    # 7: '12',
    # 8: '2=',
    # 9: '2-'}
BASE = 5

def part_1(data):
    s = sum(data)
    r = ''
    b = 1
    while b <= s:
        b *= BASE
    b = b // 5
    while b != 0:
        cs = s // b
        cs = max(cs, -2)
        while cs > 2:
            b *= 5
            cr = SNAFU_TO_TEN[r[-1]]
            r = r[:-1]
            s += b*cr
            cs = cr + 1
            
        r += str(TEN_TO_SNAFU[cs])
        s -= b*cs
        b //= 5
    return r

def part_2(data):
    pass

def parse_data():
    data = []
    with open(f'day{day}.txt', 'r') as f:
        for line in f:
            line = line.strip()
            num = 0
            b = 1
            for chr in line[::-1]:
                num += SNAFU_TO_TEN[chr]*b
                b *= BASE
            data.append(num)
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