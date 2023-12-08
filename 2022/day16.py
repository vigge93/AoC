import time
from dataclasses import dataclass
from functools import cache
from copy import deepcopy

day = 16

@dataclass
class Valve:
    name: int
    pressure: int
    connections: "list[Valve]"

    def value(self, t):
        return self.pressure*t

def bfs_m(valves):
    @cache
    def bfs_cache(start, goal):
        explored = {start: 0}
        Q = []
        Q.append(start)
        while Q:
            v = Q.pop(0)
            if v == goal:
                return explored[v]
            for c_valve in valves[v].connections:
                if c_valve.name not in explored:
                    explored[c_valve.name] = explored[v] + 1
                    Q.append(c_valve.name)
    return bfs_cache

bfs = None


def paths_part1(current_valve, data, valid, time):
    paths_lst= []
    for valve in valid:
        path = []
        dist = bfs(current_valve, valve)
        if time - dist - 1 <= 0: continue
        path.append([valve, dist + 1])
        paths_r = paths_part1(valve, data, [x for x in valid if x != valve], time - dist - 1)
        if paths_r:
            for p in paths_r:
                paths_lst.append(path + p)
        else:
            paths_lst.append(path)
    return paths_lst

def part_1(data):
    valid = []
    for valve in data.values():
        if valve.pressure > 0:
            valid.append(valve.name)
    p = paths_part1('AA', data, valid, 30)
    max_score = 0
    for path in p:
        score = 0
        t = 30
        for step in path:
            t -= step[1]
            score += data[step[0]].value(t)
        if score > max_score:
            max_score = score
    return max_score

i = 0

def get_score(path):
    score = 0
    l = path[0]
    r = path[1]
    for step in l:
        score += data[step[0]].value(step[1])
    for step in r:
        score += data[step[0]].value(step[1])
    if score > max_score:
        max_score = score
    return score

def get_p1_moves(row, data):
    time = max(row[3], row[4])
    if row[3] != time:
        return [row]
    new_states = []
    for s in row[5]:
        dist = bfs(row[1], s)
        new_t = time - dist - 1
        if new_t < 0: continue
        new_state = [row[0] + new_t*data[s].pressure, s, row[2], new_t, row[4], [x for x in row[5] if x != s]]
        new_states.append(new_state)
    if not new_states:
        row = deepcopy(row)
        row[3] = 0
        return [row]
    else:
        return new_states

def get_p2_moves(states, data):
    new_states = []
    for row in states:
        time = max(row[3], row[4])
        if time != row[4]:
            continue
        for s in row[5]:
            dist = bfs(row[2], s)
            new_t = time - dist - 1
            if new_t <= 0: continue
            new_state = [row[0] + new_t*data[s].pressure, row[1], s, row[3], new_t, [x for x in row[5] if x != s]]
            new_states.append(new_state)
    if not new_states:
        for s in states:
            s = deepcopy(s)
            s[4] = 0
            new_states.append(s)
    return new_states


def part_2(data):
    valid = []
    for valve in data.values():
        if valve.pressure > 0:
            valid.append(valve.name)
    candidates = [[0, 'AA', 'AA', 26, 26, valid]]
    best_score = 0
    best_at_t = {x: 0 for x in range(27)}
    while candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        current = candidates.pop(0)
        flow = current[0]
        t = max(current[3], current[4])
        valid = current[5]
        best_score = max(best_score, flow)
        best_at_t[t] = max(best_at_t[t], flow)
        if t > 0 and valid:
            if t > 16 or flow >= 0.8*best_at_t[t]:
                p1_states = get_p1_moves(current, data)
                p2_states = get_p2_moves(p1_states, data)
                candidates += p2_states
    return best_score

def parse_data():
    data = {}
    with open(f'day{day}.txt', 'r') as f:
        t_data = {}
        for line in f:
            line = line[6:].strip()
            v, conn = line.split(';')
            valve = v[:2]
            flow = int(v.split('=')[1])
            conn = [c.strip() for c in conn.split(',')]
            conn[0] = conn[0][-2:]
            v = Valve(valve, flow, conn)
            t_data[valve] = v
        for valve in t_data.values():
            new_conn = []
            for conn in valve.connections:
                new_conn.append(t_data[conn])
            valve.connections = new_conn
            data[valve.name] = valve
    global bfs
    bfs = bfs_m(data)
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