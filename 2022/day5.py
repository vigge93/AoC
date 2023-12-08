import time
from copy import deepcopy

day = 5

def part_1(data):
    data = deepcopy(data)
    stack = data['stack']
    moves = data['moves']
    for move in moves:
        mv = move[0]
        fr = move[1]
        to = move[2]
        mv_range = stack[fr][-mv:]
        del stack[fr][-mv:]
        stack[to] += mv_range[::-1]
    res = ''
    for i in range(1, max(stack.keys())+1):
        res += stack[i][-1]
    return res

def part_2(data):
    data = deepcopy(data)
    stack = data['stack']
    moves = data['moves']
    for move in moves:
        mv = move[0]
        fr = move[1]
        to = move[2]
        mv_range = stack[fr][-mv:]
        del stack[fr][-mv:]
        stack[to] += mv_range
    res = ''
    for i in range(1, max(stack.keys())+1):
        res += stack[i][-1]
    return res

def parse_data():
    data = {'stack': {}, 'moves': []}
    stack_done = False
    with open(f'day{day}.txt', 'r') as f:
        stack_lines = []
        for line in f:
            if line[:-1] == '': # Phase 2
                data['stack'] = {int(idx): [] for idx in stack_lines[-1].split()}
                for stack_line in stack_lines[-2::-1]:
                    for substr in range(0, len(stack_line), 4):
                        if stack_line[substr + 1] == ' ':
                            continue
                        data['stack'][substr/4 + 1].append(stack_line[substr+1])
                stack_done = True
                continue
            
            if not stack_done: # Phase 1
                stack_lines.append(line[:-1])
            else: # Phase 3
                moves = line.strip().split()
                num = int(moves[1])
                fr = int(moves[3])
                to = int(moves[5])
                data['moves'].append((num, fr, to))

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