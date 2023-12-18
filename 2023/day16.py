import time
from dataclasses import dataclass
from multiprocessing import Pool
from functools import partial

@dataclass
class Obstacle:
    x: int
    y: int
    type: str

day = 16

def get_next_obstacle(beam: tuple[int, int, str], obstacles: dict[str, dict[int, list[Obstacle]]]) -> Obstacle:
    x, y, direction = beam
    if direction == 's':
        candidates = list(filter(lambda obstacle: obstacle.y > y, obstacles['s'][x]))
        if not candidates:
            return None
        return candidates[0]
    if direction == 'n':
        candidates = list(filter(lambda obstacle: obstacle.y < y, obstacles['n'][x]))
        if not candidates:
            return None
        return candidates[-1]
    if direction == 'e':
        candidates = list(filter(lambda obstacle: obstacle.x > x, obstacles['e'][y]))
        if not candidates:
            return None
        return candidates[0]
    if direction == 'w':
        candidates = list(filter(lambda obstacle: obstacle.x < x, obstacles['w'][y]))
        if not candidates:
            return None
        return candidates[-1]
    

def energize_counter(beam: tuple[int, int, str], energized: set[tuple[int, int, str]], obstacles: dict[str, dict[int, list[Obstacle]]]):
    if beam in energized:
        return
    x, y, direction = beam
    next_obstacle = get_next_obstacle(beam, obstacles)
    if not next_obstacle:
        if direction == 's':
            energized.update([(x, new_y, direction) for new_y in range(y, max(obstacles['s']) + 1)])
        elif direction == 'n':
            energized.update([(x, new_y, direction) for new_y in range(y, -1, -1)])
        elif direction == 'e':
            energized.update([(new_x, y, direction) for new_x in range(x, max(obstacles['e']) + 1)])
        elif direction == 'w':
            energized.update([(new_x, y, direction) for new_x in range(x, -1, -1)])
        return

    next_x, next_y = next_obstacle.x, next_obstacle.y
    if direction == 's':
        energized.update([(x, new_y, direction) for new_y in range(y, next_obstacle.y)])
        if next_obstacle.type in ('/', '-'):
            energize_counter((next_x, next_y, 'w'), energized, obstacles)
        if next_obstacle.type in ('\\', '-'):
            energize_counter((next_x, next_y, 'e'), energized, obstacles)
        if next_obstacle.type == '|':
            energize_counter((next_x, next_y, direction), energized, obstacles)
    elif direction == 'n':
        energized.update([(x, new_y, direction) for new_y in range(y, next_obstacle.y, -1)])
        if next_obstacle.type in ('/', '-'):
            energize_counter((next_x, next_y, 'e'), energized, obstacles)
        if next_obstacle.type in ('\\', '-'):
            energize_counter((next_x, next_y, 'w'), energized, obstacles)
        if next_obstacle.type == '|':
            energize_counter((next_x, next_y, direction), energized, obstacles)
    elif direction == 'e':
        energized.update([(new_x, y, direction) for new_x in range(x, next_obstacle.x)])
        if next_obstacle.type in ('/', '|'):
            energize_counter((next_x, next_y, 'n'), energized, obstacles)
        if next_obstacle.type in ('\\', '|'):
            energize_counter((next_x, next_y, 's'), energized, obstacles)
        if next_obstacle.type == '-':
            energize_counter((next_x, next_y, direction), energized, obstacles)
    elif direction == 'w':
        energized.update([(new_x, y, direction) for new_x in range(x, next_obstacle.x, -1)])
        if next_obstacle.type in ('/', '|'):
            energize_counter((next_x, next_y, 's'), energized, obstacles)
        if next_obstacle.type in ('\\', '|'):
            energize_counter((next_x, next_y, 'n'), energized, obstacles)
        if next_obstacle.type == '-':
            energize_counter((next_x, next_y, direction), energized, obstacles)

def part_1(data):
    beam = (-1, 0, 'e')
    return run(beam, data)
    
def run(beam: tuple[int, int, str], data):
    energized = set()
    energize_counter(beam, energized, data)
    distinct_energised = set()
    for energize in energized:
        distinct_energised.add((energize[0], energize[1]))
    return len(distinct_energised) - 1

def part_2(data):
    max_e = -1
    run_part = partial(run, data=data)
    beams = []
    max_x = max(data['n'])
    max_y = max(data['e'])
    beams += [(-1, y, 'e') for y in range(0, max_y + 1)]
    beams += [(max_x + 1, y, 'w') for y in range(0, max_y + 1)]
    beams += [(x, -1, 's') for x in range(0, max_x + 1)]
    beams += [(x, max_y + 1, 'n') for x in range(0, max_x + 1)]

    with Pool() as p:
        max_e = max(p.imap_unordered(run_part, beams, 16))
    return max_e

def parse_data():
    data = {
        'n': {},
        'w': {},
        's': {},
        'e': {}
    }
    with open(f'day{day}.txt', 'r') as f:
        for y, row in enumerate(f):
            for x, cell in enumerate(row.strip()):
                if cell == '.':
                    continue
                obstacle = Obstacle(x, y, cell)
                if x not in data['n']:
                    data['n'][x] = []
                if x not in data['s']:
                    data['s'][x] = []
                data['n'][x].append(obstacle)
                data['s'][x].append(obstacle)
                if y not in data['e']:
                    data['e'][y] = []
                if y not in data['w']:
                    data['w'][y] = []
                data['e'][y].append(obstacle)
                data['w'][y].append(obstacle)
    return data

if __name__ == '__main__':
    start_time = time.perf_counter_ns()
    data = parse_data()
    data_time = time.perf_counter_ns()
    p1 = part_1(data)
    p1_time = time.perf_counter_ns()
    p2 = part_2(data)
    end_time = time.perf_counter_ns()
    print(f'''=== Day {day:02} ===\n'''
    f'''  · Loading data\n'''
    f'''  · Elapsed: {(data_time - start_time)/10**6:.3f} ms\n\n'''
    f'''  · Part 1: {p1}\n'''
    f'''  · Elapsed: {(p1_time - data_time)/10**6:.3f} ms\n\n'''
    f'''  · Part 2: {p2}\n'''
    f'''  · Elapsed: {(end_time - p1_time)/10**6:.3f} ms\n\n'''
    f'''  · Total elapsed: {(end_time - start_time)/10**6:.3f} ms''')