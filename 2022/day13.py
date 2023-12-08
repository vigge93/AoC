import time
import functools

day = 13

def compare(left, right):
    for i in range(len(left)):
        try:
            if isinstance(left[i], int) and isinstance(right[i], int):
                if left[i] < right[i]:
                    return True
                elif left [i] > right[i]:
                    return False
            elif isinstance(left[i], list) and isinstance(right[i], list):
                result = compare(left[i], right[i])
                if result is not None:
                    return result
            else:
                l = left[i]
                r = right[i]
                if isinstance(l, int):
                    l = [l]
                if isinstance(r, int):
                    r = [r]
                result = compare(l, r)
                if result is not None:
                    return result  
        except IndexError: # Right is shorter
            return False
    if len(left) != len(right):
        return True
    return None

def compare_key(left, right):
    res = compare(left, right)
    return -1 if res else 1

def part_1(data):
    s = 0
    for idx, pair in enumerate(data):
        if compare(pair[0], pair[1]):
            s += idx + 1
    return s

def part_2(data):
    packets = []
    div1 = [[2]]
    div2 = [[6]]
    for pair in data:
        packets.append(pair[0])
        packets.append(pair[1])
    packets.append(div1)
    packets.append(div2)
    packets.sort(key=functools.cmp_to_key(compare_key))
    # for n in range(len(packets)):
    #     for i in range(n%2,len(packets)-1,2):
    #         if not compare(packets[i], packets[i+1]):
    #             packets[i], packets[i+1] = packets[i+1], packets[i] # Swap
    return (packets.index(div1)+1)*(packets.index(div2)+1)

def parse_data():
    data = []
    with open(f'day{day}.txt', 'r') as f:
        pair = []
        for line in f:
            if line.strip() == '':
                data.append(pair)
                pair = []
                continue
            pair.append(parse_row(line.strip()))
        data.append(pair)
    return data

def parse_row(row):
    i = 0
    lst = []
    count = 0
    while i < len(row):
        if row[i] == '[':
            count += 1
            if count == 2:
                lst.append(parse_row(row[i:]))
        elif row[i] == ']':
            count -= 1
            if count == 0:
                return lst
        elif count == 1 and row[i].isnumeric():
            x = i
            while row[x].isnumeric():
                x += 1
            lst.append(int(row[i:x]))
            i = x - 1
        i += 1

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