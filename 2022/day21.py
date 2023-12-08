import time
from functools import cache

day = 21

def get_value_1(key):
    try:
        return int(key)
    except:
        pass
    func = data1[key]
    while not isinstance(func, int):
        func = func()
    return func

def get_value_2(key):
    if isinstance(data2[key], str) and (data2[key].isnumeric() or 'humn' in data2[key]):
        return data2[key]
    func = data2[key]
    func = func()
    return func


def add(lhs, rhs):
    lhs = get_value_2(lhs)
    rhs = get_value_2(rhs)
    if isinstance(lhs, str) and isinstance(rhs, str) and lhs.isnumeric() and rhs.isnumeric():
        return f'{int(lhs) + int(rhs)}'
    elif isinstance(lhs, str) and lhs.isnumeric():
        if isinstance(rhs, str):
            return lambda y, lhs=lhs:  int(lhs) - y
        else:
            return lambda y, lhs=lhs, rhs=rhs: rhs(y - int(lhs))
    elif isinstance(rhs, str) and rhs.isnumeric():
        if isinstance(lhs, str):
            return lambda y, rhs=rhs: y - int(rhs)
        else:
            return lambda y, lhs=lhs, rhs=rhs: lhs(y - int(rhs))

def subtract(lhs, rhs):
    lhs = get_value_2(lhs)
    rhs = get_value_2(rhs)
    if isinstance(lhs, str) and isinstance(rhs, str) and lhs.isnumeric() and rhs.isnumeric():
        return f'{int(lhs) - int(rhs)}'
    elif isinstance(lhs, str) and lhs.isnumeric():
        if isinstance(rhs, str):
            return lambda y, lhs=lhs:  int(lhs) + y
        else:
            return lambda y, lhs=lhs, rhs=rhs:  rhs(int(lhs) - y)
    elif isinstance(rhs, str) and rhs.isnumeric():
        if isinstance(lhs, str):
            return lambda y, rhs=rhs: y + int(rhs)
        else:
            return lambda y, lhs=lhs, rhs=rhs: lhs(y + int(rhs))

def multiply(lhs, rhs):
    lhs = get_value_2(lhs)
    rhs = get_value_2(rhs)
    if isinstance(lhs, str) and isinstance(rhs, str) and lhs.isnumeric() and rhs.isnumeric():
        return f'{int(lhs) * int(rhs)}'
    elif isinstance(lhs, str) and lhs.isnumeric():
        if isinstance(rhs, str):
            return lambda y, lhs=lhs:  int(lhs) // y
        else:
            return lambda y, lhs=lhs, rhs=rhs: rhs(y // int(lhs))
    elif isinstance(rhs, str) and rhs.isnumeric():
        if isinstance(lhs, str):
            return lambda y, rhs=rhs: y // int(rhs)
        else:
            return lambda y, lhs=lhs, rhs=rhs: lhs(y // int(rhs))

def divide(lhs, rhs):
    lhs = get_value_2(lhs)
    rhs = get_value_2(rhs)
    if isinstance(lhs, str) and isinstance(rhs, str) and lhs.isnumeric() and rhs.isnumeric():
        return f'{int(lhs) // int(rhs)}'
    elif isinstance(lhs, str) and lhs.isnumeric():
        if isinstance(rhs, str):
            return lambda y, lhs=lhs:  int(lhs) // y
        else:
            return lambda y, lhs=lhs, rhs=rhs: rhs(int(lhs) // y)
    elif isinstance(rhs, str) and rhs.isnumeric():
        if isinstance(lhs, str):
            return lambda y, rhs=rhs:  int(rhs) * y
        else:
            return lambda y, lhs=lhs, rhs=rhs: lhs(int(rhs) * y)

def part_1(data):
    func = data['root']
    return func()

def part_2(data):
    data['humn'] = 'humn'
    func = data['root']
    # while not isinstance(func, str):
    lhs, rhs = func()
    if isinstance(lhs, str):
        lhs = int(lhs)
        func = rhs(lhs)
    else:
        rhs = int(rhs)
        func = lhs(rhs)
    return func

data1 = {}
data2 = {}

def parse_data():
    global data1, data2
    with open(f'day{day}.txt', 'r') as f:
        for line in f:
            name, op = line.strip().split(':')
            if op.strip().isnumeric():
                data1[name] = int(op)
                data2[name] = op.strip()
            else:
                lhs, op, rhs = op.split()
                lhs, rhs = lhs.strip(), rhs.strip()
                if name == 'root':
                    data1[name] = lambda lhs=lhs, rhs=rhs: get_value_1(lhs) + get_value_1(rhs)
                    data2[name] = lambda lhs=lhs, rhs=rhs: (get_value_2(lhs), get_value_2(rhs))
                elif op == '+':
                    data1[name] = lambda lhs=lhs, rhs=rhs: get_value_1(lhs) + get_value_1(rhs)
                    data2[name] = lambda lhs=lhs, rhs=rhs: add(lhs, rhs)
                elif op == '-':
                    data1[name] = lambda lhs=lhs, rhs=rhs: get_value_1(lhs) - get_value_1(rhs)
                    data2[name] = lambda lhs=lhs, rhs=rhs: subtract(lhs, rhs)
                elif op == '*':
                    data1[name] = lambda lhs=lhs, rhs=rhs: get_value_1(lhs) * get_value_1(rhs)
                    data2[name] = lambda lhs=lhs, rhs=rhs: multiply(lhs, rhs)
                elif op == '/':
                    data1[name] = lambda lhs=lhs, rhs=rhs: get_value_1(lhs) // get_value_1(rhs)
                    data2[name] = lambda lhs=lhs, rhs=rhs: divide(lhs, rhs)
    return data1, data2

if __name__ == '__main__':
    start_time = time.perf_counter_ns()
    data1, data2 = parse_data()
    p1 = part_1(data1)
    p2 = part_2(data2)
    end_time = time.perf_counter_ns()
    print(f'=== Day {day:02} ===')
    print(f'  · Part 1: {p1}')
    print(f'  · Part 2: {p2}')
    print(f"  · Elapsed: {(end_time - start_time)/10**6:.3f} ms")