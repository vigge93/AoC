import time
from typing import TypedDict
import numpy as np

day = 21

type plot = tuple[int, int]
type plots = set[plot]

class DataDict(TypedDict):
    plots: plots
    start: plot
    
type Data =  DataDict

DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))

def part_1(data: Data):
    start = data['start']
    plots = data['plots']
    current = {start}
    for _ in range(64):
        next_plots: set[plot] = set()
        for cplot in current:
            for dir in DIRECTIONS:
                new_plot: tuple = tuple([sum(p) for p in zip(cplot,dir)])
                if new_plot in plots:
                    next_plots.add(new_plot)
        current = next_plots
    return len(current)


def part_2(data: Data):
    start = data['start']
    plots = data['plots']
    rows, cols = max(plots)
    rows += 1
    cols += 1
    target = 26501365
    current = {start}
    factors: list[int] = []
    for step in range(1000):
        next_plots: set[plot] = set()
        for cplot in current:
            for dir in DIRECTIONS:
                new_plot: plot = (cplot[0] + dir[0], cplot[1] + dir[1])
                if (new_plot[0] % cols, new_plot[1] % rows) in plots:
                    next_plots.add(new_plot)
        current = next_plots
        if step == rows // 2 + rows*len(factors):
            factors.append(len(current))
            if len(factors) == 3:
                print(factors)
                delta0, delta1, delta2 = factors[0], factors[1] - factors[0], factors[2] - 2 * factors[1] + factors[0]
                res = delta0 + delta1 * (target // rows) + delta2 * ((target // rows) * ((target // rows) - 1) // 2)
                break
    # coeff = np.polyfit([1, 2, 3], factors, 2)
    # res = np.polyval(coeff, (target - 65)//131)
    return res
        

def parse_data():
    data: Data = {
        'plots': set(),
        'start': (0, 0)
    }
    with open(f"day{day}.txt", "r") as f:
        for y, line in enumerate(f):
            for x, lot in enumerate(line):
                if lot in ('.', 'S'):
                    data['plots'].add((x, y))
                if lot == 'S':
                    data['start'] = (x, y)
    return data


if __name__ == "__main__":
    start_time = time.perf_counter_ns()
    data = parse_data()
    data_time = time.perf_counter_ns()
    p1 = part_1(data)
    p1_time = time.perf_counter_ns()
    p2 = part_2(data)
    end_time = time.perf_counter_ns()
    print(
        f"""=== Day {day:02} ===\n"""
        f"""  · Loading data\n"""
        f"""  · Elapsed: {(data_time - start_time)/10**6:.3f} ms\n\n"""
        f"""  · Part 1: {p1}\n"""
        f"""  · Elapsed: {(p1_time - data_time)/10**6:.3f} ms\n\n"""
        f"""  · Part 2: {p2}\n"""
        f"""  · Elapsed: {(end_time - p1_time)/10**6:.3f} ms\n\n"""
        f"""  · Total elapsed: {(end_time - start_time)/10**6:.3f} ms"""
    )
